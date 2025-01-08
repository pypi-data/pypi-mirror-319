from ..qwen2_vl.modeling_qwen2_vl import (
    Qwen2VLCausalLMOutputWithPast,
    Qwen2VLRotaryEmbedding,
    VisionRotaryEmbedding,
    PatchEmbed,
    PatchMerger,
    VisionMlp,
    VisionAttention, 
    VisionFlashAttention2,
    VisionSdpaAttention,
    Qwen2VLVisionBlock,
    Qwen2RMSNorm,
    Qwen2MLP,
    Qwen2VLAttention,
    Qwen2VLFlashAttention2,
    Qwen2VLSdpaAttention,
    Qwen2VLDecoderLayer,
    Qwen2VLPreTrainedModel,
    Qwen2VisionTransformerPretrainedModel,
    Qwen2VLModel,
    Qwen2VLForConditionalGeneration,
)
from ..qwen2_vl.configuration_qwen2_vl import Qwen2VLVisionConfig, Qwen2VLConfig
from ..qwen2_vl.processing_qwen2_vl import Qwen2VLProcessorKwargs, Qwen2VLProcessor
from ..qwen2_vl.image_processing_qwen2_vl import Qwen2VLImageProcessor


from ..llama.modeling_llama import (
    LlamaAttention,
    LlamaForCausalLM,
    LlamaForSequenceClassification,
    LlamaForTokenClassification,
    LlamaForQuestionAnswering,
    LlamaFlashAttention2,
    LlamaSdpaAttention,
    LlamaDecoderLayer,
    LlamaPreTrainedModel,
    LlamaRMSNorm,
    LlamaRotaryEmbedding,
    LlamaModel,
    LlamaMLP,
    apply_rotary_pos_emb,
    repeat_kv,
)
from ..llama.configuration_llama import LlamaConfig
from torch.nn import LayerNorm




import torch.nn as nn
import torch.nn.functional as F
from typing import Any, Dict, List, Optional, Tuple, Union, Sequence



import torch
from torch import Tensor
import numpy as np

from ...processing_utils import Unpack
from ...utils import (
    logging,
)


class FlexiPatchEmbed(nn.Module):
    def __init__(
        self,
        patch_size: int = 14,
        temporal_patch_size: int = 2,
        in_channels: int = 3,
        embed_dim: int = 1280,
        patch_size_seq: Sequence[int] = (12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32),
        interpolation: str = "bilinear",
        antialias: bool = True,
    ) -> None:
        super().__init__()
        self.in_channels = in_channels
        self.embed_dim = embed_dim
        self.temporal_patch_size = temporal_patch_size
        self.spatial_patch_size = patch_size
        self.patch_size = (temporal_patch_size, patch_size, patch_size)

        self.proj = nn.Conv3d(
            in_channels,
            embed_dim,
            kernel_size=self.patch_size,
            stride=self.patch_size,
            bias=False,
        )

        # Flexi specific attributes
        self.interpolation = interpolation
        self.antialias = antialias

        self.patch_size_seq = patch_size_seq

        # Pre-calculate pinvs
        self.pinvs = self._cache_pinvs()

    def _cache_pinvs(self) -> dict:
        """Pre-calculate all pinv matrices"""
        pinvs = {}
        for ps in self.patch_size_seq:
            ps = (self.temporal_patch_size, ps, ps)
            pinvs[ps] = self._calculate_pinv(self.patch_size, ps)
        return pinvs

    def _resize(self, conv_orig: Tensor, shape: Tuple[int, int, int]) -> Tensor:
        conv_orig = conv_orig.to(dtype=torch.float32)
        conv_resized = F.interpolate(
            conv_orig.unsqueeze(0),  # Add batch dimension: [1, 2, 14, 14]
            size=(shape[1], shape[2]),  # Preserve time dim, change spatial dims
            mode=self.interpolation,  # 2D interpolation
            align_corners=False,
            antialias=self.antialias,
        )

        return conv_resized[0, ...]

    def _calculate_pinv(self, old_shape: Tuple[int, int, int], new_shape: Tuple[int, int, int]) -> Tensor:
        mat = []
        for i in range(np.prod(old_shape)):
            basis_vec = torch.zeros(old_shape, device=self.proj.weight.device)
            basis_vec.view(-1)[i] = 1.0
            resized = self._resize(basis_vec, new_shape).reshape(-1)
            mat.append(resized)
        resize_matrix = torch.stack(mat)  # shape [prod(old_shape), prod(new_shape)]
        pinv = torch.linalg.pinv(resize_matrix)
        return pinv  # shape [prod(new_shape), prod(old_shape)]

    def resize_patch_embed(self, patch_embed: Tensor, new_patch_size: Tuple[int, int, int]):
        """Resize patch_embed to target resolution via pseudo-inverse resizing"""
        # Return original kernel if no resize is necessary
        if self.patch_size == new_patch_size:
            return patch_embed

        # Calculate pseudo-inverse of resize matrix
        if new_patch_size not in self.pinvs:
            self.pinvs[new_patch_size] = self._calculate_pinv(self.patch_size, new_patch_size)
        pinv = self.pinvs[new_patch_size]
        # shape [prod(new_shape), prod(old_shape)]
        pinv = pinv.to(patch_embed.device).to(device=patch_embed.device, dtype=patch_embed.dtype)

        # Reshape patch_embed to [embed_dim * in_chans, prod(old_shape)]
        patch_embed_flat = patch_embed.view(-1, np.prod(self.patch_size))  # [N, prod(old_shape)]

        # Apply pinv: resampled_flat = pinv @ patch_embed_flat.T
        resampled_flat = torch.matmul(pinv, patch_embed_flat.T).T  # [N, prod(new_shape)]

        # Reshape back to [embed_dim, in_chans, new_temporal_patch_size', new_hight', new_width']
        new_temporal_patch_size, new_hight, new_width = new_patch_size
        resampled = resampled_flat.view(
            patch_embed.shape[0], patch_embed.shape[1], new_temporal_patch_size, new_hight, new_width
        )
        return resampled

    def forward(self, hidden_states: torch.Tensor, patch_size: Optional[int] = None) -> torch.Tensor:
        target_dtype = self.proj.weight.dtype
        if patch_size is None:
            target_dtype = self.proj.weight.dtype
            hidden_states = hidden_states.view((-1, self.in_channels) + self.patch_size)
            hidden_states = self.proj(hidden_states.to(dtype=target_dtype)).view(-1, self.embed_dim)
        else:
            new_patch_size = (self.temporal_patch_size,) + (patch_size, patch_size)
            weight = self.resize_patch_embed(self.proj.weight, new_patch_size)
            stride = new_patch_size

            hidden_states = hidden_states.view(-1, self.in_channels, self.temporal_patch_size, patch_size, patch_size)

            hidden_states = F.conv3d(
                hidden_states.to(dtype=target_dtype),
                weight=weight,
                bias=None,
                stride=stride,
                padding=0,
            )

            # Flatten the spatial dimensions [batch_size, num_patches, embed_dim]
            hidden_states = hidden_states.flatten(2).transpose(1, 2).contiguous()
            hidden_states = hidden_states.permute(1, 0, 2).view(-1, self.embed_dim)

        return hidden_states



"""############################## CONFIG ##############################"""

class Falcon3VLVisionConfig(Qwen2VLVisionConfig):
    model_type = "falcon3_vl"
    base_config_key = "vision_config"

    def __init__(
        self,
        depth=32,
        embed_dim=1280,
        hidden_size=3072,
        hidden_act="quick_gelu",
        mlp_ratio=4,
        num_heads=16,
        in_channels=3,
        patch_size=14,
        spatial_merge_size=2,
        temporal_patch_size=2,
        patch_size_seq=[14],
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.patch_size_seq = patch_size_seq

class Falcon3VLConfig(LlamaConfig):
    model_type = "falcon3_vl"
    sub_configs = {"vision_config": Falcon3VLVisionConfig}
    keys_to_ignore_at_inference = ["past_key_values"]

    def __init__(
        self,
        vocab_size=32000,
        hidden_size=3072,
        intermediate_size=11008,
        num_hidden_layers=32,
        num_attention_heads=32,
        num_key_value_heads=None,
        hidden_act="silu",
        max_position_embeddings=2048,
        initializer_range=0.02,
        rms_norm_eps=1e-6,
        use_cache=True,
        pad_token_id=None,
        bos_token_id=1,
        eos_token_id=2,
        pretraining_tp=1,
        tie_word_embeddings=False,
        rope_theta=10000.0,
        rope_scaling=None,
        attention_bias=False,
        attention_dropout=0.0,
        mlp_bias=False,
        head_dim=None,
        vision_config=None,
        **kwargs,
    ):
        super().__init__(tie_word_embeddings=tie_word_embeddings, **kwargs)
        if isinstance(vision_config, dict):
            self.vision_config = Falcon3VLVisionConfig(**vision_config)
        elif vision_config is None:
            self.vision_config = Falcon3VLVisionConfig()

"""############################## PROCESSING ##############################"""

class Falcon3VLProcessorKwargs(Qwen2VLProcessorKwargs):
    pass

class Falcon3VLProcessor(Qwen2VLProcessor):
    image_processor_class = "Falcon3VLImageProcessor"
    tokenizer_class = ("PreTrainedTokenizer","PreTrainedTokenizerFast")

    def __init__(self, image_processor=None, tokenizer=None, chat_template=None, **kwargs):
        super().__init__(image_processor, tokenizer, chat_template=chat_template)
        self.image_token = "|<image>|" if not hasattr(tokenizer, "image_token") else tokenizer.image_token
        self.video_token = "|<video>|" if not hasattr(tokenizer, "video_token") else tokenizer.video_token

    def __call__(
        self,
        images: ImageInput = None,
        text: Union[TextInput, PreTokenizedInput, List[TextInput], List[PreTokenizedInput]] = None,
        videos: VideoInput = None,
        patch_size: int = None,
        **kwargs: Unpack[Falcon3VLProcessorKwargs],
    ) -> BatchFeature:
        """
        Main method to prepare for the model one or several sequences(s) and image(s). This method forwards the `text`
        and `kwargs` arguments to Qwen2TokenizerFast's [`~Qwen2TokenizerFast.__call__`] if `text` is not `None` to encode
        the text. To prepare the vision inputs, this method forwards the `vision_infos` and `kwrags` arguments to
        Falcon3VLImageProcessor's [`~Falcon3VLImageProcessor.__call__`] if `vision_infos` is not `None`.

        Args:
            images (`PIL.Image.Image`, `np.ndarray`, `torch.Tensor`, `List[PIL.Image.Image]`, `List[np.ndarray]`, `List[torch.Tensor]`):
                The image or batch of images to be prepared. Each image can be a PIL image, NumPy array or PyTorch
                tensor. Both channels-first and channels-last formats are supported.
            text (`str`, `List[str]`, `List[List[str]]`):
                The sequence or batch of sequences to be encoded. Each sequence can be a string or a list of strings
                (pretokenized string). If the sequences are provided as list of strings (pretokenized), you must set
                `is_split_into_words=True` (to lift the ambiguity with a batch of sequences).
            videos (`np.ndarray`, `torch.Tensor`, `List[np.ndarray]`, `List[torch.Tensor]`):
                The image or batch of videos to be prepared. Each video can be a 4D NumPy array or PyTorch
                tensor, or a nested list of 3D frames. Both channels-first and channels-last formats are supported.
            return_tensors (`str` or [`~utils.TensorType`], *optional*):
                If set, will return tensors of a particular framework. Acceptable values are:
                - `'tf'`: Return TensorFlow `tf.constant` objects.
                - `'pt'`: Return PyTorch `torch.Tensor` objects.
                - `'np'`: Return NumPy `np.ndarray` objects.
                - `'jax'`: Return JAX `jnp.ndarray` objects.

        Returns:
            [`BatchFeature`]: A [`BatchFeature`] with the following fields:

            - **input_ids** -- List of token ids to be fed to a model. Returned when `text` is not `None`.
            - **attention_mask** -- List of indices specifying which tokens should be attended to by the model (when
              `return_attention_mask=True` or if *"attention_mask"* is in `self.model_input_names` and if `text` is not
              `None`).
            - **pixel_values** -- Pixel values to be fed to a model. Returned when `images` is not `None`.
            - **pixel_values_videos** -- Pixel values of videos to be fed to a model. Returned when `videos` is not `None`.
            - **image_grid_thw** -- List of image 3D grid in LLM. Returned when `images` is not `None`.
            - **video_grid_thw** -- List of video 3D grid in LLM. Returned when `videos` is not `None`.
        """
        output_kwargs = self._merge_kwargs(
            Falcon3VLProcessorKwargs,
            tokenizer_init_kwargs=self.tokenizer.init_kwargs,
            **kwargs,
        )
        if images is not None:
            image_inputs = self.image_processor(images=images, patch_size=patch_size, videos=None, **output_kwargs["images_kwargs"])
            image_grid_thw = image_inputs["image_grid_thw"]
            if patch_size is not None: 
                image_inputs["patch_size"] = patch_size
        else:
            image_inputs = {}
            image_grid_thw = None

        videos_inputs = {}
        video_grid_thw = None

        if not isinstance(text, list):
            text = [text]

        if image_grid_thw is not None:
            merge_length = self.image_processor.merge_size**2
            index = 0
            for i in range(len(text)):
                while self.image_token in text[i]:
                    text[i] = text[i].replace(
                        self.image_token, "<|placeholder|>" * (image_grid_thw[index].prod() // merge_length), 1
                    )
                    index += 1
                text[i] = text[i].replace("<|placeholder|>", self.image_token)

        if video_grid_thw is not None:
            merge_length = self.image_processor.merge_size**2
            index = 0
            for i in range(len(text)):
                while self.video_token in text[i]:
                    text[i] = text[i].replace(
                        self.video_token, "<|placeholder|>" * (video_grid_thw[index].prod() // merge_length), 1
                    )
                    index += 1
                text[i] = text[i].replace("<|placeholder|>", self.video_token)

        text_inputs = self.tokenizer(text, **output_kwargs["text_kwargs"])

        return BatchFeature(data={**text_inputs, **image_inputs, **videos_inputs})


def smart_resize(
        height: int, width: int, factor: int = 28, min_pixels: int = 56 * 56, max_pixels: int = 14 * 14 * 4 * 1280
    ):
        if height < factor or width < factor:
            raise ValueError(f"height:{height} or width:{width} must be larger than factor:{factor}")
        elif max(height, width) / min(height, width) > 200:
            raise ValueError(
                f"absolute aspect ratio must be smaller than 200, got {max(height, width) / min(height, width)}"
            )
        h_bar = round(height / factor) * factor
        w_bar = round(width / factor) * factor
        if h_bar * w_bar > max_pixels:
            beta = np.sqrt((height * width) / max_pixels)
            h_bar = math.floor(height / beta / factor) * factor
            w_bar = math.floor(width / beta / factor) * factor
        elif h_bar * w_bar < min_pixels:
            beta = np.sqrt(min_pixels / (height * width))
            h_bar = math.ceil(height * beta / factor) * factor
            w_bar = math.ceil(width * beta / factor) * factor
        return h_bar, w_bar
class Falcon3VLImageProcessor(Qwen2VLImageProcessor):
    model_input_names = ["pixel_values", "image_grid_thw", "pixel_values_videos", "video_grid_thw", "padding_mask"]

    def _preprocess(
        self,
        images: Union[ImageInput, List[ImageInput]],
        do_resize: bool = None,
        resample: PILImageResampling = None,
        do_rescale: bool = None,
        rescale_factor: float = None,
        do_normalize: bool = None,
        image_mean: Optional[Union[float, List[float]]] = None,
        image_std: Optional[Union[float, List[float]]] = None,
        do_convert_rgb: bool = None,
        data_format: Optional[ChannelDimension] = ChannelDimension.FIRST,
        input_data_format: Optional[Union[str, ChannelDimension]] = None,
        patch_size: int = None,
    ):
        if patch_size is None:
            patch_size = self.patch_size

        images = make_list_of_images(images)

        if do_convert_rgb:
            images = [convert_to_rgb(image) for image in images]

        images = [to_numpy_array(image) for image in images]

        if is_scaled_image(images[0]) and do_rescale:
            logger.warning_once(
                "It looks like you are trying to rescale already rescaled images. If the input"
                " images have pixel values between 0 and 1, set `do_rescale=False` to avoid rescaling them again."
            )
        if input_data_format is None:
            input_data_format = infer_channel_dimension_format(images[0])

        height, width = get_image_size(images[0], channel_dim=input_data_format)
        resized_height, resized_width = height, width
        processed_images = []
        for image in images:
            if do_resize:
                resized_height, resized_width = smart_resize(
                    height,
                    width,
                    factor=patch_size * self.merge_size,
                    min_pixels=self.min_pixels,
                    max_pixels=self.max_pixels,
                )
                image = resize(
                    image, size=(resized_height, resized_width), resample=resample, input_data_format=input_data_format
                )
            if do_rescale:
                image = self.rescale(image, scale=rescale_factor, input_data_format=input_data_format)

            if do_normalize:
                image = self.normalize(
                    image=image, mean=image_mean, std=image_std, input_data_format=input_data_format
                )

            image = to_channel_dimension_format(image, data_format, input_channel_dim=input_data_format)
            processed_images.append(image)

        patches = np.array(processed_images)
        if data_format == ChannelDimension.LAST:
            patches = patches.transpose(0, 3, 1, 2)
        if patches.shape[0] == 1:
            patches = np.tile(patches, (self.temporal_patch_size, 1, 1, 1))
        channel = patches.shape[1]
        grid_t = patches.shape[0] // self.temporal_patch_size
        grid_h, grid_w = resized_height // patch_size, resized_width // patch_size
        patches = patches.reshape(
            grid_t,
            self.temporal_patch_size,
            channel,
            grid_h // self.merge_size,
            self.merge_size,
            patch_size,
            grid_w // self.merge_size,
            self.merge_size,
            patch_size,
        )
        patches = patches.transpose(0, 3, 6, 4, 7, 2, 1, 5, 8)
        flatten_patches = patches.reshape(
            grid_t * grid_h * grid_w, channel * self.temporal_patch_size * patch_size * patch_size
        )

        return flatten_patches, (grid_t, grid_h, grid_w)

    def preprocess(
        self,
        images: ImageInput,
        videos: Optional[List[ImageInput]] = None,
        do_resize: bool = None,
        size: Dict[str, int] = None,
        resample: PILImageResampling = None,
        do_rescale: bool = None,
        rescale_factor: float = None,
        do_normalize: bool = None,
        image_mean: Optional[Union[float, List[float]]] = None,
        image_std: Optional[Union[float, List[float]]] = None,
        do_convert_rgb: bool = None,
        return_tensors: Optional[Union[str, TensorType]] = None,
        data_format: Optional[ChannelDimension] = ChannelDimension.FIRST,
        input_data_format: Optional[Union[str, ChannelDimension]] = None,
        patch_size: int = None
    ):
        do_resize = do_resize if do_resize is not None else self.do_resize
        size = size if size is not None else self.size
        resample = resample if resample is not None else self.resample
        do_rescale = do_rescale if do_rescale is not None else self.do_rescale
        rescale_factor = rescale_factor if rescale_factor is not None else self.rescale_factor
        do_normalize = do_normalize if do_normalize is not None else self.do_normalize
        image_mean = image_mean if image_mean is not None else self.image_mean
        image_std = image_std if image_std is not None else self.image_std
        do_convert_rgb = do_convert_rgb if do_convert_rgb is not None else self.do_convert_rgb

        if patch_size is None:
            patch_size = self.patch_size
            print(f"Using default patch size {self.patch_size}")

        if images is not None:
            images = make_batched_images(images)
        if videos is not None:
            videos = make_batched_videos(videos)

        if images is not None and not valid_images(images):
            raise ValueError(
                "Invalid image type. Must be of type PIL.Image.Image, numpy.ndarray, "
                "torch.Tensor, tf.Tensor or jax.ndarray."
            )

        validate_preprocess_arguments(
            rescale_factor=rescale_factor,
            do_normalize=do_normalize,
            image_mean=image_mean,
            image_std=image_std,
            do_resize=do_resize,
            size=size,
            resample=resample,
        )

        if images is not None:
            pixel_values, vision_grid_thws = [], []
            max_grid_prod = 0
            for idx, image in enumerate(images):
                patches, image_grid_thw = self._preprocess(
                    image,
                    do_resize=do_resize,
                    resample=resample,
                    do_rescale=do_rescale,
                    rescale_factor=rescale_factor,
                    do_normalize=do_normalize,
                    image_mean=image_mean,
                    image_std=image_std,
                    data_format=data_format,
                    do_convert_rgb=do_convert_rgb,
                    input_data_format=input_data_format,
                    patch_size=patch_size
                )
                pixel_values.append(patches)
                vision_grid_thws.append(image_grid_thw)
                max_grid_prod = max(max_grid_prod, math.prod(image_grid_thw))
            
            padded_pixel_values = []
            for i, patches in enumerate(pixel_values):
                num_patches = patches.shape[0]
                padded_patches = torch.zeros((max_grid_prod, patches.shape[1]))
                padded_patches[:num_patches, :] = torch.tensor(patches, dtype=torch.float32)
                padded_pixel_values.append(padded_patches)
                

            padded_pixel_values = torch.stack(padded_pixel_values)
            vision_grid_thws = [tuple(int(x) for x in tup) for tup in vision_grid_thws]
            vision_grid_thws = torch.tensor(vision_grid_thws)
            data = {"pixel_values": padded_pixel_values, "image_grid_thw": vision_grid_thws}

        if videos is not None:
            pixel_values, vision_grid_thws = [], []
            max_grid_prod = 0
            for images in videos:
                patches, video_grid_thw = self._preprocess(
                    images,
                    do_resize=do_resize,
                    resample=resample,
                    do_rescale=do_rescale,
                    rescale_factor=rescale_factor,
                    do_normalize=do_normalize,
                    image_mean=image_mean,
                    image_std=image_std,
                    data_format=data_format,
                    do_convert_rgb=do_convert_rgb,
                    input_data_format=input_data_format,
                    patch_size=patch_size
                )
                pixel_values.append(patches)
                vision_grid_thws.append(video_grid_thw)
                max_grid_prod = max(max_grid_prod, math.prod(video_grid_thw))

            padded_pixel_values = []
            for i, patches in enumerate(pixel_values):
                num_patches = patches.shape[0]
                padded_patches = torch.zeros((max_grid_prod, patches.shape[1]))
                padded_patches[:num_patches, :] = torch.tensor(patches, dtype=torch.float32)
                padded_pixel_values.append(padded_patches)

            
            padded_pixel_values = torch.stack(padded_pixel_values)
            vision_grid_thws = [tuple(int(x) for x in tup) for tup in vision_grid_thws]
            vision_grid_thws = torch.tensor(vision_grid_thws)

            # pixel_values = np.array(pixel_values)
            # vision_grid_thws = np.array(vision_grid_thws)
            data = {"pixel_values_videos": padded_pixel_values, "video_grid_thw": vision_grid_thws}

        return BatchFeature(data=data, tensor_type=return_tensors)


"""############################## MODELING ##############################"""

class Falcon3VLCausalLMOutputWithPast(Qwen2VLCausalLMOutputWithPast):
    pass



class Falcon3VLRotaryEmbedding(LlamaRotaryEmbedding):
    pass

class VisionRotaryEmbedding(VisionRotaryEmbedding):
    pass

class PatchMerger(PatchMerger):
    def __init__(self, dim: int, context_dim: int, spatial_merge_size: int = 2) -> None:
        super().__init__()
        self.ln_q = LayerNorm(context_dim, eps=1e-6, bias=False)

class VisionMlp(VisionMlp):
    pass

class VisionAttention(VisionAttention):
    pass

class VisionFlashAttention2(VisionFlashAttention2):
    pass

class VisionSdpaAttention(VisionSdpaAttention):
    pass

class Falcon3VLVisionBlock(Qwen2VLVisionBlock):
    pass

class Falcon3RMSNorm(LlamaRMSNorm):
    pass

class Falcon3MLP(LlamaMLP):
    pass

class Falcon3VLAttention(LlamaAttention):
    pass

class Falcon3VLFlashAttention2(LlamaFlashAttention2):
    pass

class Falcon3VLSdpaAttention(LlamaSdpaAttention):
    pass

class Falcon3VLDecoderLayer(LlamaDecoderLayer):
    pass

class Falcon3VLPreTrainedModel(LlamaPreTrainedModel):
    pass

class Falcon3VisionTransformerPretrainedModel(Qwen2VisionTransformerPretrainedModel):
    
    def __init__(self, config) -> None:
        super().__init__(config)
        
        self.patch_embed = FlexiPatchEmbed(
            patch_size=config.patch_size,
            temporal_patch_size=config.temporal_patch_size,
            in_channels=config.in_channels,
            embed_dim=config.embed_dim,
            patch_size_seq=config.patch_size_seq,
        )
    
    def forward(self, hidden_states: torch.Tensor, grid_thw: torch.Tensor, patch_size: int) -> torch.Tensor:
        hidden_states = self.patch_embed(hidden_states, patch_size)
        rotary_pos_emb = self.rot_pos_emb(grid_thw)

        cu_seqlens = torch.repeat_interleave(grid_thw[:, 1] * grid_thw[:, 2], grid_thw[:, 0]).cumsum(
            dim=0, dtype=torch.int32
        )
        cu_seqlens = F.pad(cu_seqlens, (1, 0), value=0)

        for blk in self.blocks:
            hidden_states = blk(hidden_states, cu_seqlens=cu_seqlens, rotary_pos_emb=rotary_pos_emb)

        return self.merger(hidden_states)
class Falcon3VLModel(LlamaModel):
    pass

class Falcon3VLForConditionalGeneration(Qwen2VLForConditionalGeneration):
    def __init__(self, config):
        super().__init__(config)
        self.visual = Falcon3VisionTransformerPretrainedModel._from_config(config.vision_config)


    def forward(
        self,
        input_ids: torch.LongTensor = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[List[torch.FloatTensor]] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        cache_position: Optional[torch.LongTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
        pixel_values: Optional[torch.Tensor] = None,
        pixel_values_videos: Optional[torch.FloatTensor] = None,
        image_grid_thw: Optional[torch.LongTensor] = None,
        video_grid_thw: Optional[torch.LongTensor] = None,
        rope_deltas: Optional[torch.LongTensor] = None,
        patch_size: Optional[int] = None, 
    ) -> Union[Tuple, Falcon3VLCausalLMOutputWithPast]:
        r"""
        Args:
            labels (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*):
                Labels for computing the masked language modeling loss. Indices should either be in `[0, ...,
                config.vocab_size]` or -100 (see `input_ids` docstring). Tokens with indices set to `-100` are ignored
                (masked), the loss is only computed for the tokens with labels in `[0, ..., config.vocab_size]`.

        Returns:

        Example:

        ```python
        >>> from PIL import Image
        >>> import requests
        >>> from transformers import AutoProcessor, Falcon3VLForConditionalGeneration

        >>> model = Falcon3VLForConditionalGeneration.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")
        >>> processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")

        >>> messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image"},
                    {"type": "text", "text": "What is shown in this image?"},
                ],
            },
        ]
        >>> url = "https://www.ilankelman.org/stopsigns/australia.jpg"
        >>> image = Image.open(requests.get(url, stream=True).raw)

        >>> text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        >>> inputs = processor(text=[text], images=[image], vision_infos=[vision_infos])

        >>> # Generate
        >>> generate_ids = model.generate(inputs.input_ids, max_length=30)
        >>> tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        "The image shows a street scene with a red stop sign in the foreground. In the background, there is a large red gate with Chinese characters ..."
        ```"""

        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        if inputs_embeds is None:
            inputs_embeds = self.model.embed_tokens(input_ids)
            if pixel_values is not None:
                pixel_values = pixel_values.type(self.visual.get_dtype())
                image_embeds = self.visual(pixel_values, grid_thw=image_grid_thw, patch_size=patch_size)
                n_image_tokens = (input_ids == self.config.image_token_id).sum().item()
                n_image_features = image_embeds.shape[0]
                if n_image_tokens != n_image_features:
                    raise ValueError(
                        f"Image features and image tokens do not match: tokens: {n_image_tokens}, features {n_image_features}"
                    )
                image_mask = (
                    (input_ids == self.config.image_token_id)
                    .unsqueeze(-1)
                    .expand_as(inputs_embeds)
                    .to(inputs_embeds.device)
                )
                image_embeds = image_embeds.to(inputs_embeds.device, inputs_embeds.dtype)
                inputs_embeds = inputs_embeds.masked_scatter(image_mask, image_embeds)

            if pixel_values_videos is not None:
                pixel_values_videos = pixel_values_videos.type(self.visual.get_dtype())
                video_embeds = self.visual(pixel_values_videos, grid_thw=video_grid_thw)
                n_video_tokens = (input_ids == self.config.video_token_id).sum().item()
                n_video_features = video_embeds.shape[0]
                if n_video_tokens != n_video_features:
                    raise ValueError(
                        f"Video features and video tokens do not match: tokens: {n_video_tokens}, features {n_video_features}"
                    )
                video_mask = (
                    (input_ids == self.config.video_token_id)
                    .unsqueeze(-1)
                    .expand_as(inputs_embeds)
                    .to(inputs_embeds.device)
                )
                video_embeds = video_embeds.to(inputs_embeds.device, inputs_embeds.dtype)
                inputs_embeds = inputs_embeds.masked_scatter(video_mask, video_embeds)

            if attention_mask is not None:
                attention_mask = attention_mask.to(inputs_embeds.device)

        outputs = self.model(
            input_ids=None,
            position_ids=position_ids,
            attention_mask=attention_mask,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        hidden_states = outputs[0]
        logits = self.lm_head(hidden_states)

        loss = None
        if labels is not None:
            # Upcast to float if we need to compute the loss to avoid potential precision issues
            logits = logits.float()
            # Shift so that tokens < n predict n
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            # Flatten the tokens
            loss_fct = CrossEntropyLoss()
            shift_logits = shift_logits.view(-1, self.config.vocab_size)
            shift_labels = shift_labels.view(-1)
            # Enable model parallelism
            shift_labels = shift_labels.to(shift_logits.device)
            loss = loss_fct(shift_logits, shift_labels)

        if not return_dict:
            output = (logits,) + outputs[1:]
            return (loss,) + output if loss is not None else output

        return Falcon3VLCausalLMOutputWithPast(
            loss=loss,
            logits=logits,
            past_key_values=outputs.past_key_values,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
            rope_deltas=rope_deltas,
        )

    def prepare_inputs_for_generation(
        self,
        input_ids,
        past_key_values=None,
        attention_mask=None,
        inputs_embeds=None,
        cache_position=None,
        position_ids=None,
        use_cache=True,
        pixel_values=None,
        pixel_values_videos=None,
        image_grid_thw=None,
        video_grid_thw=None,
        patch_size=None, 
        token_type_ids=None,
        **kwargs,
    ):
        """
        Prepare the model inputs for generation. In includes operations like computing the 4D attention mask or
        slicing inputs given the existing cache.

        See the forward pass in the model documentation for expected arguments (different models might have different
        requirements for e.g. `past_key_values`). This function should work as is for most LLMs.
        """
        inputs = super().prepare_inputs_for_generation(
            input_ids, 
            past_key_values=past_key_values, 
            attention_mask=attention_mask,
            inputs_embeds=inputs_embeds, 
            cache_position=cache_position,
            position_ids=position_ids,
            use_cache=use_cache,
            pixel_values=pixel_values,
            pixel_values_videos=pixel_values_videos,
            image_grid_thw=image_grid_thw,
            video_grid_thw=video_grid_thw,
            patch_size=patch_size,
            **kwargs
        )

        if cache_position[0] != 0:
            inputs['pixel_values'] = None
            inputs['pixel_values_videos'] = None


        return inputs
    
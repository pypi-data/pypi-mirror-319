# coding=utf-8
# Copyright 2024 the HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""PyTorch Falcon3Audio model."""

from ..qwen2_audio.modeling_qwen2_audio import (
    Qwen2AudioProcessor,
    Qwen2AudioAttention,
    Qwen2AudioEncoderLayer,
    Qwen2AudioPreTrainedModel,
    Qwen2AudioEncoder,
    Qwen2AudioFlashAttention2, 
    Qwen2AudioSdpaAttention,
    Qwen2AudioCausalLMOutputWithPast,
    Qwen2AudioForConditionalGeneration
)
from ..qwen2_audio.configuration_qwen2_audio import Qwen2AudioEncoderConfig, Qwen2AudioConfig
from ..qwen2_audio.processing_qwen2_audio import Qwen2AudioProcessor
import torch.nn as nn
import torch.nn.functional as F
from typing import Any, Dict, List, Optional, Tuple, Union



import torch

from ...processing_utils import Unpack
from ...utils import (
    logging,
)

class Falcon3AudioCausalLMOutputWithPast(Qwen2AudioCausalLMOutputWithPast):
    pass

class Falcon3AudioEncoderConfig(Qwen2AudioEncoderConfig):
    pass

class Falcon3AudioConfig(Qwen2AudioConfig):
    def __init__(
        self,
        audio_config=None,
        text_config=None,
        audio_token_index=151646,
        stack_factor_for_projector=8,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.audio_token_index = audio_token_index
        self.stack_factor_for_projector = stack_factor_for_projector




class Falcon3AudioProcessor(Qwen2AudioProcessor):
    @property
    def default_chat_template(self):
        """
        This default vicuna template formats inputs in the form of a chat history. For each message in the chat history:
        * the template will output the role of the speaker followed by the content of the message.
        * content is a list of strings and audios.
        * If the content element is an audio, the template will output a sequence of <|AUDIO|> tokens

        Example:

        ```python
        messages = [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {"role": "user", "content": [
                {"type": "audio", "audio_url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen2-Audio/audio/glass-breaking-151256.mp3"},
                {"type": "text", "text": "What's that sound?"},
            ]},
            {"role": "assistant", "content": "It is the sound of glass shattering."},
            {"role": "user", "content": [
                {"type": "audio", "audio_url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen2-Audio/audio/f2641_0_throatclearing.wav"},
                {"type": "text", "text": "How about this one?"},
            ]},
        ]

        result = template.render(messages=messages, add_generation_prompt=True)
        ```
        """
        # fmt: off
        return (
            "{% for message in messages %}"
                "{% for content in message['content'] %}"
                    "{% if content['type'] == 'audio' or 'audio_url' in content %}"
                        "<|im_start|><|AUDIO|><|im_end|>\n"
                    "{% endif %}"
                "{% endfor %}"
            "{% endfor %}"
            "{% for message in messages %}"
                "{% if loop.first and message['role'] == 'system' %}"
                    "<|im_start|><|system|>\nYou are Falcon-Audio, an AI assistant developed by the Technology Innovation Institute, Abu Dhabi. As a helpful and capable assistant, you carefully process input audio step-by-step and provide accurate responses to user queries.<|im_end|>\n"
                "{% endif %}"
                "{% if message['content'] is not string %}"
                    "<|im_start|><|user|>\n"
                    "{% for content in message['content'] %}"
                        "{% if 'text' in content %}"
                            "{{ content['text'] }}"
                        "{% endif %}"
                    "{% endfor %}"
                    "<|im_end|>\n"
                "{% endif %}"
            "{% endfor %}"
            "{% if add_generation_prompt %}"
                "<|im_start|><|assistant|>\n"
            "{% endif %}"
        )


class Falcon3AudioAttention(Qwen2AudioAttention):
    pass

class Falcon3AudioFlashAttention2(Qwen2AudioFlashAttention2):
    pass 


class Falcon3AudioSdpaAttention(Qwen2AudioSdpaAttention):
    pass

class Falcon3AudioEncoderLayer(Qwen2AudioEncoderLayer):
    pass

class Falcon3AudioPreTrainedModel(Qwen2AudioPreTrainedModel):
    pass

class Falcon3AudioEncoder(Qwen2AudioEncoder):
    pass

class StackAudioFrames(nn.Module):
    """
    Stack the audio embedding frames to reduce the sequence length by a factor of `stack_factor`.
    The number of output frames will be `ceil(T / stack_factor) + 1` where `T` is the number of input frames.
    NOTE: the extra +1 is intentional: in case the number of audio tokens are over-estimated by the processor,
    we want to make sure `processor.audio_token_replacement` (i.e. EOS) doesn't get leaked into the middle of embeddings.
    In most cases this extra padding will get removed in the model's forward function so it has no effect.
    """
    def __init__(self, stack_factor: int = 8):
        super().__init__()
        self.stack_factor = stack_factor
    def forward(self, audio_embeds: torch.Tensor) -> torch.Tensor:
        batch_size, num_audio_frames, hidden_dimension = audio_embeds.shape
        num_audio_frames_pad = (num_audio_frames + self.stack_factor - 1) // self.stack_factor * self.stack_factor
        audio_embeds = F.pad(audio_embeds, (0, 0, 0, num_audio_frames_pad - num_audio_frames + self.stack_factor))
        batch_size, num_audio_frames, hidden_dimension = audio_embeds.shape
        audio_embeds = audio_embeds.view(
            batch_size, num_audio_frames // self.stack_factor, hidden_dimension * self.stack_factor
        )
        return audio_embeds

class Falcon3AudioMultiModalProjector(nn.Module):
    def __init__(self, config: Falcon3AudioConfig, stack_factor: int = 8):
        super().__init__()
        self.stack_factor = stack_factor
        self._pad_and_stack = StackAudioFrames(stack_factor=stack_factor)
        self.input_dim = config.audio_config.d_model * stack_factor
        self.layer_norm_entry = nn.LayerNorm(self.input_dim)
        self.linear_1 = nn.Linear(self.input_dim, config.text_config.hidden_size, bias=True)
        self.act = nn.GELU()
        self.linear_2 = nn.Linear(config.text_config.hidden_size, config.text_config.hidden_size, bias=True)
        self.layer_norm_exit = nn.LayerNorm(config.text_config.hidden_size)
        
    def forward(self, audio_features):
        audio_features = self._pad_and_stack(audio_features)
        hidden_states = self.layer_norm_entry(audio_features)
        hidden_states = self.linear_1(hidden_states)
        hidden_states = self.act(hidden_states)
        hidden_states = self.linear_2(hidden_states)
        hidden_states = self.layer_norm_exit(hidden_states)
        return hidden_states

class Falcon3AudioForConditionalGeneration(Qwen2AudioForConditionalGeneration):
    def __init__(self, config: Falcon3AudioConfig):
        super().__init__(config)
        self.multi_modal_projector = Falcon3AudioMultiModalProjector(config, stack_factor=config.stack_factor_for_projector)

    def _process_audio_encoder_hidden_states(self, hidden_states: torch.FloatTensor):
        hidden_states = hidden_states.permute(0, 2, 1)
        hidden_states = self.audio_tower.avg_pooler(hidden_states)
        hidden_states = hidden_states.permute(0, 2, 1)
        hidden_states = self.audio_tower.layer_norm(hidden_states)
        return hidden_states  

    def _get_feat_extract_output_lengths_modified(self, input_lengths: torch.LongTensor, stack_factor: int = 8):
        """
        Computes the output length of the convolutional layers and the output length of the audio encoder
        """
        input_lengths = (input_lengths - 1) // 2 + 1
        output_lengths = (input_lengths - 2) // 2 + 1
        # added the following line to account for the stack factor
        output_lengths = torch.ceil(output_lengths / stack_factor) + 1
        return input_lengths, output_lengths

    def forward(
        self,
        input_ids: torch.LongTensor = None,
        input_features: torch.FloatTensor = None,
        attention_mask: Optional[torch.Tensor] = None,
        feature_attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[List[torch.FloatTensor]] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
    ) -> Union[Tuple, Falcon3AudioCausalLMOutputWithPast]:
        r"""
        Args:
            labels (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*):
                Labels for computing the masked language modeling loss. Indices should either be in `[0, ...,
                config.vocab_size]` or -100 (see `input_ids` docstring). Tokens with indices set to `-100` are ignored
                (masked), the loss is only computed for the tokens with labels in `[0, ..., config.vocab_size]`.
        Returns:
        Example:
        ```python
        >>> from io import BytesIO
        >>> from urllib.request import urlopen
        >>> import librosa
        >>> from transformers import AutoProcessor, Falcon3AudioForConditionalGeneration
        >>> model = Falcon3AudioForConditionalGeneration.from_pretrained("Qwen/Falcon3-Audio-7B")
        >>> processor = AutoProcessor.from_pretrained("Qwen/Falcon3-Audio-7B")
        >>> prompt = "<|audio_bos|><|AUDIO|><|audio_eos|>Generate the caption in English:"
        >>> url = "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Falcon3-Audio/audio/glass-breaking-151256.mp3"
        >>> audio, _ = librosa.load(BytesIO(urlopen(url).read()), sr=self.processor.feature_extractor.sampling_rate)
        >>> inputs = processor(text=prompt, audios=audio, return_tensors="pt")
        >>> # Generate
        >>> generate_ids = model.generate(**inputs, max_length=30)
        >>> processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        "Generate the caption in English: Glass is breaking."
        ```"""
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict
        target_device = self.audio_tower.device
        if input_features is not None:
            input_features = input_features.to(target_device)
            feature_attention_mask = feature_attention_mask.to(target_device)
        if inputs_embeds is None:
            # 1. Extract the input embeddings
            inputs_embeds = self.get_input_embeddings()(input_ids)
            # 2. Merge text and audios
            if input_features is not None and input_ids.shape[1] != 1:
                audio_feat_lengths, audio_output_lengths = self._get_feat_extract_output_lengths_modified(
                    feature_attention_mask.sum(-1),
                    stack_factor=self.config.stack_factor_for_projector
                )
                batch_size, _, max_mel_seq_len = input_features.shape
                max_seq_len = (max_mel_seq_len - 2) // 2 + 1
                # Create a sequence tensor of shape (batch_size, max_seq_len)
                seq_range = torch.arange(0, max_seq_len, dtype=audio_feat_lengths.dtype, device=audio_feat_lengths.device)
                seq_range = seq_range.unsqueeze(0).expand(batch_size, max_seq_len)

                lengths_expand = audio_feat_lengths.unsqueeze(1).expand(batch_size, max_seq_len)
                # Create mask
                padding_mask = seq_range >= lengths_expand
                audio_attention_mask_ = padding_mask.view(batch_size, 1, 1, max_seq_len).expand(
                    batch_size, 1, max_seq_len, max_seq_len
                )
                audio_attention_mask = audio_attention_mask_.to(
                    dtype=self.audio_tower.conv1.weight.dtype, device=self.audio_tower.conv1.weight.device
                )
                audio_attention_mask[audio_attention_mask_] = float("-inf")

                audio_outputs = self.audio_tower(input_features, attention_mask=audio_attention_mask, output_hidden_states=False)
                selected_audio_feature = audio_outputs.last_hidden_state
                audio_features = self.multi_modal_projector(selected_audio_feature)

                inputs_embeds, attention_mask, labels, position_ids, _ = self._merge_input_ids_with_audio_features(
                    audio_features, audio_output_lengths, inputs_embeds, input_ids, attention_mask, labels
                )
        outputs = self.language_model(
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )
        logits = outputs[0]
        loss = None
        if labels is not None:
            # Shift so that tokens < n predict n
            if attention_mask is not None:
                shift_attention_mask = attention_mask[..., 1:]
                shift_logits = logits[..., :-1, :][shift_attention_mask.to(logits.device) != 0].contiguous()
                shift_labels = labels[..., 1:][shift_attention_mask.to(labels.device) != 0].contiguous()
            else:
                shift_logits = logits[..., :-1, :].contiguous()
                shift_labels = labels[..., 1:].contiguous()
            # Flatten the tokens
            loss_fct = nn.CrossEntropyLoss()
            loss = loss_fct(
                shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1).to(shift_logits.device)
            )
        if not return_dict:
            output = (logits,) + outputs[1:]
            return (loss,) + output if loss is not None else output
        return Falcon3AudioCausalLMOutputWithPast(
            loss=loss,
            logits=logits,
            past_key_values=outputs.past_key_values,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
            attention_mask=attention_mask,
        )

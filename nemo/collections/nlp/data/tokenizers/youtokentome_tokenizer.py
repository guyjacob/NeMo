# =============================================================================
# Copyright 2020 NVIDIA. All Rights Reserved.
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
# =============================================================================

import youtokentome as yttm

from nemo.collections.nlp.data.tokenizers.tokenizer_spec import TokenizerSpec

__all__ = ['YouTokenToMeTokenizer']


class YouTokenToMeTokenizer(TokenizerSpec):
    def __init__(self, model_path):
        self.tokenizer = yttm.BPE(model=model_path)
        self.vocab_size = len(self.tokenizer.vocab())
        self.special_tokens = self.tokens_to_ids(["<PAD>", "<UNK>", "<BOS>", "<EOS>"])

    def text_to_tokens(self, text):
        return self.tokenizer.encode(text, output_type=yttm.OutputType.SUBWORD)

    def tokens_to_text(self, tokens):
        return self.ids_to_text(self.tokens_to_ids(tokens))

    def text_to_ids(self, text):
        return self.tokenizer.encode(text, output_type=yttm.OutputType.ID)

    def ids_to_text(self, ids):
        ids_ = [id_ for id_ in ids if id_ not in self.special_tokens]
        return self.tokenizer.decode([ids_])[0]

    def tokens_to_ids(self, tokens):
        return [self.tokenizer.subword_to_id(token) for token in tokens]

    def ids_to_tokens(self, ids):
        ids_ = [id_ for id_ in ids if id_ not in self.special_tokens]
        return [self.tokenizer.id_to_subword(id_) for id_ in ids_]

    def pad_id(self):
        return self.tokenizer.subword_to_id("<PAD>")

    def bos_id(self):
        return self.tokenizer.subword_to_id("<BOS>")

    def eos_id(self):
        return self.tokenizer.subword_to_id("<EOS>")

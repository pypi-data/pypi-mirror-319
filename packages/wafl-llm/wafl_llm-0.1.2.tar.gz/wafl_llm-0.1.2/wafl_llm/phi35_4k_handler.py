import json
import logging
import os
from typing import Dict

import torch
from transformers import AutoTokenizer

from vllm import LLM, SamplingParams
from ts.torch_handler.base_handler import BaseHandler
from wafl_llm.variables import get_variables

_path = os.path.dirname(__file__)
_logger = logging.getLogger(__file__)


class Phi35Mini4KHandler(BaseHandler):
    def __init__(self, config):
        super().__init__()
        self.initialized = False
        _logger.info("The handler is created!")
        self._config = config
        self._last_strings = [
            "\nuser",
            "\nbot",
            "\nUser",
            "\nBot",
            "<|EOS|>",
            "</remember>",
            "</execute>\n",
            "</s>",
            "<|end|>",
            "<|assistant|>",
            "<|user|>",
            "\n\n---",
            "\n\n- output:",
            "\n\n- ai:",
            "\n\n- user:",
            "\n\n- response:",
            "[delete_rule]",
            "=====",
        ]

    def initialize(self, ctx):
        self.manifest = ctx.manifest
        model_name = self._config["llm_model"]
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        _logger.info(f"Loading the model {model_name}.")
        args = self._get_arguments()
        self._llm = LLM(model=model_name, max_model_len=4096, **args)
        _logger.info(f"Transformer model {model_name} loaded successfully.")
        self.initialized = True

    def preprocess(self, data):
        prompt = self._get_text_prompt(data[0].get("body").get("data"))
        temperature = data[0].get("body").get("temperature")
        num_tokens = data[0].get("body").get("num_tokens")
        num_replicas = data[0].get("body").get("num_replicas")
        return {
            "prompt": prompt,
            "temperature": temperature,
            "num_tokens": num_tokens,
            "last_strings": self._last_strings,
            "num_replicas": num_replicas,
        }

    def inference(self, data):
        with torch.no_grad():
            prompt = data["prompt"]
            temperature = data["temperature"]
            num_tokens = data["num_tokens"]
            last_strings = data["last_strings"]
            num_replicas = data["num_replicas"]
            prompts = [prompt] * num_replicas
            sampling_params = SamplingParams(
                temperature=temperature,
                top_p=0.95,
                stop=last_strings,
                max_tokens=num_tokens,
            )
            outputs = self._llm.generate(prompts, sampling_params)
            print(outputs[0].outputs[0].text)
            return "<||>".join(output.outputs[0].text for output in outputs)

    def postprocess(self, inference_output):
        return [
            json.dumps(
                {
                    "prediction": inference_output,
                    "status": "success",
                    "version": get_variables()["version"],
                    "model": self._config["llm_model"],
                }
            )
        ]

    def _get_text_prompt(self, chat_template_dictionary):
        chat_template_list = []
        for item in chat_template_dictionary["conversation"]:
            speaker = item["speaker"]
            text = item["text"]
            if speaker.lower() == "user":
                chat_template_list.append({"role": "user", "content": text})
            if speaker.lower() in ["assistant", "bot"]:
                chat_template_list.append({"role": "assistant", "content": text})
        input_ids = self._tokenizer.encode(
            "<|system|>\n"
            + chat_template_dictionary["system_prompt"]
            + "\n<|end|>"
        )
        input_ids = (
            input_ids + self._tokenizer.apply_chat_template(chat_template_list)
        )[:-1]
        input_ids = input_ids + self._tokenizer.encode("<|assistant|>")
        prompt = self._tokenizer.decode(input_ids)
        print(prompt)
        return prompt


    def _get_system_prompt_input_ids(self, chat_template_dictionary):
        system_prompt = chat_template_dictionary["system_prompt"]
        input_ids = self._tokenizer.encode(system_prompt)
        return input_ids

    def _get_arguments(self) -> Dict[str, str]:
        if "quantization" in self._config and self._config["quantization"]:
            _logger.info("Quantization is enabled.")
            return {
                "quantization": "fp8",
                "swap_space": 1,
            }

        return {
            "dtype": "bfloat16",
            "swap_space": 1,
        }

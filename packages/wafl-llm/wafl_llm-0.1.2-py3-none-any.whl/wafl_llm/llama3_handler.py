import json
import logging
import os
import torch
from transformers import AutoTokenizer

from vllm import LLM, SamplingParams
from ts.torch_handler.base_handler import BaseHandler
from wafl_llm.variables import get_variables

_path = os.path.dirname(__file__)
_logger = logging.getLogger(__file__)


class Llama3LLMHandler(BaseHandler):
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
            "\n\nComputer:" "<|EOS|>",
            "</remember>",
            "</execute>\n",
            "</s>",
            "<|im_end|>",
            "<|eot_id|>",
            "[delete_rule]",
        ]

    def initialize(self, ctx):
        self.manifest = ctx.manifest
        model_name = self._config["llm_model"]
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        _logger.info(f"Loading the model {model_name}.")
        self._llm = LLM(model=model_name, dtype="bfloat16")
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
            print(prompt)
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
            print(outputs)

            generated_texts = "<||>".join(output.outputs[0].text for output in outputs)
            generated_texts = (
                generated_texts.replace("<|im_start|>assistant\n", "")
                .replace("<|im_start|>user\n", "")
                .replace("<|im_start|>system\n", "")
                .replace("<|im_start|>bot\n", "")
            )
            return generated_texts

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
        chat_template_list.append(
            {"role": "system", "content": chat_template_dictionary["system_prompt"]}
        )
        for item in chat_template_dictionary["conversation"]:
            speaker = item["speaker"]
            text = item["text"]
            if speaker.lower() == "user":
                chat_template_list.append({"role": "user", "content": text})
            if speaker.lower() in ["assistant", "bot"]:
                chat_template_list.append({"role": "assistant", "content": text})

        prompt = self._tokenizer.decode(
            self._tokenizer.apply_chat_template(chat_template_list)
        )
        return prompt

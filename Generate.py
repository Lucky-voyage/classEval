import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig


class Generator:

    def __init__(self,
                 model,
                 tokenizer,
                 device,
                 temperature=0.5):
        self.device = device
        self.model = model
        self.tokenizer = tokenizer
        self.config = GenerationConfig(temperature=temperature)

    def get_answer(self, prompts, num) -> list:
        ret_ans = []

        tokens = self.tokenizer(prompts, return_tensors='pt')
        input_ids = tokens['input_ids'].to(self.device)

        with torch.no_grad():
            for i in range(num):
                output = self.model.generate(
                    input_ids=input_ids,
                    # generate_config=self.config,
                    # return_dict_in_generate=True
                )
                answer = self.tokenizer.decode(output.sequence,
                                               skip_special_tokens=True)
                ret_ans.append(answer)

        return ret_ans

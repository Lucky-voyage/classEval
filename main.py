import os.path

import fire
import torch
import json
from pathlib import Path

from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM
from DataLoader import DataLoader
from Generate import Generator
from TextProcessor import TextProcessor
from EvaluateUnit import EvaluateUnit

if torch.cuda.is_available():
    device = 'cuda'
else:
    device = 'auto'

import sys
sys.path.append('C:\\Users\\86166\\Desktop\\ClassEval_\\ClassEval_Project')

def main(
        checkpoint="C:\\Users\\86166\\Desktop\\gpt2-medium",
        data_path="data/ClassEval.json",
        output_path="output/raw_output.json",
        code_path="output/generate_code",
        test_path="data/benchmark_test_code",
        # load_in_8bit=True,
        torch_dtype=torch.float16,
        num=100
):
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForCausalLM.from_pretrained(
        checkpoint,
        # load_in_8bit=load_in_8bit,
        torch_dtype=torch_dtype,
        device_map=device
    )
    data_loader = DataLoader(data_path)
    generate = Generator(model, tokenizer, 'cpu')

    code_file = Path(code_path)
    prompts = data_loader.get_prompt()

    # generate code and write in files
    raw_txt_list = []
    for idx, prompt in enumerate(prompts):
        task_id = prompt['task_id']
        class_name = prompt['class_name']
        answers = generate.get_answer(prompt['prompt'], num)
        # extract code
        code_list = TextProcessor.code(answers)

        # write code in file
        dir_name = code_file / class_name
        if not os.path.exists(str(dir_name)):
            os.makedirs(str(dir_name))

        for i, code in enumerate(code_list):
            file_name = str(dir_name / (class_name + str(i) + '.py'))

            if not os.path.exists(file_name):
                os.makedirs(file_name)

            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(code)

        # save raw_output to list
        item = {'task_id': task_id, 'class_name': class_name, 'output': answers}
        raw_txt_list.append(item)

    # write raw outputs to file
    raw_output_path = Path(output_path) / "raw_output.json"
    if not os.path.exists(str(raw_output_path)):
        os.makedirs(str(raw_output_path))
    with open(str(raw_output_path), 'w', encoding='utf-8') as file:
        json.load(file)

    # test code
    result = []
    for item in data_loader.data:
        task_id = item['task_id']
        class_name = item['class_name']
        test_classes = item['test_class']
        test_class_path = Path(test_path) / (class_name + '.py')

        result_ = {'task_id': task_id, 'runs': 0,
                   'failures': 0, 'errors': 0}
        for i in range(num):
            class_path = Path(output_path) / "generate_code" / f"{class_name}{i}.py"
            res = EvaluateUnit.test(class_name, test_classes, str(class_path), str(test_class_path))
            result_['runs'] += res['runs']
            result_['failures'] += res['failures']
            result_['errors'] += res['errors']

        result.append(result_)

    with open(output_path + f"result.json", 'w', encoding='uf-8') as file:
        json.dump(result, file)


if __name__ == '__main__':
    fire.Fire(main)

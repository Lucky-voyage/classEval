import json


class DataLoader:

    def __init__(self, data_path, batch_size=1):
        self.batch_size = batch_size
        self.data = self.load_data(data_path)
        self.len = len(self.data)

    @staticmethod
    def load_data(data_path):
        with open(str(data_path), 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    @staticmethod
    def generate_prompt(skeleton: str):
        return f"""Below is an instruction that describes a task. Fill the function to complete the task.
        ### Instruction:
                {skeleton}
        ### Response:
        """

    def get_prompt(self):
        ret_list = []
        for item in self.data:
            info = item
            info['prompt'] = self.generate_prompt(item['skeleton'])
            del info['skeleton']
            ret_list.append(info)

        return ret_list

    def get_class_name(self, task_id):
        return self.data[task_id]['class_name']



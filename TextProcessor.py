import re


class TextProcessor:

    def __init__(self):
        pass

    @staticmethod
    def code(text: list) -> list:
        ret = []
        for item in text:
            ret.append(TextProcessor.extract_code(item))

        return ret

    @staticmethod
    def extract_code(text):

        def get_leading_spaces(string):
            return len(string) - len(string.strip())

        text = text.rstrip()
        output_split_identifier_list = ["### Response:", "@@ Response:", "[/INST]"]
        for identifier in output_split_identifier_list:
            if identifier in text:
                text = text.split(identifier)[1]
                break

        pattern_list = [r"```python(.*?)```", r"```ruby(.*?)```", r"```scss(.*?)```",
                        r"```python(.*?)", r"```(.*?)```", r"\[PYTHON\](.*?)\[/PYTHON\]"]
        for pattern in pattern_list:
            try:
                code = re.findall(pattern, text, re.S)[0]
                return code
            except:
                continue

        code_list = text.split("\n")
        removed_lines = []
        for code_line in code_list:
            if code_line.strip().startswith('class'):
                break
            elif not code_line.strip().startswith('import') and not code_line.strip().startswith('from'):
                removed_lines.append(code_line)
        code_list = [line for line in code_list if line not in removed_lines]
        text = '\n'.join(code_list)

        wrong_indent_flag = False
        class_signature_line_leading_spaces = 0
        for code_line in text.split("\n"):
            if code_line.strip().startswith('class'):
                class_signature_line_leading_spaces = get_leading_spaces(code_line)
                if class_signature_line_leading_spaces != 0:
                    wrong_indent_flag = True
                break
        if wrong_indent_flag:
            final_code_line_list = []
            for code_line in text.split("\n"):
                cur_leading_spaces = get_leading_spaces(code_line)
                # Keep the relative indentation unchanged
                final_code_line_list.append(
                    ' ' * (cur_leading_spaces - class_signature_line_leading_spaces) + code_line.lstrip())
            text = '\n'.join(final_code_line_list)
        return text

    @staticmethod
    def extract_imports(text):
        pattern = r'^import\s.*$|from\s.*\simport.*$'
        imports = re.findall(pattern, text, re.MULTILINE)
        return imports

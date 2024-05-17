import unittest
import importlib


class EvaluateUnit:

    def __init__(self):
        pass

    @staticmethod
    def test(class_name, test_classes: list, class_path, test_path):
        ret_dict = {'runs': 0, 'failures': 0, 'errors': 0}

        # add import statement
        with open(test_path, 'r', encoding='utf-8') as file:
            content = file.read()

        import_method = class_path.replace('\\', '.')[:-3]

        if not content.startswith('# tag\n'):
            content = "# tag\n" + f"from {import_method} import {class_name}\n" + content
            with open(test_path, 'w', encoding='utf-8') as file:
                file.write(content)

        module = importlib.import_module(test_path.replace("\\", '.')[:-3])
        for test_class in test_classes:
            TEST = getattr(module, test_class)

            loader = unittest.TestLoader()
            suite = loader.loadTestsFromTestCase(TEST)

            runner = unittest.TextTestRunner()
            result = runner.run(suite)

            ret_dict['failures'] += result.failures.__len__()
            ret_dict['errors'] += result.errors.__len__()
            ret_dict['runs'] += result.testsRun - result.failures.__len__() - result.errors.__len__()

        return ret_dict

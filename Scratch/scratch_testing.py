# tests for determining possibilities of dictionaries regarding functions

# define basic class with methods
class DictionaryFunctionalityTests:

    def __init__(self):
        self.instruction_dict = instruction_dict = {"x2": self.x2(nb=number),
                                                    "split_string": self.split_string(text=txt)}

    def add_instruction(self):
        new_instruction = {"new": "new"}
        self.instruction_dict = self.instruction_dict | new_instruction


    def x2(self, nb):
        nb2 = nb * 2
        return nb2

    def split_string(self, text):
        split_text = text.split()
        return split_text

    def updated_instruction(self, name):
        return "updated instruction --{}-- with successful functionality".format(name)


number = 5
txt = "word1 word2"
new_name = "new_name"

dict_test = DictionaryFunctionalityTests()
dict_test.add_instruction({'updated_instruction': self.updated_instruction(new_name)})


output_number, output_text, update_method = [dict_test.instruction_dict['x2'],
                                             dict_test.instruction_dict['split_string'],
                                             dict_test.instruction_dict['updated_instruction']]

print(output_number, '/n', output_text, update_method)

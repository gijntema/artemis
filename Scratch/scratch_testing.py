

# script just to try out the working of some python concepts, packages and modules, has no functionality in the model

# Containing references to functions in dictionaries
# define function
def func_test(text):
    print(text)


a = dict()                                  # initialize dict
a['func_test'] = func_test                  # refer to function in dictionary
a['func_test']('test_text')                 # execute function, contained in dictionary
print(a['func_test'])                       # print the reference to a function in the dictionary


# Containing class methods in dictionaries
class ScratchTesting:

    def __init__(self):
        self.bananas = 'TEST VALUE'
        self.instructions = {'key_test': self.method_test}

    def method_test(self, text):
        print(text)


key_test = 'key_test'
class_test = ScratchTesting()
print(class_test.method_test)
print(class_test.instructions[key_test])
class_test.instructions[key_test]('TestText')

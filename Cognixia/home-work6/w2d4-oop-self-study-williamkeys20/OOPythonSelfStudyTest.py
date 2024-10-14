import nbformat
import unittest
from unittest.mock import patch

# Function to extract code cells from a notebook
def extract_code_cells(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as nb_file:
        nb_contents = nbformat.read(nb_file, as_version=4)
    code_cells = [cell['source'] for cell in nb_contents.cells if cell.cell_type == 'code']
    return code_cells

# Function to dynamically execute extracted code
# All code will execute. Make sure any calls to functions is wrapped in `if __name__ == "__main__": `
def execute_code(code_cells):
    code_snippets = "\n".join(code_cells)
    exec_globals = {}
    exec(code_snippets, exec_globals)
    return exec_globals


# Provided test case
class TestTestCaseHere(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load the notebook
        with open('OOPythonSelfStudy.ipynb', 'r', encoding='utf-8') as f:
            cls.nb = nbformat.read(f, as_version=4)

        # Extract solution blocks
        cls.solutions = []
        for cell in cls.nb.cells:
            if cell.cell_type == 'code' or cell.cell_type == 'markdown':
                source = cell.source
                if '### BEGIN SOLUTION' in source and '### END SOLUTION' in source:
                    solution_block = source.split('### BEGIN SOLUTION')[1].split('### END SOLUTION')[0].strip()
                    cls.solutions.append(solution_block)
        
        # Extract test blocks
        cls.tests = []
        for cell in cls.nb.cells:
            if cell.cell_type == 'code':
                source = cell.source
                if '### BEGIN TESTS' in source and '### END TESTS' in source:
                    solution_block = source.split('### BEGIN TESTS')[1].split('### END TESTS')[0].strip()
                    cls.tests.append(solution_block)

        for item in cls.tests: print(item, '\n-----------------\n')

    def test_check_for_changes(self):
        specific_text = 'person_instance = Person("Alice", 25)\nassert person_instance.name == "Alice"\nassert person_instance.age == 25'
        self.assertIn(specific_text, self.tests[0], "Changes detected in the first test block for Task 1")

        specific_text = 'person_instance = Person("Alice", 25)\nassert person_instance.get_age() == 25'
        self.assertIn(specific_text, self.tests[1], "Changes detected in the second test block for Task 2")

        specific_text = '''animal_instance = Animal("Cat", "Meow")
dog_instance = Dog("Buddy", "Woof", "Golden Retriever")

# Check Animal class attributes and method
assert animal_instance.name == "Cat"
assert animal_instance.sound == "Meow"
assert callable(getattr(animal_instance, "make_sound", None))

# Check Dog class attributes and method
assert dog_instance.name == "Buddy"
assert dog_instance.sound == "Woof"
assert dog_instance.breed == "Golden Retriever"
assert callable(getattr(dog_instance, "make_sound", None))

# Check if make_sound() produces the expected output
assert_output = "The Cat says Meow."
assert_output_dog = "The Golden Retriever dog named Buddy says Woof."
assert_output_method = """The Cat says Meow.
The Golden Retriever dog named Buddy says Woof."""'''

        self.assertIn(specific_text, self.tests[2], "Changes detected in the second test block for Task 3")


    def test_task_one(self):
       exec(self.solutions[0], exec_globals)
       exec(self.tests[0], exec_globals)

    def test_task_two(self):
       exec(self.solutions[1], exec_globals)
       exec(self.tests[1], exec_globals)

    def test_task_three(self):  
         exec(self.solutions[2], exec_globals)
         exec(self.tests[2], exec_globals)

# Main function to run the extraction and tests
def main():
    global exec_globals  # Declare exec_globals as global to modify it
    notebook_path = 'OOPythonSelfStudy.ipynb'  # Path to your Jupyter Notebook
    code_cells = extract_code_cells(notebook_path)
    exec_globals = execute_code(code_cells)  # Execute the code cells and store the globals



if __name__ == "__main__":
    main()
    unittest.main()
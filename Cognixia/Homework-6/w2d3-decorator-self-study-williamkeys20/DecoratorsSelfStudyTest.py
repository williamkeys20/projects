'''
 This is a template script for extracting Python Notebook cells, executing, and testing the outputs
 Cells must be seperated into functions for each cell
 Global variables are assumed to exist and are extracted using the exec function
    - exec() function is used for the dynamic execution of Python programs 
    - local variables can optionally be extracted as well
Function names can be called directly in this file, but the editor will falsly mark it as an error.

Adjust test cases as needed
Adjust the notebook_path in the main function

'''

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
        with open('DecoratorsSelfStudy.ipynb', 'r', encoding='utf-8') as f:
            cls.nb = nbformat.read(f, as_version=4)
        
        # Extract solution blocks
        cls.solutions = []
        for cell in cls.nb.cells:
            if cell.cell_type == 'code':
                source = cell.source
                if '### BEGIN SOLUTION' in source and '### END SOLUTION' in source:
                    solution_block = source.split('### BEGIN SOLUTION')[1].split('### END SOLUTION')[0].strip()
                    cls.solutions.append(solution_block)
    
    
    def test_one_sum(self):
        global exec_globals  # Access the global variable
        self.assertEqual(exec_globals['sum'](5,7), 12, 'The sum function is not correctly defined')
        
    def test_two_square(self):
        global exec_globals  # Access the global variable
        self.assertEqual(exec_globals['square'](exec_globals['sum']), 9,'The nested square function is not correctly defined')

    def test_three_call_function(self):
        # Example test for the first solution block
        specific_text = "square(sum)"
        self.assertIn(specific_text, self.solutions[2], f"Text '{specific_text}' not found in solution block: {self.solutions[0]}")

    def test_four_call_function(self):
        # Example test for the first solution block
        specific_text = "def outer():\n  def inner():"
        self.assertIn(specific_text, self.solutions[3], f"Text '{specific_text}' not found in solution block: {self.solutions[0]}")

    def test_five_call_function_outer(self):
        # Example test for the first solution block
        specific_text = "outer()"
        self.assertIn(specific_text, self.solutions[4], f"Text '{specific_text}' not found in solution block: {self.solutions[0]}")

    def test_six_call_function_sum(self):
        # Example test for the first solution block
        specific_text = "sum"
        self.assertEqual(specific_text, self.solutions[5], f"Text '{specific_text}' not found in solution block: {self.solutions[0]}")

    def test_seven_maybe(self):
        # Example test for the first solution block
        self.assertEqual(exec_globals['maybe'](True)(), 'Yes','The maybe function is not correctly defined for True booleans')
        self.assertEqual(exec_globals['maybe'](False)(), 'No','The maybe function is not correctly defined for False booleans')

    def test_decorator(self):
        from datetime import datetime 
        date = str.upper(datetime.now().strftime("%A"))
        specific_text = f'HELLO, LADIES AND GENTLEMEN, IT IS {date}'
        self.assertEqual(exec_globals['weekday'](), specific_text, "The paperboy decorator or weekday function is not properly defined")


# Main function to run the extraction and tests
def main():
    global exec_globals  # Declare exec_globals as global to modify it
    notebook_path = 'DecoratorsSelfStudy.ipynb'  # Path to your Jupyter Notebook
    code_cells = extract_code_cells(notebook_path)
    exec_globals = execute_code(code_cells)  # Execute the code cells and store the globals


if __name__ == "__main__":
    main()
    unittest.main()
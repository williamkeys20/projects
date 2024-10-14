import nbformat
import unittest
from unittest.mock import patch
import sys
import io
from datetime import date

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
    def test_name_year_and_class(self):
        global exec_globals  # Access the global variable
        with patch('builtins.input', side_effect=['John Doe', '25', 'Warrior', 'Test Catchphrase']):
            captured_output = io.StringIO()
            sys.stdout = captured_output
            exec('CharacterCreation()', exec_globals)
            sys.stdout = sys.__stdout__  # Reset redirect
            output = captured_output.getvalue().strip()
            year = date.today().year - 25

        # Ensure the function modifies values correctly
        assert f"John doe, {year}, WARRIOR" in output, "Name, birth year, and class are not modified correctly"

    def test_catchphrase(self):
        global exec_globals  # Access the global variable
        with patch('builtins.input', side_effect=['John Doe', '25', 'Warrior', 'Test Catchphrase']):
            captured_output = io.StringIO()
            sys.stdout = captured_output
            exec('CharacterCreation()', exec_globals)
            sys.stdout = sys.__stdout__  # Reset redirect
            output = captured_output.getvalue().strip()

        # Ensure the function modifies values correctly
        assert "esarhphctaC tseT" in output, "Catchphrase is not reversed correctly"

    def test_whole_input(self):
        global exec_globals
        with patch('builtins.input', side_effect=['jeff', '108', 'knight', 'ArrE']):
            captured_output = io.StringIO()
            sys.stdout = captured_output
            exec('CharacterCreation()', exec_globals)
            sys.stdout = sys.__stdout__  # Reset redirect
            output = captured_output.getvalue().strip()
            year = date.today().year - 108

        # Ensure the function modifies values correctly
        assert f"Jeff, {year}, KNIGHT" in output, "Name, birth year, and class are not modified correctly"
        assert "ErrA" in output, "Catchphrase is not reversed correctly"

    def test_one_year_old(self):
        global exec_globals
        with patch('builtins.input', side_effect=['KAnA', '1', 'HEAler', 'HELP me!!']):
            captured_output = io.StringIO()
            sys.stdout = captured_output
            exec('CharacterCreation()', exec_globals)
            sys.stdout = sys.__stdout__  # Reset redirect
            output = captured_output.getvalue().strip()
            year = date.today().year - 1

        # Ensure the function modifies values correctly
        assert f"Kana, {year}, HEALER" in output, "Name, birth year, and class are not modified correctly"
        assert "!!em PLEH" in output, "Catchphrase is not reversed correctly"


# Main function to run the extraction and tests
def main():
    global exec_globals  # Declare exec_globals as global to modify it
    notebook_path = 'CharacterCreation.ipynb'  # Path to your Jupyter Notebook
    code_cells = extract_code_cells(notebook_path)
    exec_globals = execute_code(code_cells)  # Execute the code cells and store the globals


if __name__ == "__main__":
    main()
    unittest.main()
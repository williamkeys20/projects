import nbformat
import unittest
from unittest.mock import patch
import sys
import io


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
    def setUp(self):
        exec_globals["sample_city"] = [
        {'block': 0, 'name': 'Downtown', 'places': [{'name': 'Park'}, {'name': 'Cafe'}, {'name': 'Bookstore'}]},
        ]
        
    def test_display_current_location(self):
        global exec_globals  # Access the global variable
        with patch('sys.stdout'):
            captured_output = io.StringIO()
            sys.stdout = captured_output
            exec('display_current_location(sample_city, 0)', exec_globals)
            sys.stdout = sys.__stdout__  # Reset redirect
            output = captured_output.getvalue().strip()
        assert output == "Current Location: Downtown\nAvailable places:\nPark\nCafe\nBookstore"

    def test_character_creation(self):
        global exec_globals  # Access the global variable
        char = exec_globals['initialize_character']()
        assert char == {'energy': 50, 'money': 0, 'inventory': []}

    def test_inventory(self):
        global exec_globals
        character = {'energy': 50, 'money': 0, 'inventory': []}
        exec_globals["add_to_inventory"](character, ['Frisbee', 'Sunscreen'])
        assert character['inventory'] == ['Frisbee', 'Sunscreen']

    def test_display_inventory(self):
        global exec_globals
        character = {'energy': 50, 'money': 0, 'inventory': ['Frisbee', 'Sunscreen']}
        with patch('sys.stdout'):
            captured_output = io.StringIO()
            sys.stdout = captured_output
            exec_globals['display_inventory'](character)
            sys.stdout = sys.__stdout__  # Reset redirect
            output = captured_output.getvalue().strip()
        assert output == "Current Inventory:\nFrisbee\nSunscreen"

    def test_explore_location(self):
        global exec_globals
        character = {'energy': 50, 'money': 0, 'inventory': []}
        current_block = {'block': 0, 'name': 'Downtown', 'places': [{'name': 'Park', 'items': ['Frisbee'], 'money': 10}]}
        
        with patch('builtins.input', side_effect=['Y']):
            captured_output = io.StringIO()
            sys.stdout = captured_output
            exec_globals['explore_location'](character, current_block)
            sys.stdout = sys.__stdout__  # Reset redirect


        assert character['inventory'] == ['Frisbee']
        assert character['money'] == 10
        assert current_block['places'][0]['items'] == []  # Check that items are removed from the location
        assert current_block['places'][0]['money'] == 0  # Check that money is subtracted from the location
        assert character['energy'] == 49  # Check that energy is decreased by the number of items taken


# Main function to run the extraction and tests
def main():
    global exec_globals  # Declare exec_globals as global to modify it
    notebook_path = 'CityExplorer.ipynb'  # Path to your Jupyter Notebook
    code_cells = extract_code_cells(notebook_path)
    exec_globals = execute_code(code_cells)  # Execute the code cells and store the globals


if __name__ == "__main__":
    main()
    unittest.main()

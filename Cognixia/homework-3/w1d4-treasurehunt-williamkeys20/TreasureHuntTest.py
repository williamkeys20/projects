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
class TestTreasureHuntGame(unittest.TestCase):
    def test_winning_path(self):
        global exec_globals  # Access the global variable
        choices = ["left", "right", "left", "right", "left", "right"]
        with patch('builtins.input', side_effect=choices):
            # Ensure play function is called within the exec_globals context
            exec("play()", exec_globals)
        # Now exec_globals contains updated values from the game execution
        self.assertEqual(exec_globals['player_score'], 150)  # Access variables through exec_globals
        self.assertEqual(exec_globals['player_health'], 160)

    def test_losing_path(self):
        global exec_globals  # Access the global variable
        choices = ["right", "left", "right", "left", "right", 'left', "right"]  # Adjust the number of steps as needed
        with patch('builtins.input', side_effect=choices):
            exec("play()", exec_globals)
        self.assertEqual(exec_globals['player_score'], -60)  # Player should have 0 points
        self.assertEqual(exec_globals['player_health'], -20)  # Player health should reach 0

# Main function to run the extraction and tests
def main():
    global exec_globals  # Declare exec_globals as global to modify it
    notebook_path = 'TreasureHunt.ipynb'  # Path to your Jupyter Notebook
    code_cells = extract_code_cells(notebook_path)
    exec_globals = execute_code(code_cells)  # Execute the code cells and store the globals


if __name__ == "__main__":
    main()
    unittest.main()
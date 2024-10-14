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
    def test_purchase_potions(self):
        global exec_globals  # Access the global variable
        currency = 100
        inventory = {"Healing Potion": 0}
        user_input = "5"
        with patch('builtins.input', return_value=user_input):
            currency, inventory = exec_globals['purchase_potions'](currency, inventory)
        assert currency == 50
        assert inventory["Healing Potion"]== 5

    def test_purchase_potions_insufficient_funds(self):
        global exec_globals  # Access the global variable
        currency = 20
        inventory = {"Healing Potion": 0}
        user_input = "5"
        with patch('builtins.input', return_value=user_input):
            currency, inventory = exec_globals['purchase_potions'](currency, inventory)
        assert currency == 20
        assert inventory["Healing Potion"]== 0

    def test_purchase_potions_non_integer_quantity(self):
        global exec_globals
        currency = 100
        inventory = {"Healing Potion": 0}
        user_input = "abc"
        with patch('builtins.input', return_value=user_input):
            currency, inventory = exec_globals['purchase_potions'](currency, inventory)
        assert currency == 100
        assert inventory["Healing Potion"]== 0

    def test_sell_inventory_valid_sale(self):
        global exec_globals
        currency = 50
        inventory = {"Healing Potion": 10}
        user_input = "3"
        with patch('builtins.input', return_value=user_input):
            currency, inventory = exec_globals['sell_inventory'](currency, inventory)
        assert currency == 65
        assert inventory["Healing Potion"]== 7

    def test_sell_inventory_insufficient_potions(self):
        global exec_globals
        currency = 50
        inventory = {"Healing Potion": 2}
        user_input = "5"
        with patch('builtins.input', return_value=user_input):
            currency, inventory = exec_globals['sell_inventory'](currency, inventory)
        assert currency == 50
        assert inventory["Healing Potion"]== 2

    def test_sell_inventory_non_integer_quantity(self):
        global exec_globals
        currency = 50
        inventory = {"Healing Potion": 10}
        user_input = "abc"
        with patch('builtins.input', return_value=user_input):
            currency, inventory = exec_globals['sell_inventory'](currency, inventory)
        assert currency == 50
        assert inventory["Healing Potion"]== 10

    def test_sell_inventory_sell_zero_potions(self):
        currency = 50
        inventory = {"Healing Potion": 10}
        user_input = "0"
        with patch('builtins.input', return_value=user_input):
            currency, inventory = exec_globals['sell_inventory'](currency, inventory)
        assert currency == 50
        assert inventory["Healing Potion"]== 10


# Main function to run the extraction and tests
def main():
    global exec_globals  # Declare exec_globals as global to modify it
    notebook_path = 'HealingPotionShop.ipynb'  # Path to your Jupyter Notebook
    code_cells = extract_code_cells(notebook_path)
    exec_globals = execute_code(code_cells)  # Execute the code cells and store the globals


if __name__ == "__main__":
    main()
    unittest.main()
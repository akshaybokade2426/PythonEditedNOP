# In a file like Utilities/data_providers.py

from utils.excel_provider import ExcelDataProvider

# utils/data_providers.py (The Bridge)
# Purpose: This file contains the simple helper functions (get_all_test_data, get_filtered_test_data, etc.) that connect your "Engine" to Pytest's @pytest.mark.parametrize decorator.
# Analogy: This is the car's transmission and accelerator pedal—it controls how the engine's power is delivered to the tests.
def get_all_test_data(workbook_name, sheet_name):
    """
    Uses the ExcelDataProvider to fetch all rows from a sheet for parametrization.
    """
    try:
        # Assumes your Excel file is in a folder named 'test_data' at the project root
        provider = ExcelDataProvider(workbook_name, data_folder="test_data")
        return provider.get_all_data(sheet_name)
    except FileNotFoundError:
        print(f"Warning: Data file not found at expected path. Parametrization will be empty.")
        return [] # Return an empty list to prevent crashes


# Add this function to Utilities/data_providers.py

def get_filtered_test_data(workbook_name, sheet_name, filter_column, filter_value):
    """
    Uses the ExcelDataProvider to fetch rows from a sheet that match a specific
    filter condition (e.g., WHERE TESTCASE_ID = 'TC_001').
    """
    try:
        provider = ExcelDataProvider(workbook_name, data_folder="test_data")
        return provider.get_data_by_key_value(sheet_name, filter_column, filter_value)
    except FileNotFoundError:
        print(f"Warning: Data file not found. Parametrization will be empty.")
        return []
from config import iot23_attacks_dir, iot23_combined_data_dir
from src.experiments import iot23_config, data_combinations
from src.helpers.data_helper import run_data_combinations
from src.helpers.log_helper import add_logger

# Add Logger
add_logger(file_name='02_data_combinations.log')

# Make combinations
source_files_dir = iot23_attacks_dir
output_files_dir = iot23_combined_data_dir
combinations = [
    data_combinations['Combination_1'],
    data_combinations['Combination_2'],
]
run_data_combinations(source_files_dir,
                      output_files_dir,
                      iot23_config["file_header"],
                      data_combinations=combinations,
                      overwrite=False)

print('Step 02: The end.')

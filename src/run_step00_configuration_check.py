from config import iot23_scenarios_dir, iot23_attacks_dir, iot23_experiments_dir
from src.experiments import iot23_config
from src.helpers.config_helper import check_config
from src.helpers.log_helper import add_logger

# Add Logger
add_logger(file_name='00_config_check.log')

# Check Config
scenarios_location = iot23_scenarios_dir
file_name_pattern = iot23_config['file_name_pattern']
attack_files_location = iot23_attacks_dir
experiments_location = iot23_experiments_dir
check_config(scenarios_location,
             file_name_pattern,
             attack_files_location,
             experiments_location)

print('Step 00: The End')

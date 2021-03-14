import logging

# Set logging
from config import iot23_attacks_dir, iot23_scenarios_dir
from src.experiments import iot23_config
from src.helpers.experiment_helper import split_scenarios_by_attack_type
from src.helpers.file_helper import delete_dir_content

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S', handlers=[
        logging.FileHandler("..\logs\exp_exec.log"),
        logging.StreamHandler()
    ])

# Delete existing files in target dir
output_dir = iot23_attacks_dir
delete_dir_content(output_dir)

# Split scenarios content
source_dir = iot23_scenarios_dir
file_name_pattern = iot23_config['file_name_pattern']
header_line = iot23_config['file_header']
split_scenarios_by_attack_type(source_dir,
                               file_name_pattern,
                               output_dir,
                               header_line)

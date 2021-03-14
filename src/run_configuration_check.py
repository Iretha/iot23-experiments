import os

import logging

from config import iot23_scenarios_dir, iot23_attacks_dir, iot23_experiments_dir
from src.experiments import iot23_config
from src.helpers.file_helper import find_files_recursively

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S', handlers=[
        logging.FileHandler("..\logs\\validation.log"),
        logging.StreamHandler()
    ])


def check_config(scenarios_dir, scenario_file_name_pattern, attack_files_dir, experiments_dir):
    # Validate scenarios home_dir
    valid_scenarios_dir = os.path.exists(scenarios_dir)
    if not valid_scenarios_dir:
        logging.error("Please, go to config.py and make sure that path to scenarios exists.")
    else:
        # Validate scenario files
        scenario_files = find_files_recursively(scenarios_dir, scenario_file_name_pattern)
        valid_scenarios_content = len(scenario_files) > 0
        if not valid_scenarios_content:
            logging.error("Scenarios dir is empty: " + scenarios_dir +
                          "\nPlease download IoT23 dataset and copy the content of iot23_small "
                          "to iot23_scenarios_dir or config scenarios_dir to point to iot23_small")

    # Validate attack files home_dir
    valid_attack_files_dir = os.path.exists(attack_files_dir)
    if not valid_attack_files_dir:
        logging.error("Please, make sure that attack files dir exists: " + attack_files_dir +
                      " or go to config.py and setup another one.")

    # Validate experiments home_dir
    valid_experiments_dir = os.path.exists(experiments_dir)
    if not valid_experiments_dir:
        logging.error("Please, make sure that experiments dir exists: " + experiments_dir +
                      " or go to config.py and setup another one.")

    if valid_scenarios_dir \
            and valid_scenarios_content \
            and valid_attack_files_dir \
            and valid_experiments_dir:
        logging.info("Validation is successful. You may proceed with the next step (scenarios data extraction).")
    else:
        logging.error("Please, fix the above errors in order to proceed further. ")



scenarios_location = iot23_scenarios_dir
file_name_pattern = iot23_config['file_name_pattern']
attack_files_location = iot23_attacks_dir
experiments_location = iot23_experiments_dir
check_config(scenarios_location, file_name_pattern, attack_files_location, experiments_location)

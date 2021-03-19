import logging
from config import iot23_experiments_dir
from src.experiments import data_combinations, feature_combinations
from src.helpers.log_helper import add_logger
from src.helpers.st5_exp_stats import explore_experiments_results

add_logger(file_name='06_explore_exp_results.log')
logging.warning("!!! This step takes about 3 min to complete !!!")

# Explore data
exp_home_dir = iot23_experiments_dir
data_combinations = [
    data_combinations['FL04_R_100_000'],  # 30 sec
    # data_combinations['FL16_R_100_000'],  # 30 sec

    # data_combinations['FL04_R_5_000_000'],   # 10 min
    # data_combinations['FL16_R_5_000_000'],   # 10 min
]

# Selected Features
feature_combos = [
    feature_combinations['F14'],
]

explore_experiments_results(exp_home_dir,
                            data_combinations,
                            feature_combos,
                            export_score_tables=True,
                            export_score_charts=True)

print('Step 06: The end.')

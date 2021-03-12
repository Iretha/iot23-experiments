import logging
import os

from config import iot23_experiments_dir
from src.experiments import experiment_definitions, iot23_config
from src.helpers.data_helper import fmt_num
from src.helpers.model_helper import score_trained_models


def score_experiment_models(experiment_definition_name, rows, model_names):
    experiment_name = experiment_definition_name + fmt_num(rows)
    experiment_dir = iot23_experiments_dir + experiment_name + "\\"

    # Check experiment files
    is_empty = not os.path.exists(experiment_dir) or len(os.listdir(experiment_dir)) == 0
    if is_empty:
        logging.error("--- Experiment folder is empty. ---")
        return

    # Score models
    experiment = experiment_definitions[experiment_definition_name]
    data_file_path = experiment_dir + "data\\" + experiment["clean_data"]["output_file_name"]
    model_dir = experiment_dir + "models\\"
    classification_col = iot23_config["classification_col"]
    score_trained_models(data_file_path, model_names, classification_col, model_dir, prefix=experiment_name)


def score_experiments_models(exp_dict, model_names):
    experiments = exp_dict.keys()
    for exp_definition in experiments:
        iterations = exp_dict[exp_definition]
        for rows_per_it in iterations:
            score_experiment_models(exp_definition, rows_per_it, model_names)

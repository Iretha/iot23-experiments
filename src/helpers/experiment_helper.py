import logging
import time
from config import iot23_attacks_dir, iot23_experiments_dir
from src.experiments import experiment_definitions, iot23_config
from src.helpers.file_helper import combine_files, shuffle_file_content, mk_dir
from src.helpers.data_helper import clean_data_in_file, split_into_train_and_test, fmt_num, select_features
from src.helpers.model_helper import create_models


def run_experiments(experiments, rows_per_attack, algorithms, override=False):
    for exp_definition in experiments:
        for rows_per_it in rows_per_attack:
            run_experiment(exp_definition, rows_per_it, algorithms, override=override)


def run_experiment(experiment_definition_name, rows_per_attack, algorithms, override=False):
    experiment_name = experiment_definition_name + fmt_num(rows_per_attack)
    logging.info("===== Start experiment: " + experiment_name)
    start_time = time.time()

    experiment_definition = experiment_definitions[experiment_definition_name]
    combined_file_name = experiment_definition['config']['combined_file_name']

    # Make experiment directory
    experiment_dir = iot23_experiments_dir + experiment_name
    data_dir = experiment_dir + "\\data\\"
    mk_dir(data_dir)

    # Combine rows from multiple files
    file_header = iot23_config["file_header"]
    combine_files(iot23_attacks_dir,
                  experiment_definition["attack_files"],
                  data_dir,
                  combined_file_name,
                  header_line=file_header,
                  max_rows_from_file=rows_per_attack,
                  skip_rows=1)

    # Select features
    select_features(data_dir, combined_file_name, experiment_definition)

    # Shuffle rows
    shuffle_file_content(data_dir, combined_file_name)

    # Clean data
    output_data_file_name = experiment_definition['config']['output_file_name']
    clean_data_in_file(data_dir,
                       combined_file_name,
                       data_dir,
                       output_data_file_name,
                       experiment_definition)

    # Split data
    split_into_train_and_test(data_dir + output_data_file_name)

    # Make models dir
    model_dir = experiment_dir + "\\models\\"
    mk_dir(model_dir)

    # Train models
    classification_col = experiment_definition["config"]["classification_col"]
    data_file_path = data_dir + output_data_file_name
    create_models(data_file_path, algorithms, classification_col, model_dir, override=override)

    # Score models
    # score_experiment_models(experiment_definition_name, experiment_name, algorithms)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("===== Experiment " + experiment_name + " finished in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))

import logging
import time

from src.experiments import experiment_definitions, iot23_config, format_line
from src.helpers.file_helper import combine_files, shuffle_file_content, mk_dir, find_files_recursively, filter_out_files_larger_than, is_not_comment, get_col_value
from src.helpers.data_helper import clean_data, split_into_train_and_test, fmt_num, select_features
from src.helpers.model_helper import create_models


def run_experiments(experiments_dir,
                    attack_files_dir,
                    experiments,
                    rows_per_attack,
                    algorithms,
                    prepare_data=False,
                    override=False):
    for exp_definition in experiments:
        for rows_per_it in rows_per_attack:
            run_experiment(experiments_dir,
                           attack_files_dir,
                           exp_definition,
                           rows_per_it,
                           algorithms,
                           prepare_data=prepare_data,
                           override=override)
    logging.info("Experiment folders are in " + experiments_dir)


def run_experiment(experiments_dir,
                   attack_files_dir,
                   experiment_definition_name,
                   rows_per_attack,
                   algorithms,
                   prepare_data=False,
                   override=False):
    experiment_name = experiment_definition_name + fmt_num(rows_per_attack)
    logging.info("===== Start experiment: " + experiment_name)
    start_time = time.time()

    # Make experiment directory if not exists
    experiment_dir = experiments_dir + experiment_name
    data_dir = experiment_dir + "\\data\\"
    mk_dir(data_dir)

    # Preprocess data
    experiment_definition = experiment_definitions[experiment_definition_name]
    combined_file_name = experiment_definition['config']['combined_file_name']
    output_data_file_name = experiment_definition['config']['output_file_name']
    preprocess_data(attack_files_dir,
                    experiment_definition,
                    rows_per_attack,
                    data_dir,
                    combined_file_name,
                    output_data_file_name, prepare_data=prepare_data)

    # Make models dir
    model_dir = experiment_dir + "\\models\\"
    mk_dir(model_dir)

    # Train models
    classification_col = experiment_definition["config"]["classification_col"]
    data_file_path = data_dir + output_data_file_name
    create_models(data_file_path, algorithms, classification_col, model_dir, override=override)
    logging.info("****** Experiment models are in " + model_dir)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("===== Experiment " + experiment_name + " finished in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


def preprocess_data(attack_files_dir,
                    experiment_definition,
                    rows_per_attack,
                    data_dir,
                    combined_file_name,
                    output_data_file_name,
                    prepare_data=False):
    if not prepare_data:
        return

    # Combine slices from files
    combine_files(attack_files_dir,
                  experiment_definition["attack_files"],
                  data_dir,
                  combined_file_name,
                  header_line=iot23_config["file_header"],
                  max_rows_from_file=rows_per_attack,
                  skip_rows=1)

    # Select features
    select_features(data_dir, combined_file_name, experiment_definition)

    # Shuffle rows
    shuffle_file_content(data_dir, combined_file_name)

    # Clean data
    clean_data(data_dir,
               combined_file_name,
               data_dir,
               output_data_file_name,
               experiment_definition)

    # Split data
    split_into_train_and_test(data_dir + output_data_file_name)
    logging.info("****** Experiment data files are in " + data_dir)



def list_experiment_names(experiment_def_names, rows_per_attack):
    experiment_names = []
    for exp_def_name in experiment_def_names:
        for it in rows_per_attack:
            experiment_name = exp_def_name + fmt_num(it)
            experiment_names.append(experiment_name)
    return experiment_names

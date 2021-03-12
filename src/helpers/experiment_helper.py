import logging
import time
from config import iot23_attacks_dir, iot23_experiments_dir
from src.experiments import experiment_definitions, iot23_config, iot23_category_encodings
from src.helpers.file_helper import combine_files, shuffle_file_content, mk_dir
from src.helpers.data_helper import clean_data_in_file, split_into_train_and_test, fmt_num
from src.helpers.model_helper import create_models, score_models, score_trained_models


def run_experiment(experiment_definition_name, rows_per_attack, algorithms, override=False):
    experiment_name = experiment_definition_name + fmt_num(rows_per_attack)
    logging.info("===== Start experiment: " + experiment_name)
    start_time = time.time()

    experiment = experiment_definitions[experiment_definition_name]
    attack_source_files = experiment["prepare_data"]["attack_files"]
    combined_file_name = experiment["prepare_data"]["output_file_name"]

    # Make experiment directory
    experiment_dir = iot23_experiments_dir + experiment_name
    data_dir = experiment_dir + "\\data\\"
    mk_dir(data_dir)

    # Combine rows from multiple attack files
    file_header = iot23_config["file_header"]
    combine_files(iot23_attacks_dir,
                  attack_source_files,
                  data_dir,
                  combined_file_name,
                  header_line=file_header,
                  max_rows_from_file=rows_per_attack,
                  skip_rows=1)

    # Shuffle rows
    shuffle_file_content(data_dir, combined_file_name)

    # Clean data
    cat_encoding = iot23_category_encodings
    drop_columns = experiment["clean_data"]["drop_columns"]
    replace_values = experiment["clean_data"]["replace_values"]
    replace_values_in_col = experiment["clean_data"]["replace_values_in_col"]
    numeric_columns = experiment["clean_data"]["transform_to_numeric"]
    clean_data_file_name = experiment["clean_data"]["output_file_name"]
    clean_data_in_file(data_dir,
                       combined_file_name,
                       data_dir,
                       clean_data_file_name,
                       drop_cols=drop_columns,
                       category_encoding=cat_encoding,
                       replace_values=replace_values,
                       replace_values_in_col=replace_values_in_col,
                       transform_to_numeric=numeric_columns)

    # Split data
    split_into_train_and_test(data_dir + clean_data_file_name)

    # Make models dir
    model_dir = experiment_dir + "\\models\\"
    mk_dir(model_dir)

    # Train models
    classification_col = iot23_config["classification_col"]
    data_file_path = data_dir + clean_data_file_name
    create_models(data_file_path, algorithms, classification_col, model_dir, override=override)

    # Score models
    # score_experiment_models(experiment_definition_name, experiment_name, algorithms)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("===== Experiment " + experiment_name + " finished in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


def run_experiments(exp_definitions, algorithms, override=False):
    experiments = exp_definitions.keys()
    for exp_definition in experiments:
        iterations = exp_definitions[exp_definition]
        for rows_per_it in iterations:
            run_experiment(exp_definition, rows_per_it, algorithms, override=override)

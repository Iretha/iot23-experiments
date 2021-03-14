import logging
import time
from src.experiments import experiment_definitions, iot23_config
from src.helpers.file_helper import combine_files, shuffle_file_content, mk_dir, find_files_recursively, filter_out_files_larger_than, is_not_comment, get_col_value
from src.helpers.data_helper import clean_data_in_file, split_into_train_and_test, fmt_num, select_features
from src.helpers.model_helper import create_models


def run_experiments(experiments_dir, attack_files_dir, experiments, rows_per_attack, algorithms, override=False):
    for exp_definition in experiments:
        for rows_per_it in rows_per_attack:
            run_experiment(experiments_dir, attack_files_dir, exp_definition, rows_per_it, algorithms, override=override)


def run_experiment(experiments_dir, attack_files_dir, experiment_definition_name, rows_per_attack, algorithms, override=False):
    experiment_name = experiment_definition_name + fmt_num(rows_per_attack)
    logging.info("===== Start experiment: " + experiment_name)
    start_time = time.time()

    experiment_definition = experiment_definitions[experiment_definition_name]
    combined_file_name = experiment_definition['config']['combined_file_name']

    # Make experiment directory
    experiment_dir = experiments_dir + experiment_name
    data_dir = experiment_dir + "\\data\\"
    mk_dir(data_dir)

    # Combine rows from multiple files
    file_header = iot23_config["file_header"]
    combine_files(attack_files_dir,
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


def split_scenarios_by_attack_type(dataset_location,
                                   file_name_pattern,
                                   output_dir,
                                   header_line,
                                   column_index=22,
                                   sep='\s+',
                                   max_size_in_mb=None):
    logging.info("--> Start splitting file . . . ")
    start_time = time.time()

    source_files = find_files_recursively(dataset_location, file_name_pattern)
    source_files = filter_out_files_larger_than(source_files, max_size_in_mb=max_size_in_mb)
    logging.info(str(len(source_files)) + " files to process ")

    map_key_values = {'-': 'Benign'}
    file_counter = 0
    file_cache = {}
    for file_path in source_files:
        file_counter += 1
        logging.info(str(file_counter) + '. Start processing file: ' + file_path)
        file_start_time = time.time()
        with open(file_path, "r") as source_file:
            for line in source_file:
                if is_not_comment(line):
                    value = get_col_value(line, sep, column_index, map_key_values=map_key_values)
                    output_file_exists = True if value in file_cache else False
                    if output_file_exists:
                        target_file = file_cache[value]
                    else:
                        output_file = output_dir + value + '.csv'
                        target_file = open(output_file, "a+")
                        target_file.write(header_line)
                        file_cache[value] = target_file
                    target_file.write(line)
        file_end_time = time.time()
        logging.info('End processing file in %s seconds = %s minutes...' % (
            (file_end_time - file_start_time), ((file_end_time - file_start_time) / 60)))

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("---> END in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


def list_experiment_names(experiment_def_names, rows_per_attack):
    experiment_names = []
    for exp_def_name in experiment_def_names:
        for it in rows_per_attack:
            experiment_name = exp_def_name + fmt_num(it)
            experiment_names.append(experiment_name)
    return experiment_names

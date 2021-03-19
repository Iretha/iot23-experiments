import logging
import time
from os import path

from sklearn.model_selection import train_test_split

from src.helpers.dataframe_helper import df_get, df_transform_to_numeric, save_to_csv, df_encode_objects, write_to_csv
from src.helpers.file_helper import overwrite_existing_file, mk_dir, combine_files, shuffle_file_content
from src.helpers.log_helper import log_duration


def run_data_combinations(sources_dir,
                          output_dir,
                          header_line,
                          data_combinations=[],
                          overwrite=False):
    logging.info("-----> Start data extraction for  . . . " + str(data_combinations))
    start_time = time.time()

    mk_dir(output_dir)

    for data_combination in data_combinations:
        source_files = data_combination["files"]
        output_file_name = data_combination["output_file_name"]
        max_rows = data_combination["max_rows_per_file"]

        exists = path.exists(output_dir + output_file_name)
        if overwrite is True or not exists:
            # Combine slices from files
            combine_files(sources_dir,
                          source_files,
                          output_dir,
                          output_file_name,
                          header_line=header_line,
                          max_rows_from_file=max_rows,
                          skip_rows=1)

            # Shuffle content
            shuffle_file_content(output_dir, output_file_name)
        else:
            logging.info("Data file " + output_file_name + " exists, skipping call...")
    log_duration(start_time, '-----> Data extraction finished in')


def select_features(data_dir, data_file_name, experiment_definition, delimiter='\s+'):
    logging.info("-----> Selecting features . . . ")
    start_time = time.time()

    # Check definition
    selected_features = experiment_definition["features"]
    if selected_features is None or len(selected_features) == 0:
        return  # Select all

    # Load dataframe
    data_file_path = data_dir + data_file_name
    dataframe = df_get(data_file_path, delimiter=delimiter)

    # Select features
    dataframe = dataframe[selected_features]

    # Save file
    output_file_name = data_file_name + '_tmp.csv'
    save_to_csv(dataframe, data_dir, output_file_name, append=False)

    # Overwrite previous file
    output_file_path = data_dir + output_file_name
    overwrite_existing_file(data_file_path, output_file_path)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("-----> Features selected in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


def clean_data(source_dir,
               source_file,
               output_dir,
               output_file,
               experiment_definition,
               delimiter=','):
    logging.info("-----> Clean data... ")
    start_time = time.time()

    # Load dataframe
    source_file_path = source_dir + source_file
    dataframe = df_get(source_file_path, delimiter=delimiter)
    df_columns = list(dataframe.columns)

    # Replace values in specific columns
    replace_values_in_col = filter_dict(df_columns,
                                        experiment_definition['config']["replace_values_in_col"])
    if len(replace_values_in_col) > 0:
        logging.info('Replace col values: ' + str(replace_values_in_col))
        dataframe.replace(replace_values_in_col, inplace=True)

    # Replace values in dataframe
    replace_values = experiment_definition['config']["replace_values"]
    if len(replace_values) > 0:
        logging.info('Replace df values: ' + str(replace_values))
        dataframe.replace(replace_values, inplace=True)

    # Encode String Categorical Values
    category_encoding = experiment_definition['config']["category_encodings"]
    if len(category_encoding) > 0:
        logging.info('Replace cat values: ' + str(category_encoding))
        dataframe.replace(category_encoding, inplace=True)

    # Convert to numeric (if possible)
    transform_to_numeric = filter_list(df_columns, experiment_definition['config']["transform_to_numeric"])
    if len(transform_to_numeric) > 0:
        df_transform_to_numeric(dataframe, transform_to_numeric)

    # Encode what is left
    df_encode_objects(dataframe)

    # Save cleaned data to a file
    save_to_csv(dataframe, output_dir, output_file, append=False)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("-----> Cleaning finished in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


def filter_dict(keys, dict_data):
    filtered_data = {}
    for data_key in dict_data.keys():
        if data_key in keys:
            filtered_data[data_key] = dict_data[data_key]
    return filtered_data


def filter_list(values, list_data):
    filtered_data = []
    for col in list_data:
        if col in values:
            filtered_data.append(col)
    return filtered_data


def split_into_train_and_test(source_path, test_size=0.2):
    logging.info("-----> Split data... ")
    start_time = time.time()

    # 0. Load dataframe
    df = df_get(source_path, delimiter=',')

    # 1. Split Data
    train, test = train_test_split(df, test_size=test_size)

    # 2. Save Training Data
    file_path_train = source_path + '_train.csv'
    write_to_csv(train, file_path_train, mode='w')

    # 3. Save Test Data
    file_path_test = source_path + '_test.csv'
    write_to_csv(test, file_path_test, mode='w')

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("-----> Splitting data finished in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


def fmt_num(num):
    return f"{num:_}"

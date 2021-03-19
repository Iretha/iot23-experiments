import logging
import os

import time
from os import path
import pandas as pd
from sklearn.model_selection import train_test_split

from src.experiments import format_line, get_train_data_path, get_test_data_path
from src.helpers.dataframe_helper import df_get, df_transform_to_numeric, df_encode_objects, save_to_csv, write_to_csv
from src.helpers.file_helper import mk_dir, combine_files, shuffle_file_content
from src.helpers.log_helper import log_duration


def prepare_data(sources_dir,
                 output_dir,
                 header_line,
                 cleanup_conf,
                 data_combinations=[],
                 overwrite=False):
    logging.info("-----> Start data extraction for  . . . " + str(data_combinations))
    start_time = time.time()

    mk_dir(output_dir)

    for data_combination in data_combinations:
        source_files = data_combination["files"]
        combined_data_file_name = data_combination["combined_data_file_name"]
        clean_data_file_name = data_combination["clean_data_file_name"]
        max_rows = data_combination["max_rows_per_file"]

        exists = path.exists(output_dir + clean_data_file_name)
        if overwrite is True or not exists:
            # Combine slices from files
            combine_files(sources_dir,
                          source_files,
                          output_dir,
                          combined_data_file_name,
                          header_line=format_line(header_line),
                          max_rows_from_file=max_rows,
                          skip_rows=1)

            # Clean data
            clean_data(output_dir,
                       combined_data_file_name,
                       output_dir,
                       clean_data_file_name,
                       cleanup_conf,
                       delimiter=',')

            # Shuffle content
            shuffle_file_content(output_dir, clean_data_file_name)

        else:
            logging.info("Data file " + clean_data_file_name + " exists, skipping call...")
    log_duration(start_time, '-----> Data extraction finished in')


def clean_data(source_dir,
               source_file,
               output_dir,
               output_file,
               cleanup_conf,
               delimiter=','):
    logging.info("-----> Clean data... ")
    start_time = time.time()

    # Load dataframe
    source_file_path = source_dir + source_file
    dataframe = df_get(source_file_path, delimiter=delimiter)
    df_columns = list(dataframe.columns)
    selected_columns = [x for x in df_columns if x not in cleanup_conf['drop_cols']]
    dataframe = dataframe[selected_columns]

    pd.set_option('display.expand_frame_repr', False)
    logging.debug(dataframe.head(10))

    # Replace values in specific columns
    replace_values_in_col = filter_dict(selected_columns, cleanup_conf["replace_values_in_col"])
    if len(replace_values_in_col) > 0:
        logging.info('Replace col values: ' + str(replace_values_in_col))
        dataframe.replace(replace_values_in_col, inplace=True)

    # Encode String Categorical Values
    category_encoding = cleanup_conf["category_encodings"]
    if len(category_encoding) > 0:
        logging.info('Replace cat values: ' + str(category_encoding))
        dataframe.replace(category_encoding, inplace=True)

    # Replace values in dataframe
    replace_values = cleanup_conf["replace_values"]
    if len(replace_values) > 0:
        logging.info('Replace df values: ' + str(replace_values))
        dataframe.replace(replace_values, inplace=True)

    # Convert to numeric (if possible)
    transform_to_numeric = selected_columns
    if len(transform_to_numeric) > 0:
        df = df_transform_to_numeric(dataframe, transform_to_numeric)

    # Encode what is left
    df_encode_objects(dataframe)
    logging.debug(dataframe.head(10))

    # Save cleaned data to a file
    save_to_csv(dataframe, output_dir, output_file, append=False)

    log_duration(start_time, '-----> Cleaning finished in')


def split_into_train_and_test(source_dir, source_data_file, dest_dir, test_size=0.2, features=None, overwrite=False):
    file_path_train = get_train_data_path(dest_dir + source_data_file)
    file_path_test = get_test_data_path(dest_dir + source_data_file)

    if not os.path.exists(file_path_train) \
            or not os.path.exists(file_path_test) \
            or overwrite:

        logging.info("-----> Split data... ")
        start_time = time.time()

        # 0. Load dataframe
        df = df_get(source_dir + source_data_file, delimiter=',')

        # 1. Select features
        if features is not None:
            df = df[features]

        # 2. Split Data
        train, test = train_test_split(df, test_size=test_size)

        # 3. Save Training Data
        write_to_csv(train, file_path_train, mode='w')

        # 4. Save Test Data
        write_to_csv(test, file_path_test, mode='w')

        log_duration(start_time, '-----> Splitting data finished in')


def filter_dict(keys, dict_data):
    filtered_data = {}
    for data_key in dict_data.keys():
        if data_key in keys:
            filtered_data[data_key] = dict_data[data_key]
    return filtered_data

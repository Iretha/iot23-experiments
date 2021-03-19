import logging
import time
from src.helpers.dataframe_helper import df_get, save_to_csv
from src.helpers.file_helper import overwrite_existing_file
from src.helpers.log_helper import log_duration


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

    log_duration(start_time, '-----> -----> Features selected in')


def filter_list(values, list_data):
    filtered_data = []
    for col in list_data:
        if col in values:
            filtered_data.append(col)
    return filtered_data


def fmt_num(num):
    return f"{num:_}"

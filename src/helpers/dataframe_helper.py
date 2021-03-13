import logging
import pandas as pd
from os import path
import time

from sklearn.preprocessing import OrdinalEncoder, StandardScaler


def df_get(file_path, delimiter='\t', header=0):
    logging.info('Load data file: ' + file_path)
    return pd.read_csv(file_path, delimiter=delimiter, header=header)


def df_transform_to_numeric(df, columns=[]):
    if len(columns) == 0:
        columns = list(df.select_dtypes(include=['object']).columns)

    for column_name in columns:
        df[column_name] = pd.to_numeric(df[column_name], errors='ignore')

    logging.info('Transform columns to numeric: ' + ' ,'.join(columns))
    return df


def df_encode_objects(df):
    ord_enc = OrdinalEncoder()
    obj_column_names = list(df.select_dtypes(include=['object']).columns)
    for obj_column_name in obj_column_names:
        df[obj_column_name] = ord_enc.fit_transform(df[[obj_column_name]])

    logging.info('Encode object columns: ' + ' ,'.join(obj_column_names))


# TODO two save-s
def save_to_csv(df, dest_dir, file_name, append=False):
    mode = 'w' if append is False else 'a'
    df.to_csv(dest_dir + file_name, index=False, mode=mode)
    logging.info('Save file: ' + file_name)


# TODO two save-s, use one
def write_to_csv(df, dest_file_path, mode='a'):
    add_header = False if (mode == 'a' and path.exists(dest_file_path)) else True
    df.to_csv(dest_file_path, mode=mode, header=add_header, index=False)
    logging.info('File saved: ' + dest_file_path)


def scale_data(x_train, x_test, scaler):
    logging.info("-----> Scale data . . . ")
    start_time = time.time()

    scaler.fit(x_train)
    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("-----> Data scaled in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))
    return x_train, x_test


def load_data_into_frame(data_file_path, classification_col_name, columns=[]):
    # logging.info('Loading df from ' + data_file_path)
    df = df_get(data_file_path, delimiter=',')

    if len(columns) == 0:
        columns = list(df.columns)

    selected_features = [x for x in columns if x not in [classification_col_name]]
    y = df[classification_col_name]
    x = df[selected_features]
    return x, y


def load_data(file_path, classification_col_name, features=[], scale=True):
    logging.info("-----> Load data ")
    start_time = time.time()

    # Load data
    x_train, y_train = load_data_into_frame(file_path + '_train.csv', classification_col_name, columns=features)
    x_test, y_test = load_data_into_frame(file_path + '_test.csv', classification_col_name, columns=features)

    # Scale data
    if scale:
        x_train, x_test = scale_data(x_train, x_test, StandardScaler())

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("-----> Data loaded in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))
    return x_train, y_train, x_test, y_test

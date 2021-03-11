import logging
import time

from sklearn.model_selection import train_test_split

from src.helpers.dataframe_helper import df_get, df_drop_cols, df_transform_to_numeric, save_to_csv, df_encode_objects, write_to_csv


def clean_data_in_file(source_dir,
                       source_file,
                       output_dir,
                       output_file,
                       delimiter='\s+',
                       drop_cols=[],
                       category_encoding={},
                       replace_values={},
                       replace_values_in_col={},
                       transform_to_numeric=[]):
    logging.info("-----> Clean data... ")
    start_time = time.time()

    source_file_path = source_dir + source_file

    # 0. Load dataframe
    dataframe = df_get(source_file_path, delimiter=delimiter)

    # 1. Delete columns by name
    if len(drop_cols) > 0:
        df_drop_cols(dataframe, drop_cols)

    # 2. Replace values in specific columns
    if len(replace_values_in_col) > 0:
        logging.info('Replace col values: ' + str(replace_values_in_col))
        dataframe.replace(replace_values_in_col, inplace=True)

    # 3. Replace values in dataframe
    if len(replace_values) > 0:
        logging.info('Replace df values: ' + str(replace_values))
        dataframe.replace(replace_values, inplace=True)

    # 4. Encode String Categorical Values
    if len(category_encoding) > 0:
        logging.info('Replace cat values: ' + str(category_encoding))
        dataframe.replace(category_encoding, inplace=True)

    # 5. Convert to numeric if possible
    if len(transform_to_numeric) > 0:
        df_transform_to_numeric(dataframe, transform_to_numeric)

    # 6. Encode what is left
    df_encode_objects(dataframe)

    # 7. Save cleaned data to file
    save_to_csv(dataframe, output_dir, output_file, append=False)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("-----> Cleaning finished in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


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

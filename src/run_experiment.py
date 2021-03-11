import logging
import os
import time
import pandas as pd
import warnings

import sklearn
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.linear_model import Perceptron, LogisticRegression
from sklearn.naive_bayes import GaussianNB, MultinomialNB, CategoricalNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.tree import DecisionTreeClassifier

from config import iot23_attacks_dir, iot23_experiments_dir
from src.experiments import experiments, iot23_config, iot23_category_encodings
from src.helpers.files_helper import combine_files, shuffle_file_content, mk_dir
from src.helpers.data_helper import clean_data_in_file, split_into_train_and_test
from src.helpers.model_helper import create_models, score_models, score_trained_models

# Set logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

# Set python's max row display
pd.set_option('display.max_row', 1000)

# Set Python's max column width to 50
pd.set_option('display.max_columns', 50)

warnings.filterwarnings("ignore", category=sklearn.exceptions.UndefinedMetricWarning)


def run_experiment(experiment_name, algorithms):
    logging.info("===== Start experiment =====")
    start_time = time.time()

    experiment = experiments[experiment_name]
    attack_source_files = experiment["prepare_data"]["attack_files"]
    rows_per_attack = experiment["prepare_data"]["rows_per_attack"]
    combined_file_name = experiment["prepare_data"]["output_file_name"]

    # Make experiment directory
    experiment_dir = iot23_experiments_dir + experiment_name + "\\"
    mk_dir(experiment_dir)

    # Combine rows from multiple attack files
    file_header = iot23_config["file_header"]
    combine_files(iot23_attacks_dir,
                  attack_source_files,
                  experiment_dir,
                  combined_file_name,
                  header_line=file_header,
                  max_rows_from_file=rows_per_attack,
                  skip_rows=1)

    # Shuffle rows
    shuffle_file_content(experiment_dir, combined_file_name)

    # Clean data
    cat_encoding = iot23_category_encodings
    drop_columns = experiment["clean_data"]["drop_columns"]
    replace_values = experiment["clean_data"]["replace_values"]
    replace_values_in_col = experiment["clean_data"]["replace_values_in_col"]
    numeric_columns = experiment["clean_data"]["transform_to_numeric"]
    clean_data_file_name = experiment["clean_data"]["output_file_name"]
    clean_data_in_file(experiment_dir,
                       combined_file_name,
                       experiment_dir,
                       clean_data_file_name,
                       drop_cols=drop_columns,
                       category_encoding=cat_encoding,
                       replace_values=replace_values,
                       replace_values_in_col=replace_values_in_col,
                       transform_to_numeric=numeric_columns)

    # Split data
    split_into_train_and_test(experiment_dir + clean_data_file_name)

    # Train models
    classification_col = iot23_config["classification_col"]
    data_file_path = experiment_dir + clean_data_file_name
    create_models(data_file_path, algorithms, classification_col, experiment_dir)

    # Score models
    score_experiment_models(experiment_name, algorithms)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("===== Experiment finished in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


def score_experiment_models(experiment_name, algorithms):
    experiment_dir = iot23_experiments_dir + experiment_name + "\\"

    # Check experiment files
    is_empty = not os.path.exists(experiment_dir) or len(os.listdir(experiment_dir)) == 0
    if is_empty:
        logging.error("--- Experiment folder is empty. ---")
        return

    # Score models
    experiment = experiments[experiment_name]
    data_file_path = experiment_dir + experiment["clean_data"]["output_file_name"]
    classification_col = iot23_config["classification_col"]
    score_trained_models(data_file_path, algorithms, classification_col, experiment_dir)


training_algorithms = dict([
    ('GaussianNB', GaussianNB()),  # 1.327 sec
    ('Perceptron', Perceptron(eta0=0.2, max_iter=1000, tol=1e-3, verbose=0, early_stopping=True, validation_fraction=0.1)),  # 25.717 sec
    ('DecisionTree', DecisionTreeClassifier(random_state=0)),  # 17.019 sec
    ('RandomForest', RandomForestClassifier(random_state=0)),  # 6.318 min
    ('AdaBoost', AdaBoostClassifier(n_estimators=100, random_state=0)),  # 6.426 min
    ('MLPClassifier', MLPClassifier(alpha=1e-05, hidden_layer_sizes=(15,), random_state=1, solver='lbfgs')),  # 8.313 min
    ('LogisticRegression', LogisticRegression(solver='lbfgs', max_iter=1000)),  # 16.95 min
    ('GradientBoostingClassifier', GradientBoostingClassifier(random_state=0)),  # 37.039 min
    ('SVC_linear', LinearSVC()),  # 47.565 min
    ('KNeighborsClassifier', KNeighborsClassifier(n_neighbors=3)),  # 0.293 sec
    ('SVC_rbf', SVC(kernel='rbf')),  # idk
    ('SVC_poly', SVC(kernel='poly')),  # idk
])

run_experiment("experiment_04_x100", training_algorithms)
# score_experiment_models(experiment_key, training_algorithms)


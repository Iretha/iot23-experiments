import os

import logging

import pickle
import sys
import time

from src.experiments import get_exp_name, get_exp_data_dir, get_exp_models_dir, data_cleanup_conf, get_train_data_path
from src.helpers.dataframe_helper import load_data
from src.helpers.file_helper import mk_dir
from src.helpers.log_helper import log_duration
from src.helpers.st2_data_helper import split_into_train_and_test


def run_combinations(data_dir,
                     experiments_dir,
                     data_combinations_list,
                     feature_combinations_list,
                     training_algorithms,
                     test_size=0.2,
                     overwrite=False):
    for data_combination in data_combinations_list:
        for feature_combination in feature_combinations_list:
            run_combination(data_dir,
                            experiments_dir,
                            data_combination,
                            feature_combination,
                            training_algorithms,
                            test_size=test_size,
                            overwrite=overwrite)


def run_combination(data_dir,
                    experiments_dir,
                    data_combination,
                    feature_combination,
                    training_algorithms,
                    test_size=0.2,
                    overwrite=False):
    # Make experiment data dir
    experiment_name = get_exp_name(data_combination, feature_combination)
    experiment_data_dir = experiments_dir + get_exp_data_dir(experiment_name)
    mk_dir(experiment_data_dir)

    # Prepare experiment data
    data_file_name = data_combination['clean_data_file_name']
    split_into_train_and_test(data_dir,
                              data_file_name,
                              experiment_data_dir,
                              test_size=test_size,
                              features=feature_combination['features'],
                              overwrite=overwrite)
    logging.info("****** Experiment data is in " + experiment_data_dir)

    # Make experiment models dir
    experiment_models_dir = experiments_dir + get_exp_models_dir(experiment_name)
    mk_dir(experiment_models_dir)

    # Train models
    classification_col = data_cleanup_conf["classification_col"]
    train_data_file_path = experiment_data_dir + get_train_data_path(data_file_name)
    create_models(experiment_models_dir,
                  train_data_file_path,
                  classification_col,
                  training_algorithms,
                  overwrite=overwrite)
    logging.info("****** Experiment models are in " + experiment_models_dir)


def create_models(models_dir,
                  train_data_file_path,
                  classification_col,
                  algorithms,
                  overwrite=False):
    logging.info("-----> Train " + str(len(algorithms)) + " models : " + str(algorithms))
    start_time = time.time()

    # Load Data
    x_train, y_train = load_data(train_data_file_path, classification_col)

    # Train & Save Models
    for model_name in algorithms.keys():
        model_path = models_dir + model_name + '.pkl'
        exists = os.path.exists(model_path)

        if not exists or overwrite:
            trained_model = None

            # Train
            try:
                trained_model = train_model(model_name, algorithms[model_name], x_train, y_train)
            except:
                logging.error("Oops! Could not train with model " + model_name + " data=" + train_data_file_path, sys.exc_info()[0], " occurred.")

            # Save
            if trained_model is not None:
                try:
                    save_model(model_path, trained_model)
                except:
                    logging.error("Oops! Could not save model " + model_name + " in " + models_dir + '; ' + train_data_file_path, sys.exc_info()[0], " occurred.")
        else:
            logging.warning('^^^^^ Model ' + model_name + ' already exists! Skip training...')

    log_duration(start_time, '-----> Training of all models finished in')


def train_model(model_name, model, x_train, y_train):
    logging.info("=====> Train " + model_name + " . . .")
    start_time = time.time()

    model.fit(x_train, y_train)

    log_duration(start_time, "=====> Training of " + model_name + " finished in")
    return model


def save_model(model_path, model):
    # Save Model
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)

import pickle
import logging
import sys
import time

from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from src.helpers.dataframe_helper import load_data, scale_data


def save_trained_model(model, model_dir=None, model_name=None, model_name_suffix=None):
    if model_name is None:
        model_name = model.__class__.__name__

    model_path = model_name
    if model_dir is not None:
        model_path = model_dir + model_name

    if model_name_suffix is not None:
        model_path += model_name_suffix

    model_path += '.pkl'
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)

    logging.info('Model saved: ' + model_path)
    return model_path


def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)

    logging.info('Model loaded: ' + model_path)
    return model


def load_models(model_names, model_dir, ext='.pkl'):
    logging.info('------ Load ' + str(len(model_names)) + ' models ')

    trained_models = {}
    for model_name in model_names:
        trained_models[model_name] = load_model(model_dir + model_name + ext)
    return trained_models


def train_model(model, x_train, y_train):
    model_name = model.__class__.__name__
    start_time = time.time()

    logging.info("=====> Train " + model_name + " . . .")

    model.fit(x_train, y_train)

    exec_time_seconds = (time.time() - start_time)
    exec_time_minutes = exec_time_seconds / 60

    logging.info("=====> Training of " + model_name + " finished in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))
    return model


def train_models(models, x_train, y_train, model_dir=None):
    model_names = models.keys()
    trained_models = {}

    for model_name in model_names:
        model = train_model(models[model_name], x_train, y_train)
        save_trained_model(model, model_dir, model_name=model_name)
        trained_models[model_name] = model
    return trained_models


def score_models(models, x_test, y_test):
    for model_name in models.keys():
        score_model(model_name, models[model_name], x_test, y_test)


def score_model(model_name, model, x_test, y_test, labels=None, title=''):
    logging.info('======================= Predicting with: ' + model_name)

    start_time = time.time()
    predictions = model.predict(x_test)

    print_score(y_test, predictions)
    print_time("---> ---> Prediction time is", (time.time() - start_time))
    print_class_report(y_test, predictions)
    # plt_confusion_matrix(y_test, predictions, labels=labels, title=model_name + title)
    # plot_classification_report(cls_report)

    exec_time_seconds = (time.time() - start_time)
    exec_time_minutes = exec_time_seconds / 60

    logging.info("======================= Prediction ended in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


def print_time(msg, time_in_seconds):
    exec_time_minutes = time_in_seconds / 60
    logging.info(msg + " %s seconds = %s minutes ---" % (time_in_seconds, exec_time_minutes))


def print_score(y_test, predictions):
    logging.info("---> ---> Accuracy Score: " + str(accuracy_score(predictions, y_test)))


def print_class_report(y_test, predictions):
    cls_report = classification_report(y_test, predictions)
    logging.info("---> ---> Classification report: \n" + cls_report)


def create_models(file_path, models, classification_col_name, model_dir, features=[]):
    logging.info("-----> Train " + str(len(models)) + " models : " + str(models))
    start_time = time.time()

    # Load Data
    x_train, y_train, x_test, y_test = load_data(file_path, classification_col_name, features=features)
    logging.info("-----> -----> x= " + str(x_train.columns))

    # Scale data
    x_train, x_test = scale_data(x_train, x_test, StandardScaler())

    # Create Models
    try:
        train_models(models, x_train, y_train, model_dir=model_dir)
    except:
        logging.error("Oops!", sys.exc_info()[0], " occurred.")

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("-----> Training of all models finished in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


def score_trained_models(file_path, models, classification_col_name, model_dir, features=[]):
    logging.info("===== ===== ===== Score models ===== ===== =====")
    start_time = time.time()

    # Load Data
    x_train, y_train, x_test, y_test = load_data(file_path, classification_col_name, features=features)

    # Scale data
    x_train, x_test = scale_data(x_train, x_test, StandardScaler())

    # Load Models
    trained_models = load_models(models.keys(), model_dir)

    # Score models
    score_models(trained_models, x_test, y_test)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("===== ===== ===== Execution finished in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))

import os
import pickle
import logging
import sys
import time
from sklearn.inspection import permutation_importance

from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import MinMaxScaler

from src.experiments import get_train_data_path, get_test_data_path
from src.helpers.dataframe_helper import load_data


def save_trained_model(model, model_dir=None, model_name=None, model_name_suffix=None, scaler=None):
    if model_name is None:
        model_name = model.__class__.__name__

    model_path = calc_model_path(model_dir, model_name, model_name_suffix)

    # Save Model
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)

    # Save Scaler
    if scaler is not None:
        with open(model_path + '_sc.pkl', 'wb') as file:
            pickle.dump(model, file)

    logging.info('Model saved: ' + model_path)
    return model_path


def calc_model_path(model_dir=None, model_name=None, model_name_suffix=None, ext=".pkl"):
    model_path = model_name
    if model_dir is not None:
        model_path = model_dir + model_name

    if model_name_suffix is not None:
        model_path += model_name_suffix

    model_path += ext
    return model_path


def load_model(model_path):
    if os.path.exists(model_path):
        with open(model_path, 'rb') as file:
            model = pickle.load(file)

        logging.info('Model loaded: ' + model_path)
        return model
    return None


def load_models(model_names, model_dir, ext='.pkl'):
    logging.info('------ Load ' + str(len(model_names)) + ' models ')

    trained_models = {}
    for model_name in model_names:
        mdl = load_model(model_dir + model_name + ext)
        if mdl is not None:
            trained_models[model_name] = mdl
    return trained_models


def train_model(model_dir, model_name, model, x_train, y_train, save_model=False):
    logging.info("=====> Train " + model_name + " . . .")

    start_time = time.time()

    model.fit(x_train, y_train)

    exec_time_seconds = (time.time() - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("=====> Training of " + model_name + " finished in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))

    if save_model:
        try:
            save_trained_model(model, model_dir, model_name=model_name)
        except:
            logging.error("Oops! Could not save model " + model_name, sys.exc_info()[0], " occurred.")

    return model


def train_models(models, x_train, y_train, model_dir=None, override_model=False):
    model_names = models.keys()
    trained_models = {}

    for model_name in model_names:
        if model_not_exists(model_dir, model_name) or override_model:
            try:
                model = train_model(model_dir, model_name, models[model_name], x_train, y_train, save_model=True)
            except:
                logging.error("Oops! Could not finish training of " + model_name, sys.exc_info()[0], " occurred.")
            trained_models[model_name] = model
        else:
            logging.warning('Training skipped! Model ' + model_name + ' already exists!')
    return trained_models


def model_not_exists(model_dir, model_name, ext=".pkl"):
    model_path = calc_model_path(model_dir, model_name, ext=ext)
    return not os.path.exists(model_path)


def score_models(models, x_test, y_test, prefix=''):
    for model_name in models.keys():
        score_model(model_name, models[model_name], x_test, y_test, prefix=prefix)


def score_model(model_name, model, x_test, y_test, prefix='', labels=None, title=''):
    logging.info('======================= Predicting with: ' + model_name)

    adv_stats = {}

    start_time = time.time()
    # x_test = model.fit_transform(x_test)
    predictions = model.predict(x_test)

    pred_time_in_sec = time.time() - start_time
    adv_stats['Runtime (sec)'] = pred_time_in_sec
    adv_stats['Runtime (min)'] = "%0.2f" % ((pred_time_in_sec / 60),)
    print_time("---> ---> Prediction time is", pred_time_in_sec)

    extract_feature_importance(model_name, model, adv_stats)
    extract_permutation_importance(model_name, model, x_test, y_test, adv_stats)
    print_score(y_test, predictions)
    print_class_report(y_test, predictions)

    exec_time_seconds = (time.time() - start_time)
    exec_time_minutes = exec_time_seconds / 60

    logging.info("======================= Prediction ended in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))
    return y_test, predictions, adv_stats


def extract_feature_importance(model_name, model, adv_stats):
    feature_importance = None
    try:
        feature_importance = model.feature_importances_
    except:
        try:
            feature_importance = model.coef_[0]
        except:
            logging.error("Oops! Feat Importance could not be extracted for " + model_name)

    if feature_importance is not None:
        d = {i: v for i, v in enumerate(feature_importance)}
        logging.info('Feature Importance: ' + str(d))
        adv_stats['Feature Importance'] = d



def print_time(msg, time_in_seconds):
    exec_time_minutes = time_in_seconds / 60
    logging.info(msg + " %s seconds = %s minutes ---" % (time_in_seconds, exec_time_minutes))


def print_score(y_test, predictions):
    logging.info("---> ---> Accuracy Score: " + str(accuracy_score(predictions, y_test)))


def print_class_report(y_test, predictions):
    cls_report = classification_report(y_test, predictions)
    logging.debug("---> ---> Classification report: \n" + cls_report)


def create_models(file_path, models, classification_col_name, model_dir, features=[], override=False):
    logging.info("-----> Train " + str(len(models)) + " models : " + str(models))
    start_time = time.time()

    # Load Data
    x_train, y_train = load_data(get_train_data_path(file_path), classification_col_name, features=features)

    # Create Models
    try:
        train_models(models, x_train, y_train, model_dir=model_dir, override_model=override)
    except:
        logging.error("Oops!", sys.exc_info()[0], " occurred.")

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("-----> Training of all models finished in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


def score_trained_models(file_path, model_names, classification_col_name, model_dir, prefix='', features=[]):
    logging.info("===== ===== ===== Score models ===== ===== =====")
    start_time = time.time()

    # Load Data
    x_test, y_test = load_data(get_test_data_path(file_path), classification_col_name, features=features, scaler=MinMaxScaler())

    # Load Models
    trained_models = load_models(model_names, model_dir)

    # Score models
    score_models(trained_models, x_test, y_test, prefix=prefix)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("===== ===== ===== Execution finished in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))

import os

import glob

import ntpath

import pickle

import logging
import time

import psutil
import re

from sklearn.metrics import accuracy_score, classification_report

from src.experiments import get_exp_name, get_exp_models_dir, get_exp_results_dir, get_exp_data_dir, data_cleanup_conf, get_test_data_path
from src.helpers.dataframe_helper import load_data
from src.helpers.file_helper import mk_dir, write_json_file
from src.helpers.log_helper import log_duration
from src.helpers.stats_helper import plot_feature_importance, plot_confusion_ma3x_v2, plot_roc_curve_custom, plot_precision_recall_curve_custom
from src.helpers.xls_helper import export_stats_xls


def explore_experiments_results(exp_home_dir,
                                data_combinations,
                                feature_combinations,
                                export_score_tables=True,
                                export_score_charts=False):
    for data_combination in data_combinations:
        for feature_combination in feature_combinations:
            exp_name = get_exp_name(data_combination, feature_combination)
            explore_experiment_results(exp_home_dir,
                                       exp_name,
                                       data_combination['clean_data_file_name'],
                                       export_score_tables=export_score_tables,
                                       export_score_charts=export_score_charts)


def explore_experiment_results(exp_home_dir,
                               exp_name,
                               data_file_name,
                               export_score_tables=True,
                               export_score_charts=False):
    # Make results dir
    res_dir = exp_home_dir + get_exp_results_dir(exp_name)
    mk_dir(res_dir)

    # Load test data
    experiment_data_dir = exp_home_dir + get_exp_data_dir(exp_name)
    classification_col = data_cleanup_conf["classification_col"]
    test_data_file_path = experiment_data_dir + get_test_data_path(data_file_name)
    x_test, y_test = load_data(test_data_file_path, classification_col)

    # Export model stats
    exp_models_dir = get_exp_models_dir(exp_home_dir + exp_name)
    export_model_stats(exp_name,
                       exp_models_dir,
                       x_test,
                       y_test,
                       res_dir,
                       export_score_tables=export_score_tables,
                       export_score_charts=export_score_charts)


def export_model_stats(experiment_name,
                       models_location,
                       x_test,
                       y_test,
                       results_location,
                       export_score_tables=True,
                       export_score_charts=False):
    if not export_score_tables and not export_score_charts:
        return

    stats = {}
    model_stats = {}
    pid = os.getpid()
    p = psutil.Process(pid)
    # Score
    model_paths = glob.glob(models_location + "/*.pkl")
    for model_path in model_paths:
        model_name = ntpath.basename(model_path)
        model_name = re.findall(r'[^\/]+(?=\.)', model_name)[0]
        # print(p.memory_info())
        # print(p.cpu_percent(interval=1.0))
        model = load_model(model_path)
        if model is not None:
            # print(p.memory_info())
            # print(p.cpu_percent(interval=1.0))
            y_test, predictions, adv_stats = score_model(model_name,
                                                         model,
                                                         x_test,
                                                         y_test)

            model_stats[model_name] = prepare_model_stats(y_test,
                                                          predictions,
                                                          adv_stats,
                                                          export_score_tables=export_score_tables)

            export_model_chart_images(results_location,
                                      model_name, model,
                                      x_test,
                                      y_test,
                                      predictions,
                                      experiment_name,
                                      adv_stats,
                                      export_score_charts=export_score_charts)

    stats['model_stats'] = model_stats
    write_json_file(results_location + 'stats.json', stats)
    export_stats_xls(results_location,
                     {experiment_name: stats},
                     output_file_name=experiment_name + '.xlsx',
                     export_score_tables=export_score_tables)


def load_model(model_path):
    if os.path.exists(model_path):
        with open(model_path, 'rb') as file:
            model = pickle.load(file)

        logging.info('Model loaded: ' + model_path)
        return model
    return None


def score_model(model_name, model, x_test, y_test):
    logging.info('======================= Predicting with: ' + model_name)

    adv_stats = {}

    start_time = time.time()
    predictions = model.predict(x_test)

    pred_time_in_sec = time.time() - start_time
    adv_stats['Runtime (sec)'] = pred_time_in_sec
    adv_stats['Runtime (min)'] = "%0.2f" % ((pred_time_in_sec / 60),)

    log_duration(start_time, "---> ---> Prediction time of " + model_name + " is")

    load_feat_importance(model_name, model, adv_stats)
    log_score(model_name, y_test, predictions)
    log_class_report(model_name, y_test, predictions)

    return y_test, predictions, adv_stats


def load_feat_importance(model_name, model, adv_stats):
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
        logging.info('---> ---> Feature Importance of ' + model_name + ': ' + str(d))
        adv_stats['Feature Importance'] = d


def log_score(model_name, y_test, predictions):
    logging.info('---> ---> Accuracy Score of ' + model_name + ': ' + str(accuracy_score(predictions, y_test)))


def log_class_report(model_name, y_test, predictions):
    cls_report = classification_report(y_test, predictions)
    logging.debug("---> ---> Classification report of " + model_name + ": \n" + cls_report)


def prepare_model_stats(y_true, y_pred, adv_stats, export_score_tables=False):
    if not export_score_tables:
        return

    return {'classification_report': classification_report(y_true, y_pred, output_dict=True),
            'adv_stats': adv_stats}


def export_model_chart_images(results_location,
                              model_name,
                              model,
                              x_test,
                              y_test,
                              y_pred,
                              experiment_name,
                              adv_stats,
                              export_score_charts=False):
    if not export_score_charts:
        return

    if adv_stats is not None and 'Feature Importance' in adv_stats:
        feat_imp = adv_stats['Feature Importance']
        if feat_imp is not None:
            plot_feature_importance(results_location,
                                    model_name,
                                    experiment_name,
                                    feat_imp,
                                    title=experiment_name + "\n\n" + model_name + "\nFeature Importance",
                                    file_name=experiment_name + '_' + model_name + "_feat_imp.png")

    plot_confusion_ma3x_v2(results_location,
                           y_test,
                           y_pred,
                           experiment_name,
                           title=experiment_name + "\n\n" + model_name + "\nConfusion Matrix",
                           file_name=experiment_name + '_' + model_name + "_conf_m3x_v2.png")

    plot_roc_curve_custom(results_location,
                          model,
                          model_name,
                          x_test,
                          y_test,
                          experiment_name,
                          title=experiment_name + "\n\n" + model_name + "\nROC Curves",
                          file_name=experiment_name + '_' + model_name + "_roc_curve.png")

    plot_precision_recall_curve_custom(results_location,
                                       model,
                                       model_name,
                                       x_test,
                                       y_test,
                                       experiment_name,
                                       title=experiment_name + "\n\n" + model_name + "\nPrecision-Recall Curves",
                                       file_name=experiment_name + '_' + model_name + "_pr_recall_curve.png")

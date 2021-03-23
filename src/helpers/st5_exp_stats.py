import os
import glob
import ntpath
import pickle
import logging
import time
import psutil
import re

from sklearn.inspection import permutation_importance
from sklearn.metrics import accuracy_score, classification_report, f1_score, recall_score, precision_score, balanced_accuracy_score
from sklearn.pipeline import Pipeline

from src.experiments import get_exp_name, get_exp_models_dir, get_exp_results_dir, get_exp_data_dir, data_cleanup_conf, get_test_data_path
from src.helpers.dataframe_helper import load_data
from src.helpers.file_helper import mk_dir, write_json_file
from src.helpers.log_helper import log_duration
from src.helpers.stats_helper import plot_feature_importance, plot_confusion_ma3x, plot_model_precision_recall_curve, plot_model_roc_curve, plot_permutation_importance
from src.helpers.xls_helper import export_stats_xls


def explore_experiments_results(exp_home_dir,
                                data_combinations,
                                feature_combinations,
                                enable_score_tables=True,
                                enable_score_charts=False,
                                enable_model_insights=False):
    for data_combination in data_combinations:
        for feature_combination in feature_combinations:
            exp_name = get_exp_name(data_combination, feature_combination)
            explore_experiment_results(exp_home_dir,
                                       exp_name,
                                       data_combination['clean_data_file_name'],
                                       enable_score_tables=enable_score_tables,
                                       enable_score_charts=enable_score_charts,
                                       enable_model_insights=enable_model_insights)


def explore_experiment_results(exp_home_dir,
                               exp_name,
                               data_file_name,
                               enable_score_tables=True,
                               enable_score_charts=False,
                               enable_model_insights=False):
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
                       enable_score_tables=enable_score_tables,
                       enable_score_charts=enable_score_charts,
                       enable_model_insights=enable_model_insights)


def export_model_stats(experiment_name,
                       models_location,
                       x_test,
                       y_test,
                       results_location,
                       enable_score_tables=True,
                       enable_score_charts=False,
                       enable_model_insights=False):
    if not enable_score_tables and not enable_score_charts and not enable_model_insights:
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
            y_test, predictions, adv_stats, adv_insights = score_model(model_name,
                                                                       model,
                                                                       x_test,
                                                                       y_test,
                                                                       enable_model_insights=enable_model_insights)

            model_stats[model_name] = load_model_stats(y_test,
                                                       predictions,
                                                       adv_stats,
                                                       enable_score_tables=enable_score_tables)

            export_model_result_charts(results_location,
                                       model_name, model,
                                       x_test,
                                       y_test,
                                       predictions,
                                       experiment_name,
                                       adv_stats,
                                       enable_score_charts=enable_score_charts)

            export_model_insights(results_location,
                                  model_name, model,
                                  x_test,
                                  y_test,
                                  predictions,
                                  experiment_name,
                                  adv_insights,
                                  enable_model_insights=enable_model_insights)

    stats['model_stats'] = model_stats
    write_json_file(results_location + 'stats.json', stats)
    export_stats_xls(results_location,
                     {experiment_name: stats},
                     output_file_name=experiment_name + '.xlsx',
                     enable_score_tables=enable_score_tables)


def export_model_result_charts(results_location,
                               model_name,
                               model,
                               x_test,
                               y_test,
                               y_pred,
                               experiment_name,
                               adv_stats,
                               enable_score_charts=False):
    if not enable_score_charts:
        return

    plot_confusion_ma3x(results_location,
                        y_test,
                        y_pred,
                        experiment_name,
                        title=experiment_name + "\n\n" + model_name + "\nConfusion Matrix",
                        file_name=experiment_name + '_' + model_name + "_conf_m3x_v2.png")

    plot_model_roc_curve(results_location,
                         model,
                         model_name,
                         x_test,
                         y_test,
                         experiment_name,
                         title=experiment_name + "\n\n" + model_name + "\nROC Curves",
                         file_name=experiment_name + '_' + model_name + "_roc_curve.png")

    plot_model_precision_recall_curve(results_location,
                                      model,
                                      model_name,
                                      x_test,
                                      y_test,
                                      experiment_name,
                                      title=experiment_name + "\n\n" + model_name + "\nPrecision-Recall Curves",
                                      file_name=experiment_name + '_' + model_name + "_pr_recall_curve.png")


def export_model_insights(results_location,
                          model_name,
                          model,
                          x_test,
                          y_test,
                          y_pred,
                          experiment_name,
                          adv_insights,
                          enable_model_insights=False):
    if not enable_model_insights or adv_insights is None:
        return

    if 'Feature Importance' in adv_insights:
        imp = adv_insights['Feature Importance']
        if imp is not None:
            plot_feature_importance(results_location,
                                    model_name,
                                    experiment_name,
                                    imp,
                                    title=experiment_name + "\n\n" + model_name + "\nFeature Importance",
                                    file_name=experiment_name + '_' + model_name + "_feature_imp.png")

    if 'Permutation Importance' in adv_insights:
        imp = adv_insights['Permutation Importance']
        if imp is not None:
            plot_permutation_importance(results_location,
                                        model_name,
                                        experiment_name,
                                        imp,
                                        title=experiment_name + "\n\n" + model_name + "\nPermutation Importance",
                                        file_name=experiment_name + '_' + model_name + "_permutation_imp.png")


def load_model(model_path):
    if not os.path.exists(model_path):
        return None

    with open(model_path, 'rb') as file:
        model = pickle.load(file)

    logging.info('Model loaded: ' + model_path)
    return model


def score_model(model_name, model, x_test, y_test, enable_model_insights=False):
    logging.info('======================= Predicting with: ' + model_name)
    start_time = time.time()

    # Measure CPU Utilization (Starting point)
    pid = os.getpid()
    p = psutil.Process(pid)
    p.cpu_percent()

    # Make predictions
    predictions = model.predict(x_test)
    pred_time_in_sec = time.time() - start_time
    log_duration(start_time, "---> ---> Prediction time of " + model_name + " is")

    # Collect stats
    adv_stats = {
        'Runtime (sec)': pred_time_in_sec,
        'Runtime (min)': "%0.2f" % ((pred_time_in_sec / 60),),
        'CPU': p.cpu_percent(),
        'Process Memory': p.memory_percent()}

    adv_insights = {}
    if enable_model_insights:
        real_model = model.named_steps["classifier"]
        load_feat_importance(model_name, real_model, adv_insights)
        load_permutation_importance(model_name, real_model, x_test, y_test, adv_insights)

    log_score(model_name, y_test, predictions)
    log_class_report(model_name, y_test, predictions)

    return y_test, predictions, adv_stats, adv_insights


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
        logging.info('---> ---> Loading feature importance of ' + model_name + ': ' + str(d))
        adv_stats['Feature Importance'] = d


def load_permutation_importance(model_name, model, x_test, y_test, adv_stats):
    per_importance = None
    try:
        per_importance = permutation_importance(model, x_test, y_test)
    except:
        logging.error("Oops! Permutation Importance could not be extracted for " + model_name)

    if per_importance is not None:
        logging.info('---> ---> Loading permutation importance of ' + model_name)
        adv_stats['Permutation Importance'] = per_importance
        adv_stats['Permutation Importance']['columns'] = x_test.columns


def log_score(model_name, y_test, predictions):
    logging.info('---> ---> Accuracy Score of ' + model_name + ': ' + str(accuracy_score(predictions, y_test)))


def log_class_report(model_name, y_test, predictions):
    cls_report = classification_report(y_test, predictions)
    logging.debug("---> ---> Classification report of " + model_name + ": \n" + cls_report)


def load_model_stats(y_true, y_pred, adv_stats, enable_score_tables=False):
    if not enable_score_tables:
        return

    return {'classification_report': classification_report(y_true, y_pred, output_dict=True),
            'accuracy': accuracy_score(y_true, y_pred),
            'precision_score_micro': precision_score(y_true, y_pred, average='micro'),
            'recall_score_micro': recall_score(y_true, y_pred, average='micro'),
            'f1_score_micro': f1_score(y_true, y_pred, average='micro'),
            'balanced_accuracy': balanced_accuracy_score(y_true, y_pred),
            'adv_stats': adv_stats}

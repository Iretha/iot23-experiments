import glob
import os
import re
import json
import ntpath
import logging

import sklearn
import time
import psutil
import pandas as pd

from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler

from src.helpers.dataframe_helper import df_get, load_data, scale_data
from src.helpers.file_helper import mk_dir
from src.helpers.model_helper import load_model, score_model
from src.helpers.stats_helper import print_correlations, print_value_distribution, print_scatter_matrix, print_attribute_distribution, plot_conf_m3x
from src.helpers.xls_helper import export_stats_xls


def run_reports(exp_dir, experiment_names, data_file_name, classification_col_name, export_charts=False, export_tables=True):
    for experiment_name in experiment_names:
        run_report(exp_dir, experiment_name, data_file_name, classification_col_name, export_charts=export_charts, export_tables=export_tables)


def run_report(experiments_dir, experiment_name, data_file, class_col_name, results_dir='results', export_charts=False, export_tables=True):
    logging.info("===== Export stats: " + experiment_name)
    start_time = time.time()

    if export_charts or export_tables:
        # Make stats directory
        experiment_location = experiments_dir + experiment_name + "\\"
        results_path = experiment_location + results_dir + "\\"
        mk_dir(results_path)

        data_file_path = experiment_location + "\\data\\" + data_file
        x_train, y_train, x_test, y_test = load_data(data_file_path, class_col_name)

        x_train, x_test = scale_data(x_train, x_test, StandardScaler())

    # Export Data Charts
    if export_charts:
        export_data_stats(data_file_path, results_path, class_col_name)

    # Export Model Scores
    if export_tables:
        models_dir = experiment_location + "\\models\\"
        export_experiment_results(experiment_name, models_dir, x_test, y_test, results_path, class_col_name, export=True)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("===== Stats " + experiment_name + " exported in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


def export_experiment_results(experiment_name, models_location, x_test, y_test, results_location, class_col_name, export=True):
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
            y_test, predictions, adv_stats = score_model(model_name, model, x_test, y_test)
            model_stats[model_name] = export_stats(y_test, predictions, results_location, model_name=model_name)
            model_stats[model_name]['adv_stats'] = adv_stats

    stats['model_stats'] = model_stats
    json_file = results_location + 'stats.json'
    with open(json_file, 'w') as outfile:
        json.dump(stats, outfile)
    export_stats_xls(results_location, stats, experiment_name)


def export_stats(y_true, y_pred, results_location, prefix='', model_name=''):
    stats = {}
    stats['classification_report'] = classification_report(y_true, y_pred, output_dict=True)
    # plot_conf_m3x(y_true, y_pred)

    # plot_confusion_matrix(conf_matrix, None)

    # sns.heatmap(confusion_matrix, annot=True)
    # plt.show()
    # plt.close()

    # plt_confusion_matrix(y_test, predictions, title=prefix + ': ' + model_name)
    # plot_classification_report(cls_report)
    return stats


def export_data_stats(source_file_path, results_path, class_col_name):
    # Data Stats
    df = df_get(source_file_path, delimiter=',')
    export_data_charts(results_path, class_col_name, df, prefix='data_', export=True)

    # Train Data Stats
    df_train = df_get(source_file_path + '_train.csv', delimiter=',')
    export_data_charts(results_path, class_col_name, df_train, prefix='data_train_', export=True)

    # Test Data Stats
    df_test = df_get(source_file_path + '_test.csv', delimiter=',')
    export_data_charts(results_path, class_col_name, df_test, prefix='data_test_', export=True)


def export_data_charts(stats_location, class_col_name, df, prefix='', export=True):
    # Show Correlations
    print_correlations(stats_location, df.corr(), file_name=prefix + "correlations.png", export=export)

    # Print Data Distribution
    print_value_distribution(stats_location, df, class_col_name, file_name=prefix + "class_values_distribution.png", export=export)

    # Print Feature Distribution
    # display_feature_distribution(stats_location, df, file_name="feature_distribution.png")

    print_attribute_distribution(stats_location, df, file_name=prefix + "attr_distribution.png", export=export)

    print_scatter_matrix(stats_location, df, file_name=prefix + "scatter_m3x.png", export=export)

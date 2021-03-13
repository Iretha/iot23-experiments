import glob
import os
import re
import ntpath
import logging
import json
import time
import psutil

from sklearn.metrics import classification_report, plot_confusion_matrix
from src.helpers.dataframe_helper import df_get, load_data
from src.helpers.file_helper import mk_dir, write_json_file
from src.helpers.model_helper import load_model, score_model
from src.helpers.stats_helper import print_correlations, print_class_value_distribution, print_scatter_matrix, print_attribute_distribution, plot_confusion_ma3x, plot_roc_curve, \
    plot_roc_curve_c
from src.helpers.xls_helper import export_stats_xls


def run_reports(exp_dir,
                experiment_names,
                data_file_name,
                classification_col_name,
                export_data_charts=False,
                export_score_tables=True,
                export_score_charts=False):
    for experiment_name in experiment_names:
        run_report(exp_dir,
                   experiment_name,
                   data_file_name,
                   classification_col_name,
                   export_data_charts=export_data_charts,
                   export_score_tables=export_score_tables,
                   export_score_charts=export_score_charts)


def run_report(experiments_dir,
               experiment_name,
               data_file,
               class_col_name,
               results_dir='results',
               export_data_charts=False,
               export_score_tables=True,
               export_score_charts=False):
    if not export_data_charts and not export_score_tables and not export_score_charts:
        return

    logging.info("===== Export stats: " + experiment_name)
    start_time = time.time()

    # Make stats directory
    experiment_location = experiments_dir + experiment_name + "\\"
    results_path = experiment_location + results_dir + "\\"
    mk_dir(results_path)

    # Load data
    data_file_path = experiment_location + "\\data\\" + data_file
    x_train, y_train, x_test, y_test = load_data(data_file_path, class_col_name)

    # Export Data Charts
    export_data_stats(data_file_path,
                      results_path,
                      class_col_name,
                      export_data_charts=export_data_charts)

    # Export Model Scores
    models_dir = experiment_location + "\\models\\"
    export_model_stats(experiment_name,
                       models_dir,
                       x_test,
                       y_test,
                       results_path,
                       class_col_name,
                       export_score_tables=export_score_tables,
                       export_score_charts=export_score_charts)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("===== Stats " + experiment_name + " exported in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


def combine_reports(exp_dir,
                    experiment_names,
                    output_file_name):
    json_stats = find_json_stats(exp_dir, experiment_names)
    export_stats_xls(exp_dir, json_stats, output_file_name=output_file_name)


def find_json_stats(exp_dir, experiment_names):
    json_stats = {}
    for experiment_name in experiment_names:
        experiment_result_json = exp_dir + experiment_name + '\\results\\stats.json'
        with open(experiment_result_json) as json_file:
            json_stats[experiment_name] = json.load(json_file)
    return json_stats


def export_model_stats(experiment_name,
                       models_location,
                       x_test,
                       y_test,
                       results_location,
                       class_col_name,
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
            y_test, predictions, adv_stats = score_model(model_name, model, x_test, y_test)
            model_stats[model_name] = prepare_model_stats(y_test, predictions, adv_stats, export_score_tables=export_score_tables)
            export_model_chart_images(results_location, model_name, model, x_test, y_test, predictions, experiment_name, export_score_charts=export_score_charts)

    stats['model_stats'] = model_stats
    write_json_file(results_location + 'stats.json', stats)
    export_stats_xls(results_location, {experiment_name: stats}, output_file_name=experiment_name + '.xlsx', export_score_tables=export_score_tables)


def prepare_model_stats(y_true, y_pred, adv_stats, export_score_tables=False):
    if not export_score_tables:
        return

    return {'classification_report': classification_report(y_true, y_pred, output_dict=True),
            'adv_stats': adv_stats}


def export_model_chart_images(results_location, model_name, model, x_test, y_test, y_pred, experiment_name, export_score_charts=False):
    if not export_score_charts:
        return

    plot_confusion_ma3x(results_location,
                        model,
                        x_test,
                        y_test,
                        experiment_name,
                        title=experiment_name + " " + model_name + ": Confusion Matrix",
                        file_name=experiment_name + '_' + model_name + "_conf_m3x.png")

    plot_roc_curve_c(results_location,
                     model,
                     model_name,
                     x_test,
                     y_test,
                     experiment_name,
                     title=experiment_name + " " + model_name + ": ROC Curves",
                     file_name=experiment_name + '_' + model_name + "_roc_curve.png")


def export_data_stats(source_file_path,
                      results_path,
                      class_col_name,
                      export_data_charts=False):
    if not export_data_charts:
        return

    # Data Stats
    df = df_get(source_file_path, delimiter=',')
    export_data_chart_images(results_path,
                             class_col_name,
                             df,
                             prefix='data_',
                             export=True)

    # Train Data Stats
    df_train = df_get(source_file_path + '_train.csv', delimiter=',')
    export_data_chart_images(results_path,
                             class_col_name,
                             df_train,
                             prefix='data_train_',
                             export=True)

    # Test Data Stats
    df_test = df_get(source_file_path + '_test.csv', delimiter=',')
    export_data_chart_images(results_path,
                             class_col_name,
                             df_test,
                             prefix='data_test_',
                             export=True)


def export_data_chart_images(stats_location,
                             class_col_name,
                             df,
                             prefix='',
                             export=True):
    print_correlations(stats_location,
                       df.corr(),
                       file_name=prefix + "correlations.png",
                       export=export)

    print_class_value_distribution(stats_location,
                                   df,
                                   class_col_name,
                                   file_name=prefix + "class_values_distribution.png",
                                   export=export)

    print_attribute_distribution(stats_location,
                                 df,
                                 file_name=prefix + "attr_distribution.png",
                                 export=export)

    print_scatter_matrix(stats_location,
                         df,
                         file_name=prefix + "scatter_m3x.png",
                         export=export)

import logging
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scikitplot as sk_plt
import sys
from pandas.plotting import scatter_matrix
from sklearn.metrics import plot_confusion_matrix, roc_curve, auc, plot_roc_curve
from sklearn.utils.multiclass import unique_labels

from src.experiments import iot23_data_config, experiment_definitions, get_exp_def_name_by_experiment, get_exp_features


def print_correlations(output_dir,
                       corr,
                       title="Correlations",
                       file_name="correlations.png",
                       export=True):
    columns_count = len(corr.columns)
    file_path = output_dir + file_name

    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=[columns_count, columns_count])
    fig.suptitle(title, fontsize=18)
    ax = sns.heatmap(corr, annot=True, fmt='.0%', cmap='Greens', ax=ax)

    export_sns(fig, file_path, export=export)


def export_sns(fig, file_path, export=True):
    if export:
        fig.savefig(file_path)
        plt.close()
    else:
        plt.show()


def print_class_value_distribution(output_dir, df, col_name, title="Class Frequency", file_name="data_distribution.png", export=True):
    unique, counts = np.unique(df[col_name], return_counts=True)
    values = counts
    x_values = unique

    file_path = output_dir + file_name
    x = decode_labels(x_values)
    x_pos = [i for i, _ in enumerate(x)]
    cnt = len(x) + 2

    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(cnt, cnt))
    fig.subplots_adjust(bottom=0.2, left=0.2, top=0.75)
    fig.suptitle(title, fontsize=18)
    ax.bar(x_pos, values, color='orange', alpha=0.6)
    # ax.set_title(title)
    ax.set_ylabel('Frequency')
    ax.set_xlabel('Class')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(
        x,
        rotation=35,
        ha="right",
        rotation_mode="anchor")

    # plt.xticks(x_pos, x)

    export_plt(file_path)


def decode_labels(keys):
    class_labels = iot23_data_config['class_labels']
    labels = [class_labels[key] for key in keys]
    return labels


def decode_label(key):
    return iot23_data_config['class_labels'][key]


def get_all_labels():
    class_labels = iot23_data_config['class_labels']
    keys = class_labels.keys()
    labels = [class_labels[key] for key in keys]
    return labels


def display_feature_distribution(output_dir, df, file_name="feature_distribution.png", export=True):
    file_path = output_dir + file_name
    columns_count = len(df.columns)
    df.boxplot()
    plt.figure(figsize=[columns_count, columns_count])
    export_plt(file_path)


def print_attribute_distribution(output_dir,
                                 df,
                                 title='Attribute Distribution',
                                 file_name='attr_distribution.png',
                                 export=True):
    file_path = output_dir + file_name
    columns_count = len(df.columns)

    plt.style.use('ggplot')
    df.hist(alpha=0.6, figsize=(columns_count + 1, columns_count + 1), color='green')
    plt.suptitle(title, fontsize=18)
    export_plt(file_path)


def print_scatter_matrix(output_dir,
                         df,
                         title='Scatter MAtrix',
                         file_name="feature_distribution.png",
                         export=True):
    file_path = output_dir + file_name
    cnt = len(df.columns)

    plt.style.use('ggplot')

    # fig, ax = plt.subplots()
    # fig.subplots_adjust(bottom=0.1, left=0.1)
    # fig.suptitle(title, fontsize=25)

    pd.plotting.scatter_matrix(df, alpha=0.2, figsize=(cnt * 2, cnt * 2), color='black')
    export_plt(file_path, export=export)


def plot_confusion_ma3x(output_dir, model, x_test, y_test, experiment_name, title="Confusion Matrix", file_name="conf_ma3x.png"):
    n_classes = experiment_definitions[get_exp_def_name_by_experiment(experiment_name)]["features"]

    # display_labels = get_all_labels()
    # labels = [i for i, _ in enumerate(display_labels)]
    # columns_count = len(display_labels)
    # fig, ax = plt.subplots(figsize=(columns_count, columns_count))
    # disp = plot_confusion_matrix(model, x_test, y_test, labels=labels, display_labels=display_labels, cmap="Blues", ax=ax)

    disp = plot_confusion_matrix(model, x_test, y_test, cmap="Blues")
    disp.ax_.set_title(title)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    export_plt(output_dir + file_name)


def plot_confusion_ma3x_v2(output_dir,
                           y_test,
                           predictions,
                           experiment_name,
                           title="Confusion Matrix",
                           file_name="conf_ma3x.png"):
    classes = unique_labels(y_test, predictions)
    cnt = len(classes)
    cnt = cnt * 2 if cnt < 10 else cnt * 0.8
    # labels = decode_labels(classes)

    sk_plt.metrics.plot_confusion_matrix(y_test,
                                         predictions,
                                         normalize=True,
                                         title=title + " (Normalized)",
                                         title_fontsize="large",
                                         figsize=(cnt, cnt))
    export_plt(output_dir + file_name + '_n.png')

    # sk_plt.metrics.plot_confusion_matrix(y_test,
    #                                      predictions,
    #                                      normalize=False,
    #                                      title=title,
    #                                      title_fontsize="large",
    #                                      figsize=(cnt, cnt))
    # export_plt(output_dir + file_name)


def plot_roc_curve_custom(output_dir,
                          model,
                          model_name,
                          x_test,
                          y_true,
                          experiment_name,
                          title="ROC Curve",
                          file_name="roc_curve.png"):
    try:
        y_prob = model.predict_proba(x_test)
        sk_plt.metrics.plot_roc(y_true, y_prob, title=title, cmap='nipy_spectral')
        export_plt(output_dir + file_name)
    except:
        logging.error("Oops! Could not export ROC curve for model " + model_name, sys.exc_info()[0], " occurred.")


def plot_precision_recall_curve_custom(output_dir,
                                       model,
                                       model_name,
                                       x_test,
                                       y_true,
                                       experiment_name,
                                       title="Precision Recall Curve",
                                       file_name="pr_recall_curve.png"):
    try:
        y_prob = model.predict_proba(x_test)
        sk_plt.metrics.plot_precision_recall(y_true, y_prob, title=title, cmap='nipy_spectral')
        export_plt(output_dir + file_name)
    except:
        logging.error("Oops! Could not export ROC curve for model " + model_name, sys.exc_info()[0], " occurred.")


# def plot_cumulative_gain_custom(output_dir, model, model_name, x_test, y_true, title="Feature Importance", file_name="feat_importance.png"):
#     try:
#         y_prob = model.predict_proba(x_test)
#         sk_plt.metrics.plot_ks_statistic(y_true, y_prob)
#         plt.show()
#     except:
#         logging.error("Oops! Could not export Feature Importance for " + model_name, sys.exc_info()[0], " occurred.")


def plot_feature_importance(results_location,
                            model_name,
                            experiment_name,
                            feat_importance,
                            title="Feature Importance",
                            file_name="feat_imp.png"):
    feature_names = get_exp_features(experiment_name)

    values = list(feat_importance.values())
    x_pos = [x for x in range(len(values))]

    plt.style.use('ggplot')
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.25, top=0.75, left=0.15)
    ax.bar(x_pos, values, color='orange', alpha=0.6)
    ax.set_title(title)
    ax.set_ylabel('Importance')
    ax.set_xlabel('Features')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(
        feature_names[0:len(values)],
        rotation=35,
        ha="right",
        rotation_mode="anchor")
    export_plt(results_location + file_name)


def export_plt(file_path, export=True):
    if export:
        plt.savefig(file_path)
        plt.close()
    else:
        plt.show()

import logging
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scikitplot as sk_plt
import sys
from pandas.plotting import scatter_matrix
from sklearn.metrics import plot_confusion_matrix, roc_curve, auc, plot_roc_curve

from src.experiments import iot23_data_config, experiment_definitions, get_exp_def_name_by_experiment


def print_correlations(output_dir, corr, label="Correlations", file_name="correlations.png", export=True):
    columns_count = len(corr.columns)
    file_path = output_dir + file_name
    fig, ax = plt.subplots(figsize=[columns_count, columns_count])
    ax = sns.heatmap(corr, annot=True, fmt='.0%', cmap='Greens', ax=ax)
    ax.set_title(label)
    export_sns(fig, file_path, export=export)


def export_sns(fig, file_path, export=True):
    if export:
        fig.savefig(file_path)
        plt.close()
    else:
        plt.show()


def print_class_value_distribution(output_dir, df, col_name, file_name="data_distribution.png", export=True):
    unique, counts = np.unique(df[col_name], return_counts=True)
    file_path = output_dir + file_name

    x = decode_labels(unique)
    x_pos = [i for i, _ in enumerate(x)]

    plt.style.use('ggplot')
    plt.bar(x_pos, counts, color='orange', alpha=0.6)
    plt.title('Class Frequency')
    plt.ylabel('Frequency')
    plt.xlabel('Class')
    plt.xticks(x_pos, x)

    export_plt(file_path)


def decode_labels(keys):
    class_labels = iot23_data_config['class_labels']
    labels = [class_labels[key] for key in keys]
    return labels


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


def print_attribute_distribution(output_dir, df, file_name="attr_distribution.png", export=True):
    file_path = output_dir + file_name
    columns_count = len(df.columns)

    plt.style.use('ggplot')
    df.hist(alpha=0.6, figsize=(columns_count + 1, columns_count + 1), color='green')
    plt.suptitle('Attribute Distribution')
    export_plt(file_path)


def print_scatter_matrix(output_dir, df, file_name="feature_distribution.png", export=True):
    file_path = output_dir + file_name
    columns_count = len(df.columns)
    plt.style.use('ggplot')
    pd.plotting.scatter_matrix(df, alpha=0.2, figsize=(columns_count * 2, columns_count * 2), color='black')
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


def plot_roc_curve_c(output_dir, model, model_name, x_test, y_true, experiment_name, title="ROC Curve", file_name="roc_curve.png"):
    try:
        y_prob = model.predict_proba(x_test)
        sk_plt.metrics.plot_roc_curve(y_true, y_prob, title=title)
        export_plt(output_dir + file_name)
    except:
        logging.error("Oops! Could not export ROC curve for model " + model_name, sys.exc_info()[0], " occurred.")


def export_plt(file_path, export=True):
    if export:
        plt.savefig(file_path)
        plt.close()
    else:
        plt.show()

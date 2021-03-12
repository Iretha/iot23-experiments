import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sklearn
from pandas.plotting import scatter_matrix


def display_sns(fig, plt, file_path, export=True):
    if export:
        fig.savefig(file_path)
        plt.close()
    else:
        plt.show()


def display_plt(plt, file_path, export=True):
    if export:
        plt.savefig(file_path)
        plt.close()
    else:
        plt.show()


def print_correlations(output_dir, corr, label="Correlations", file_name="correlations.png", export=True):
    columns_count = len(corr.columns)
    file_path = output_dir + file_name
    fig, ax = plt.subplots(figsize=[columns_count, columns_count])
    # ax = sns.heatmap(corr, annot=True, fmt='.0%', cmap='Greens', linewidths=.5, ax=ax, cbar=False)
    ax = sns.heatmap(corr, annot=True, fmt='.0%', cmap='Greens', ax=ax)
    ax.set_title(label)
    display_sns(fig, plt, file_path, export=export)


def print_value_distribution(output_dir, df, col_name, file_name="data_distribution.png", export=True):
    unique, counts = np.unique(df[col_name], return_counts=True)
    file_path = output_dir + file_name

    # fig, ax = plt.figure(nrows=1, ncols=1)
    plt.bar(unique, counts)
    # plt.plot(...)
    plt.title('Class Frequency')
    plt.xlabel('Class')
    plt.ylabel('Frequency')

    if export:
        plt.savefig(file_path)
        plt.close()
    else:
        plt.show()


def display_feature_distribution(output_dir, df, file_name="feature_distribution.png", export=True):
    file_path = output_dir + file_name
    columns_count = len(df.columns)
    df.boxplot()
    plt.figure(figsize=[columns_count, columns_count])
    if export:
        plt.savefig(file_path)
        plt.close()
    else:
        plt.show()


def print_attribute_distribution(output_dir, df, file_name="attr_distribution.png", export=True):
    file_path = output_dir + file_name
    columns_count = len(df.columns)
    df.hist()

    if export:
        plt.savefig(file_path)
        plt.close()
    else:
        plt.show()


def print_scatter_matrix(output_dir, df, file_name="feature_distribution.png", export=True):
    file_path = output_dir + file_name
    columns_count = len(df.columns)
    scatter = scatter_matrix(df, alpha=0.2, figsize=(columns_count, columns_count), diagonal='hist')
    display_plt(plt, file_path, export=export)

    # fig, ax = plt.subplots(figsize=[1, 1])
    # sns.pairplot(df)
    # display_sns(fig, plt, file_path, export=export)


def plot_conf_m3x(y_true, y_pred):
    conf_matrix = sklearn.metrics.confusion_matrix(y_true, y_pred, labels=None, sample_weight=None)
    df_cm = pd.DataFrame(conf_matrix)
    plt.figure(figsize=(10, 7))
    sns.heatmap(df_cm, annot=True)
    plt.show()

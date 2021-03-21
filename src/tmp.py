import os

import pandas as pd
import matplotlib.pyplot as plt
import psutil
import seaborn as sns

from src.experiments import data_cleanup_conf
from src.helpers.dataframe_helper import df_get

# def usage():
#     process = psutil.Process(os.getpid())
#     print(process.memory_full_info()[0] / float(2 ** 20))
#     print(psutil.cpu_percent(interval=None))
#     print(psutil.virtual_memory())
#     print(psutil.disk_usage('E:'))
#
#
#
# usage()
from src.helpers.log_helper import log_start, log_end

info = log_start('Start')

# file_path = 'E:\\machine-learning\\datasets\\iot23\\3_data\\FL16_R_5_000_000_clean.csv'
file_path = 'E:\\machine-learning\\datasets\\iot23\\4_experiments\\F14_FL16_R_5_000_000\\data\\FL16_R_5_000_000_clean.csv_train.csv'
file_path1 = 'E:\\machine-learning\\datasets\\iot23\\4_experiments\\F14_FL16_R_5_000_000\\data\\FL16_R_5_000_000_clean.csv_test.csv'
pd.set_option('display.expand_frame_repr', False)
df = df_get(file_path, delimiter=',')


df_val_counts = df['detailed-label'].value_counts()
print(df_val_counts)
# labels_map = data_cleanup_conf['category_encodings']['detailed-label']
# labels_map_r = {v: k for k, v in labels_map.items()}


# df['label'] =
# sns.pairplot(df.iloc[:, [7, 8, 9]], hue='detailed-label')


# vizualize corr
# size = 8
# plt.figure(figsize=[size, size])
# sns.heatmap(df.iloc[:, [1, 3, 4, 6, 9, 13, 18, 19]].corr().abs(), annot=True, fmt='.0%', cmap='Greens')
# plt.show()

def get_top_abs_correlations(df, n=5):
    au_corr = df.corr().abs().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    return au_corr[0:n]


def get_redundant_pairs(df):
    """ Get diagonal and lower triangular pairs of correlation matrix"""
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i + 1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop


# print(get_top_abs_correlations(df, 3))

log_end(info, 'End')
quit()

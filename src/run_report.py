import os
import warnings

import logging

import ntpath

import re
import sklearn
from glob import glob
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.linear_model import Perceptron, LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

from config import iot23_experiments_dir
from src.helpers.experiment_stats_helper import run_report, run_reports

# Set logging
from src.helpers.file_helper import list_folder_names

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S', handlers=[
        logging.FileHandler("..\logs\exp_stats.log"),
        logging.StreamHandler()
    ])

# Setup warnings
warnings.filterwarnings("ignore", category=sklearn.exceptions.UndefinedMetricWarning)
warnings.filterwarnings("ignore", category=sklearn.exceptions.ConvergenceWarning)

training_algorithms = dict([
    ('GaussianNB', GaussianNB()),  # 1.327 sec
    ('Perceptron', Perceptron(eta0=0.2, max_iter=1000, tol=1e-3, verbose=0, early_stopping=True, validation_fraction=0.1)),  # 25.717 sec
    ('DecisionTree', DecisionTreeClassifier(random_state=0)),  # 17.019 sec
    ('RandomForest', RandomForestClassifier(random_state=0)),  # 6.318 min
    ('AdaBoost', AdaBoostClassifier(n_estimators=100, random_state=0)),  # 6.426 min
    ('MLPClassifier', MLPClassifier(alpha=1e-05, hidden_layer_sizes=(15,), random_state=1, solver='lbfgs')),  # 8.313 min
    ('LogisticRegression', LogisticRegression(solver='lbfgs', max_iter=1000)),  # 16.95 min
    ('GradientBoosting', GradientBoostingClassifier(random_state=0)),  # 37.039 min
    ('SVC_linear', LinearSVC()),  # 47.565 min
    # ('KNeighborsClassifier', KNeighborsClassifier(n_neighbors=3)),  # 0.293 sec
    # ('SVC_rbf', SVC(kernel='rbf')),  # idk
    # ('SVC_poly', SVC(kernel='poly')),  # idk
])


exp_dir = iot23_experiments_dir
exp_list_all = list_folder_names(exp_dir)
exp_list = [
    'EXP_FL16_FT13_R_100_000'
]
run_reports(exp_dir, exp_list_all, '_data_02.csv', 'detailed-label', export_charts=False, export_tables=True)

print('The end.')

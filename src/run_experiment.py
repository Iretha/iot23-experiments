import logging
import pandas as pd
import warnings

import sklearn
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.linear_model import Perceptron, LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier

from src.helpers.experiment_helper import run_experiments

# Set logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S', handlers=[
        logging.FileHandler("..\logs\exp_exec.log"),
        logging.StreamHandler()
    ])

# Set python's max row display
pd.set_option('display.max_row', 1000)

# Set Python's max column width to 50
pd.set_option('display.max_columns', 50)

# Setup warnings
warnings.filterwarnings("ignore", category=sklearn.exceptions.UndefinedMetricWarning)
warnings.filterwarnings("ignore", category=sklearn.exceptions.ConvergenceWarning)

training_algorithms = dict([
    ('GaussianNB', GaussianNB()),  # 1.327 sec
    ('Perceptron', Perceptron(eta0=0.2, max_iter=1000, tol=1e-3, verbose=0, early_stopping=True, validation_fraction=0.1)),  # 25.717 sec
    ('DecisionTree', DecisionTreeClassifier()),  # 17.019 sec
    ('RandomForest', RandomForestClassifier()),  # 6.318 min
    ('AdaBoost', AdaBoostClassifier(n_estimators=100)),  # 6.426 min
    ('MLPClassifier', MLPClassifier(alpha=1e-05, hidden_layer_sizes=(15,), random_state=1, solver='lbfgs')),  # 8.313 min
    ('LogisticRegression', LogisticRegression(solver='lbfgs', max_iter=1000)),  # 16.95 min
    ('GradientBoosting', GradientBoostingClassifier()),  # 37.039 min
    # ('SVC_linear', LinearSVC()),  # 47.565 min
    # ('KNeighborsClassifier', KNeighborsClassifier(n_neighbors=3)),  # 0.293 sec
    # ('SVC_rbf', SVC(kernel='rbf')),  # idk
    # ('SVC_poly', SVC(kernel='poly')),  # idk
])

rows_per_attack = [10_000, 100_000]
exp_list = {
    'EXP_FL4_FT13_R_': rows_per_attack,
    'EXP_FL4_FT14_R_': rows_per_attack,
    'EXP_FL4_FT17_R_': rows_per_attack,
    'EXP_FL4_FT19_R_': rows_per_attack,

    'EXP_FL16_FT13_R_': rows_per_attack,
    'EXP_FL16_FT14_R_': rows_per_attack,
    'EXP_FL16_FT17_R_': rows_per_attack,
    'EXP_FL16_FT19_R_': rows_per_attack,
}
# score_experiment_models('EXP_FL4_FT13_R_', 100_000, training_algorithms.keys())

run_experiments(exp_list, training_algorithms, override=True)

print('The end.')


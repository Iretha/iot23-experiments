import logging
import pandas as pd
import warnings
import sklearn
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.linear_model import Perceptron, LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier

from config import iot23_experiments_dir, iot23_attacks_dir
from src.experiments import experiment_definitions
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
    ('DecisionTree', DecisionTreeClassifier()),  # 17.019 sec
    ('Perceptron', Perceptron()),  # 25.717 sec
    ('RandomForest', RandomForestClassifier()),  # 6.318 min
    ('AdaBoost', AdaBoostClassifier()),  # 6.426 min
    ('LogisticRegression', LogisticRegression()),  # 16.95 min
    ('MLPClassifier', MLPClassifier()),  # 8.313 min
    ('GradientBoosting', GradientBoostingClassifier()),  # 37.039 min
    # ('SVC_linear', LinearSVC()),  # 47.565 min
    # ('KNeighborsClassifier', KNeighborsClassifier(n_neighbors=3)),  # 0.293 sec
    # ('SVC_rbf', SVC(kernel='rbf')),  # idk
    # ('SVC_poly', SVC(kernel='poly')),  # idk
    # ('Perceptron', Perceptron(eta0=0.2, max_iter=1000, tol=1e-3, verbose=0, early_stopping=True, validation_fraction=0.1)),  # 25.717 sec
    # ('MLPClassifier', MLPClassifier(alpha=1e-05, hidden_layer_sizes=(15,), random_state=1, solver='lbfgs')),  # 8.313 min
    # ('LogisticRegression', LogisticRegression(solver='lbfgs', max_iter=1000)),  # 16.95 min
])

rows_per_attack = [100_000]
exp_list_all = experiment_definitions.keys()
exp_list_selected = [
    'EXP_FL4_FT12_R_',
]
# score_experiment_models('EXP_FL4_FT13_R_', 100_000, training_algorithms.keys())
run_experiments(iot23_experiments_dir,
                iot23_attacks_dir,
                exp_list_all,
                rows_per_attack,
                training_algorithms,
                override=True)

print('The end.')

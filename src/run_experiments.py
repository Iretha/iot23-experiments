import logging
import pandas as pd
import warnings
import sklearn
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

from config import iot23_experiments_dir, iot23_attacks_dir
from src.helpers.experiment_helper import run_experiments

# Set logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S', handlers=[
        logging.FileHandler("..\logs\experiment_execution.log"),
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
    # ('DecisionTree', DecisionTreeClassifier()),  # 5 mil = 2 min
    # ('GaussianNB', GaussianNB()),  # 5 mil = 5 sec
    # ('LogisticRegression_Multi-Class', LogisticRegression(multi_class='multinomial')),  # 5 mil = 22 min
    # ('RandomForest', RandomForestClassifier()),  # 5 mil = 52 min
    # ('MLPClassifier', MLPClassifier()),  # 8.313 min
    # ('SVC_Multi-Class', LinearSVC(c=1.0, max_iter=1000)),  # 5 mil= 14h
    # ('AdaBoost_Decision_Tree', AdaBoostClassifier(DecisionTreeClassifier())),  # 6.426 min
    ('SVC_linear', LinearSVC()),  # 47.565 min

    # ('KNeighborsClassifier', KNeighborsClassifier(n_neighbors=3)),  # 0.293 sec
    # ('Perceptron', Perceptron()),  # 25.717 sec
])

rows_per_attack = [5_000_000]
# exp_list_all = experiment_definitions.keys()
exp_list_selected = [
    # 'EXP_FL16_FT12_R_',
    'EXP_FL16_FT14_R_',
    # 'EXP_FL16_FT17_R_',
    # 'EXP_FL16_FT18_R_',
    # 'EXP_FL16_FT19_R_',
    #
    # 'EXP_FL4_FT12_R_',
    # 'EXP_FL4_FT14_R_',
    # 'EXP_FL4_FT17_R_',
    # 'EXP_FL4_FT18_R_',
    # 'EXP_FL4_FT19_R_',
]
# score_experiment_models('EXP_FL4_FT13_R_', 100_000, training_algorithms.keys())
run_experiments(iot23_experiments_dir,
                iot23_attacks_dir,
                exp_list_selected,
                rows_per_attack,
                training_algorithms,
                override=False,
                prepare_data=True)

print('The end.')

# ('LogisticRegression', LogisticRegression(max_iter=1000)),  # 16.95 min
# ('KNeighborsClassifier', KNeighborsClassifier(n_neighbors=3)),  # 0.293 sec
# ('AdaBoost_DecTree', AdaBoostClassifier(DecisionTreeClassifier(max_depth=2),
#                                         n_estimators=600,
#                                         learning_rate=1)),
# ('LabelSpreading', LabelSpreading()),  # 47.565 min
# ('LabelPropagation', LabelPropagation()),  # 47.565 min
# ('SVC_linear', LinearSVC()),  # 47.565 min
# ('MLPClassifier', MLPClassifier()),  # 8.313 min
# ('GradientBoosting', GradientBoostingClassifier()),  # 37.039 min
# ('AdaBoost', AdaBoostClassifier()),  # 6.426 min
# ('Perceptron', Perceptron()),  # 25.717 sec
# ('SVC_rbf', SVC()),  # idk
# ('SVC_poly', SVC(kernel='poly')),  # idk
# ('Perceptron', Perceptron(eta0=0.2, max_iter=1000, tol=1e-3, verbose=0, early_stopping=True, validation_fraction=0.1)),  # 25.717 sec
# ('MLPClassifier', MLPClassifier(alpha=1e-05, hidden_layer_sizes=(15,), random_state=1, solver='lbfgs')),  # 8.313 min
# ('LogisticRegression', LogisticRegression(solver='lbfgs', max_iter=1000)),  # 16.95 min

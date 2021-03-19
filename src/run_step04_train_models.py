from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

from config import iot23_data_dir, iot23_experiments_dir
from src.experiments import data_combinations, feature_combinations
from src.helpers.log_helper import add_logger
from src.helpers.st4_experiments_helper import run_combinations

add_logger(file_name='04_train_models.log')

# Selected Data Files
data_file_dir = iot23_data_dir
data_combinations = [
    data_combinations['FL04_R_100_000'],
    # data_combinations['FL16_R_100_000'],
    #
    # data_combinations['FL04_R_5_000_000'],
    # data_combinations['FL16_R_5_000_000'],
]

# Selected Features
features = [
    feature_combinations['F14'],
]

# Selected Algorithms
training_algorithms = dict([
    ('DecisionTree', Pipeline([('normalization', MinMaxScaler()), ('classifier', DecisionTreeClassifier())])),  # 5 mil = 2 min
    ('GaussianNB', Pipeline([('normalization', StandardScaler()), ('classifier', GaussianNB())])),  # 5 mil = 11 sec
    ('LogisticRegression', Pipeline([('normalization', StandardScaler()), ('classifier', LogisticRegression(max_iter=1000))])),  # 5 mil = 21 min
    ('RandomForest', Pipeline([('normalization', StandardScaler()), ('classifier', RandomForestClassifier())])),  # 5 mil = 48 min
    ('SVC_linear', Pipeline([('normalization', MinMaxScaler()), ('classifier', LinearSVC())])),  # 5 mil = 44 min
    ('AdaBoost_Decision_Tree', Pipeline([('normalization', StandardScaler()), ('classifier', AdaBoostClassifier(DecisionTreeClassifier(max_depth=2), n_estimators=1000))])),
    ('AdaBoost', Pipeline([('normalization', MinMaxScaler()), ('classifier', AdaBoostClassifier(n_estimators=1000))])),  # 5 mil = 2 min
])

experiments_dir = iot23_experiments_dir
run_combinations(data_file_dir,
                 experiments_dir,
                 data_combinations,
                 features,
                 training_algorithms,
                 overwrite=False)

print('Step 04: The end.')

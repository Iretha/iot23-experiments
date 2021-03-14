import logging

import sklearn
import warnings

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from config import iot23_experiments_dir, iot23_attacks_dir
from src.experiments import experiment_definitions, iot23_data_config
from src.helpers.experiment_helper import run_experiments, list_experiment_names
from src.helpers.report_helper import run_reports, combine_reports

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S', handlers=[
        logging.FileHandler("..\logs\demo.log"),
        logging.StreamHandler()
    ])

# Setup warnings
warnings.filterwarnings("ignore", category=sklearn.exceptions.UndefinedMetricWarning)
warnings.filterwarnings("ignore", category=sklearn.exceptions.ConvergenceWarning)


def run_demo(experiments_dir,
             attack_files_dir,
             experiments,
             rows_per_attack,
             training_algorithms,
             output_data_file,
             classification_col,
             combined_stats_xlsx_file_name="combined_stats.xlsx"):
    # Run Experiments
    run_experiments(experiments_dir,
                    attack_files_dir,
                    experiments,
                    rows_per_attack,
                    training_algorithms,
                    override=False)

    # Run Reports
    experiment_names = list_experiment_names(experiments, rows_per_attack)
    run_reports(experiments_dir,
                experiment_names,
                output_data_file,
                classification_col,
                export_data_charts=True,
                export_score_tables=True,
                export_score_charts=True)

    # Combine results into single xlsx file
    combine_reports(experiments_dir, experiment_names, combined_stats_xlsx_file_name)


all_experiments = experiment_definitions.keys()
demo_output_data_file = iot23_data_config["output_file_name"]
demo_classification_col = iot23_data_config["classification_col"]
demo_experiments_dir = iot23_experiments_dir
demo_attack_files_dir = iot23_attacks_dir
demo_rows_per_attack = [100, 1_000]
demo_training_algorithms = dict([
    # ('GaussianNB', GaussianNB()),
    ('DecisionTree', DecisionTreeClassifier()),
    # ('Perceptron', Perceptron()),
    ('RandomForest', RandomForestClassifier()),
    # ('AdaBoost', AdaBoostClassifier()),
    # ('LogisticRegression', LogisticRegression()),
    # ('MLPClassifier', MLPClassifier()),
    # ('GradientBoosting', GradientBoostingClassifier()),
])
demo_selected_experiments = [
    "EXP_FL4_FT12_R_",
    "EXP_FL16_FT12_R_",
]
# demo_experiments = all_experiments
demo_experiments = demo_selected_experiments
demo_combined_stats_xlsx_file_name = "combined_stats_m1.xlsx"

run_demo(demo_experiments_dir,
         demo_attack_files_dir,
         demo_experiments,
         demo_rows_per_attack,
         demo_training_algorithms,
         demo_output_data_file,
         demo_classification_col,
         demo_combined_stats_xlsx_file_name)
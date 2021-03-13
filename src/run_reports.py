import logging
import sklearn
import warnings

from config import iot23_experiments_dir
from src.experiments import iot23_data_config
from src.helpers.report_helper import run_reports
from src.helpers.file_helper import list_folder_names

# Set logging
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

exp_dir = iot23_experiments_dir
exp_list_all = list_folder_names(exp_dir)
exp_list_selected = [
    'EXP_FL4_FT12_R_10_000',
    # 'EXP_FL16_FT12_R_10_000',
]
run_reports(exp_dir,
            exp_list_selected,
            iot23_data_config["output_file_name"],
            iot23_data_config["classification_col"],
            export_charts=False,
            export_tables=True)

print('The end.')

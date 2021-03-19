import logging
import sklearn
import warnings

from config import iot23_experiments_dir
from src.experiments import iot23_data_config
from src.helpers.report_helper import run_reports, combine_reports
from src.helpers.file_helper import list_folder_names

# Set logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S', handlers=[
        logging.FileHandler("..\logs\experiment_reports.log"),
        logging.StreamHandler()
    ])

# Setup warnings
warnings.filterwarnings("ignore", category=sklearn.exceptions.UndefinedMetricWarning)
warnings.filterwarnings("ignore", category=sklearn.exceptions.ConvergenceWarning)

exp_dir = iot23_experiments_dir
# exp_list_all = list_folder_names(exp_dir)

no = '5_000_000'
exp_list_selected = [
    # 'EXP_FL16_FT12_R_' + no,
    'EXP_FL16_FT14_R_' + no,
    # 'EXP_FL16_FT17_R_' + no,
    # 'EXP_FL16_FT18_R_' + no,
    # 'EXP_FL16_FT19_R_' + no,
    #
    # 'EXP_FL4_FT12_R_' + no,
    # 'EXP_FL4_FT14_R_' + no,
    # 'EXP_FL4_FT17_R_' + no,
    # 'EXP_FL4_FT18_R_' + no,
    # 'EXP_FL4_FT19_R_' + no,
]
run_reports(exp_dir,
            exp_list_selected,
            iot23_data_config["output_file_name"],
            iot23_data_config["classification_col"],
            export_data_charts=True,
            export_score_tables=True,
            export_score_charts=True)

combine_reports(exp_dir, exp_list_selected, 'combined_all_1m.xlsx')

print('The end.')

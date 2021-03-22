import logging
import time

import xlsxwriter

from src.helpers.stats_helper import decode_label


def export_stats_xls(output_dir, exp_stats_dict, output_file_name='stats.xlsx', enable_score_tables=False):
    if not enable_score_tables:
        return

    file_path = output_dir + output_file_name

    logging.info("===== Export xlsx file: " + file_path)
    start_time = time.time()

    workbook = xlsxwriter.Workbook(file_path)
    try:
        create_overall_scores_worksheet(workbook, exp_stats_dict, title="Model Overall Scores")
        create_class_scores_worksheet(workbook, exp_stats_dict, title="Model Class Scores")
    finally:
        if workbook is not None:
            workbook.close()

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("===== Xlsx file in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


def create_overall_scores_worksheet(workbook, exp_stats_dict, title="Model Scores"):
    header = [
        'EXP',
        'Algorithm',
        'Runtime (sec)',
        'Accuracy',
        'Precision (Weighted Avg)',
        'Precision (Macro)',
        'Recall (Weighted Avg)',
        'Recall (Macro)',
        'F1-Score (Weighted Avg)',
        'F1-Score (Macro)',
        'F1-Score (Micro)',
        'Support (Weighted Avg)',
        'Support (Macro)'
    ]
    content = [header]
    exp_stat_names = exp_stats_dict.keys()
    for exp_stat_name in exp_stat_names:
        exp_stats = exp_stats_dict[exp_stat_name]
        create_overall_model_scores_content(content, exp_stat_name, exp_stats)

    worksheet = workbook.add_worksheet(name=title)
    write_sheet_content(worksheet, content)


def create_overall_model_scores_content(content, exp_name, exp_stats):
    model_stats = exp_stats['model_stats']
    model_names = model_stats.keys()
    for model_name in model_names:
        if model_stats[model_name] is None:
            logging.warning("No stats json for exp=" + exp_name + " and model=" + model_name)
            continue

        model_cls_report = model_stats[model_name]['classification_report']
        adv_stats = model_stats[model_name]['adv_stats']
        row_content = [exp_name,
                       model_name,
                       float(adv_stats['Runtime (sec)']),
                       float(model_cls_report["accuracy"]),
                       float(model_cls_report["weighted avg"]["precision"]),
                       float(model_cls_report["macro avg"]["precision"]),
                       float(model_cls_report["weighted avg"]["recall"]),
                       float(model_cls_report["macro avg"]["recall"]),
                       float(model_cls_report["weighted avg"]["f1-score"]),
                       float(model_cls_report["macro avg"]["f1-score"]),
                       float(model_stats[model_name]['f1_score_micro']),
                       float(model_cls_report["weighted avg"]["support"]),
                       float(model_cls_report["macro avg"]["support"])]
        content.append(row_content)
    return content


def create_class_scores_worksheet(workbook, exp_stats_dict, title="Class Scores"):
    header = [
        'EXP',
        'Algorithm',
        'Class',
        'Class Code',
        'Precision',
        'Recall',
        'F1-Score',
        'Support',
    ]
    content = [header]
    exp_stat_names = exp_stats_dict.keys()
    for exp_stat_name in exp_stat_names:
        exp_stats = exp_stats_dict[exp_stat_name]
        create_class_model_scores_content(content, exp_stat_name, exp_stats)

    worksheet = workbook.add_worksheet(name=title)
    write_sheet_content(worksheet, content)


def create_class_model_scores_content(content, exp_name, exp_stats):
    model_stats = exp_stats['model_stats']
    model_names = model_stats.keys()
    for model_name in model_names:
        if model_stats[model_name] is None:
            logging.warning("No stats json for exp=" + exp_name + " and model=" + model_name)
            continue

        model_cls_report = model_stats[model_name]['classification_report']
        keys = model_cls_report.keys()
        filtered_keys = [x for x in keys if x.isnumeric()]
        for key in filtered_keys:
            key_num = int(key)
            label = decode_label(key_num)
            row_cells = [exp_name,
                         model_name,
                         label,
                         key_num,
                         model_cls_report[key]["precision"],
                         model_cls_report[key]["recall"],
                         model_cls_report[key]["f1-score"],
                         model_cls_report[key]["support"]]
            content.append(row_cells)
    return content


def write_sheet_content(worksheet, content):
    row = 0
    for line in content:
        column = 0
        for cell in line:
            worksheet.write(row, column, cell)
            column += 1
        row += 1

import pandas as pd
import xlsxwriter


def export_stats_xls(output_dir, dict, title):
    file_path = output_dir + title + '.xlsx'
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()

    model_stats = dict['model_stats']
    model_names = model_stats.keys()

    header = [
        'EXP',
        'Algorithm',
        'Accuracy',
        'Precision (macro avg)',
        'Precision (weighted avg)',
        'Recall (macro avg)',
        'Recall (weighted avg)',
        'F1-Score (macro avg)',
        'F1-Score (weighted avg)',
        'Support (macro avg)',
        'Support (weighted avg)',
    ]
    content = [header]

    for model_name in model_names:
        model_cls_report = model_stats[model_name]['classification_report']
        row_content = [title,
                       model_name,
                       model_cls_report["accuracy"],
                       model_cls_report["macro avg"]["precision"],
                       model_cls_report["weighted avg"]["precision"],
                       model_cls_report["macro avg"]["recall"],
                       model_cls_report["weighted avg"]["recall"],
                       model_cls_report["macro avg"]["f1-score"],
                       model_cls_report["weighted avg"]["f1-score"],
                       model_cls_report["macro avg"]["support"],
                       model_cls_report["weighted avg"]["support"]]
        content.append(row_content)

    row = 0
    for line in content:
        column = 0
        for cell in line:
            worksheet.write(row, column, cell)
            column += 1
        row += 1

    workbook.close()

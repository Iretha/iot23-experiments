import xlsxwriter


def export_stats_xls(output_dir, exp_stats_dict, output_file_name='stats.xlsx', export_score_tables=False):
    if not export_score_tables:
        return

    file_path = output_dir + output_file_name
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()

    header = [
        'EXP',
        'Algorithm',
        'Runtime (sec)',
        'Runtime (min)',
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

    exp_stat_names = exp_stats_dict.keys()
    for exp_stat_name in exp_stat_names:
        exp_stats = exp_stats_dict[exp_stat_name]
        prepare_content(content, exp_stat_name, exp_stats)

    row = 0
    for line in content:
        column = 0
        for cell in line:
            worksheet.write(row, column, cell)
            column += 1
        row += 1

    workbook.close()


def prepare_content(content, exp_name, exp_stats):
    model_stats = exp_stats['model_stats']
    model_names = model_stats.keys()
    for model_name in model_names:
        model_cls_report = model_stats[model_name]['classification_report']
        adv_stats = model_stats[model_name]['adv_stats']
        row_content = [exp_name,
                       model_name,
                       adv_stats['Runtime (sec)'],
                       adv_stats['Runtime (min)'],
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
    return content

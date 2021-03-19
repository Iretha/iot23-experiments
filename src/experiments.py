iot23_config = {
    "file_name_pattern": "/**/conn.log.labeled",
    "file_header": "ts	uid	id.orig_h	id.orig_p	id.resp_h	id.resp_p	proto	service	duration	orig_bytes	resp_bytes	conn_state	local_orig	local_resp	missed_bytes	history	orig_pkts	orig_ip_bytes	resp_pkts	resp_ip_bytes	tunnel_parents	label	detailed-label\n",
    "all_columns": [
        'ts', 'uid',
        'id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p', 'proto',
        'service', 'duration', 'orig_bytes', 'resp_bytes', 'conn_state',
        'local_orig', 'local_resp', 'missed_bytes', 'history', 'orig_pkts',
        'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes', 'tunnel_parents',
        'label', 'detailed-label'
    ],
    "numeric_columns": ["duration",
                        "orig_bytes",
                        "resp_bytes",
                        "missed_bytes",
                        "local_orig",
                        "local_resp",
                        "orig_pkts",
                        "orig_ip_bytes",
                        "resp_pkts",
                        "resp_ip_bytes"],
}

iot23_data_config = {
    "classification_col": "detailed-label",
    "replace_values": {},
    "replace_values_in_col": {
        "detailed-label": {
            "-": "Benign"
        },
        "duration": {
            "-": 99
        },
        "orig_bytes": {
            "-": 99
        },
        "resp_bytes": {
            "-": 99
        },
        "missed_bytes": {
            "-": 99
        },
        "local_orig": {
            "-": 99
        },
        "local_resp": {
            "-": 99
        },
        "orig_pkts": {
            "-": 99
        },
        "orig_ip_bytes": {
            "-": 99
        },
        "resp_pkts": {
            "-": 99
        },
        "resp_ip_bytes": {
            "-": 99
        },
    },
    "transform_to_numeric": [
        "duration",
        "orig_bytes",
        "resp_bytes",
        "missed_bytes",
        "local_orig",
        "local_resp",
        "orig_pkts",
        "orig_ip_bytes",
        "resp_pkts",
        "resp_ip_bytes"
    ],
    "class_labels": {
        0: "Benign",
        1: "Att",
        2: "C&C",
        3: "C&C-FD",
        4: "C&C-HB",
        5: "C&C-HB-Att",
        6: "C&C-HB-FD",
        7: "C&C-Mirai",
        8: "C&C-HPS",
        9: "C&C-Torii",
        10: "DDoS",
        11: "FD",
        12: "Okiru",
        13: "Okiru-Att",
        14: "HorizPortSc",
        15: "HPS-Att",
    },
    "category_encodings": {
        "conn_state": {
            "S0": 0,
            "S1": 1,
            "S2": 2,
            "S3": 3,
            "SF": 4,
            "REJ": 5,
            "RSTO": 6,
            "RSTR": 7,
            "RSTOS0": 8,
            "RSTRH": 9,
            "SH": 10,
            "SHR": 11,
            "OTH": 12
        },
        "detailed-label": {
            "Benign": 0,
            "Attack": 1,
            "C&C": 2,
            "C&C-FileDownload": 3,
            "C&C-HeartBeat": 4,
            "C&C-HeartBeat-Attack": 5,
            "C&C-HeartBeat-FileDownload": 6,
            "C&C-Mirai": 7,
            "C&C-PartOfAHorizontalPortScan": 8,
            "C&C-Torii": 9,
            "DDoS": 10,
            "FileDownload": 11,
            "Okiru": 12,
            "Okiru-Attack": 13,
            "PartOfAHorizontalPortScan": 14,
            "PartOfAHorizontalPortScan-Attack": 15
        },
        # "history": {
        #     "S": 10,
        #     "H": 11,
        #     "A": 12,
        #     "D": 13,
        #     "F": 14,
        #     "R": 15,
        #     "C": 16,
        #     "I": 17,
        #     "s": 100,
        #     "h": 101,
        #     "a": 102,
        #     "d": 103,
        #     "f": 104,
        #     "r": 105,
        #     "c": 106,
        #     "i": 107,
        # },
        "label": {
            "benign": 0,
            "Malicious": 1
        },
        "proto": {
            "icmp": 0,
            "tcp": 1,
            "udp": 2
        },
        "service": {
            "-": 0,
            "dhcp": 1,
            "dns": 2,
            "http": 3,
            "ssh": 4,
            "ssl": 5,
            "irc": 6
        },
        "tunnel_parents": {
            "-": 0,
            "(empty)": 1
        },
    },
    "combined_file_name": "_data_01_pre.csv",
    "output_file_name": "_data_02.csv",
}

data_combinations = {
    'Combination_1': {
        "description": 'Combination_1 (4 classes)',
        "files": ["Benign.csv",
                  "DDoS.csv",
                  "Okiru.csv",
                  "PartOfAHorizontalPortScan.csv"],
        "max_rows_per_file": 5_000_000,
        "output_file_name": 'data_combination_1.scv'},
    'Combination_2': {
        "description": 'Combination_2 (all classes)',
        "files": [],  # empty => combine all source files
        "max_rows_per_file": 5_000_000,
        "output_file_name": 'data_combination_2.scv'},
}

feature_combinations = {
    # All without:
    # 'ts', 'uid', 'label'
    "iot23_F19": [
        'id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p', 'proto',
        'service', 'duration', 'orig_bytes', 'resp_bytes', 'conn_state',
        'local_orig', 'local_resp', 'missed_bytes', 'history', 'orig_pkts',
        'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes', 'tunnel_parents',
        'detailed-label'
    ],

    # EXP_FL16_FT18_R_ / EXP_FL4_FT18_R_
    # All without:
    # 'ts', 'uid', 'label', 'id.orig_h'
    "iot23_F18": [
        'id.orig_p', 'id.resp_h', 'id.resp_p', 'proto',
        'service', 'duration', 'orig_bytes', 'resp_bytes', 'conn_state',
        'local_orig', 'local_resp', 'missed_bytes', 'history', 'orig_pkts',
        'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes', 'tunnel_parents',
        'detailed-label'
    ],

    # EXP_FL16_FT17_R_ / EXP_FL4_FT17_R_
    # All without:
    # 'ts', 'uid', 'label', 'id.orig_h', 'id.resp_h'
    "iot23_F17": [
        'id.orig_p', 'id.resp_p', 'proto',
        'service', 'duration', 'orig_bytes', 'resp_bytes', 'conn_state',
        'local_orig', 'local_resp', 'missed_bytes', 'history', 'orig_pkts',
        'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes', 'tunnel_parents',
        'detailed-label'
    ],

    # EXP_FL16_FT14_R_ / EXP_FL4_FT14_R_
    # All without:
    # 'ts', 'uid', 'label', 'id.orig_h', 'local_orig',
    # 'local_resp', 'missed_bytes',  'tunnel_parents'
    "iot23_F14_RESEARCH1": [
        'id.orig_p', 'id.resp_h', 'id.resp_p', 'proto',
        'service', 'duration', 'orig_bytes', 'resp_bytes', 'conn_state',
        'history', 'orig_pkts',
        'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes',
        'detailed-label'
    ],

    # EXP_FL16_FT12_R_ / EXP_FL14_FT12_R_
    # All without:
    # 'ts', 'uid', 'label', 'id.orig_h', 'service', 'history'
    # 'local_orig', 'local_resp', 'missed_bytes',  'tunnel_parents'
    "iot23_F12_RESEARCH2": [
        'id.orig_p', 'id.resp_h', 'id.resp_p', 'proto',
        'duration', 'orig_bytes', 'resp_bytes', 'conn_state',
        'orig_pkts', 'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes',
        'detailed-label'
    ],
}

experiment_definitions = {
    "EXP_FL16_FT12_R_": {
        "description": "Based on the second research; All attack types",
        "attack_files": data_combinations['Combination_2']['files'],
        "features": feature_combinations['iot23_F12_RESEARCH2'],
        "config": iot23_data_config,
    },
    "EXP_FL4_FT12_R_": {
        "description": "Based on the second research; All attack types",
        "attack_files": data_combinations['Combination_1']['files'],
        "features": feature_combinations['iot23_F12_RESEARCH2'],
        "config": iot23_data_config,
    },

    "EXP_FL16_FT14_R_": {
        "description": "Based on the research; All attack types",
        "attack_files": data_combinations['Combination_2']['files'],
        "features": feature_combinations['iot23_F14_RESEARCH1'],
        "config": iot23_data_config,
    },
    "EXP_FL4_FT14_R_": {
        "description": "Based on the research; All attack types",
        "attack_files": data_combinations['Combination_1']['files'],
        "features": feature_combinations['iot23_F14_RESEARCH1'],
        "config": iot23_data_config,
    },

    "EXP_FL16_FT17_R_": {
        "description": "All features without: 'ts', 'uid', 'label', 'id.orig_h', 'id.resp_h'; All attack types",
        "attack_files": data_combinations['Combination_2']['files'],
        "features": feature_combinations['iot23_F17'],
        "config": iot23_data_config,
    },
    "EXP_FL4_FT17_R_": {
        "description": "All features without: 'ts', 'uid', 'label', 'id.orig_h', 'id.resp_h'; All attack types",
        "attack_files": data_combinations['Combination_1']['files'],
        "features": feature_combinations['iot23_F17'],
        "config": iot23_data_config,
    },

    "EXP_FL16_FT18_R_": {
        "description": "All features without: 'ts', 'uid', 'label', 'id.orig_h'; All atack types",
        "attack_files": data_combinations['Combination_2']['files'],
        "features": feature_combinations['iot23_F18'],
        "config": iot23_data_config,
    },
    "EXP_FL4_FT18_R_": {
        "description": "All features without: 'ts', 'uid', 'label', 'id.orig_h'; All atack types",
        "attack_files": data_combinations['Combination_1']['files'],
        "features": feature_combinations['iot23_F18'],
        "config": iot23_data_config,
    },

    "EXP_FL16_FT19_R_": {
        "description": "All features without: 'ts', 'uid', 'label'; All attack types",
        "attack_files": data_combinations['Combination_2']['files'],
        "features": feature_combinations['iot23_F19'],
        "config": iot23_data_config,
    },
    "EXP_FL4_FT19_R_": {
        "description": "All features without: 'ts', 'uid', 'label'; All attack types",
        "attack_files": data_combinations['Combination_1']['files'],
        "features": feature_combinations['iot23_F19'],
        "config": iot23_data_config,
    },
}


def get_exp_def_name_by_experiment(experiment_name):
    exp_def_name = experiment_name.split("_R_", 1)[0]
    exp_def_name += "_R_"
    return exp_def_name


def get_exp_features(experiment_name):
    exp_def_name = get_exp_def_name_by_experiment(experiment_name)
    exp_def = experiment_definitions[exp_def_name]
    return exp_def['features']


def get_train_data_path(file_path):
    return file_path + '_train.csv'


def get_test_data_path(file_path):
    return file_path + '_test.csv'

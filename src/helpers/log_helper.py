import logging
import os

import psutil
import time


def add_logger(file_name='log.log', level=logging.INFO):
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=level,
        datefmt='%Y-%m-%d %H:%M:%S', handlers=[
            logging.FileHandler("..\logs\\" + file_name),
            logging.StreamHandler()
        ])

    sys_file_handler = logging.FileHandler("..\logs\\sys_info.log")
    sys_file_handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    logging.getLogger('sys').addHandler(sys_file_handler)



def log_duration(start_time, msg):
    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info(msg + " %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


def log_start(msg):
    stats = {
        'start_msg': msg,
        'start_stats': build_stats()
    }

    logging.info(msg)
    logging.getLogger('sys').info(msg + ' => ' + str(stats))
    return stats


def log_end(stats, msg):
    stats['end_stats'] = build_stats()

    exec_time_seconds = round((stats['end_stats']['time'] - stats['start_stats']['time']))
    exec_time_minutes = round(exec_time_seconds / 60)

    stats['duration_sec'] = exec_time_seconds
    stats['duration_min'] = exec_time_minutes

    msg = msg + " %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes)

    logging.info(msg)
    logging.getLogger('sys').info(msg + ' => ' + str(stats))
    return stats


def build_stats():
    pid = os.getpid()
    process = psutil.Process(pid)
    stats = {
        'time': time.time(),
        'pid': pid,
        'time': time.time(),
        'memory': (process.memory_full_info()[0] / float(2 ** 20)),
        'cpu_per': psutil.cpu_percent(interval=None),
        'v_memory': psutil.virtual_memory(),
    }
    return stats


add_logger(file_name='stats_results.log')

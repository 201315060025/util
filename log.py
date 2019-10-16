import sys
import os
from pathlib import Path
import logging

logger_map = {}


def get_module_logger(module_name,
                      ch_level=logging.WARNING,
                      enable_fh=True,
                      fh_level=logging.INFO,
                      log_dir=None):
    """
    get module logger

    :param module_name: module name
    :param ch_level: StreamHandler level
    :param enable_fh: is use FileHandler
    :param fh_level: FileHandler level
    :param log_dir: log file path
    :return: logging.Logger
    """

    if module_name in logger_map:
        return logger_map[module_name]

    # create logger
    logger = logging.getLogger(module_name)
    logger.setLevel(fh_level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(ch_level)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    if enable_fh:
        log_dir = Path(sys.argv[0]).parent / 'logs' if log_dir is None else Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / f'{module_name}.log'

        fh = logging.FileHandler(log_path, encoding='utf-8')
        fh.setLevel(fh_level)
        fh.setFormatter(formatter)

        logger.addHandler(fh)

    logger_map[module_name] = logger
    return logger

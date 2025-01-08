import logging


def get_file_logger(name, path, level='INFO'):
    # please mind: within a single python process, loggers that share the same name refer to the 
    # same logger instance.
    logger = logging.getLogger(name)
    
    logger.setLevel(getattr(logging, level.upper(), None))
    
    for i in logger.handlers.copy():
        logger.removeHandler(i)
    
    file_handler = logging.FileHandler(path)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

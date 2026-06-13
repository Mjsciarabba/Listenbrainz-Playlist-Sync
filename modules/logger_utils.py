import logging
import colorlog

formatter = colorlog.ColoredFormatter(
    fmt='%(log_color)s%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d,%H:%M:%S',
    log_colors={
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)


def create_logger():
    handler = colorlog.StreamHandler()
    handler.setFormatter(formatter)

    # Set the level for the root logger
    # logging.root.setLevel(logging.NOTSET)
    logging.root.setLevel(logging.INFO)

    # Add the colorlog handler to the root logger
    logging.root.addHandler(handler)

    # Now, use the root logger for your application's logging
    logger = logging.getLogger(__name__)

    return logger


logger = create_logger()

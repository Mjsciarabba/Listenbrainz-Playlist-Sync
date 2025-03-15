import logging
import colorlog
from tqdm import tqdm

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


def get_tqdm_bar(iterable, desc="Processing", unit="item"):
    return tqdm(iterable, desc="\x1b[32m{}:".format(desc), unit=unit,
                bar_format="\x1b[32m{desc} {percentage:3.0f}%|\x1b[32m{bar}| {n}/{total} tracks found \x1b[0m")

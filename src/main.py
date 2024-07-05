import logging
from logging.handlers import RotatingFileHandler

from src.controllers import Scenarios
from src.UI.OverlayUI import OverlayUI
from src.controllers.ThaumInteractor import createTI
from src.utils.constants import LOG_FILE_PATH, MAX_LOG_FILE_SIZE_BYTES
from utils.utils import createDirByFilePath

createDirByFilePath(LOG_FILE_PATH)
logging.basicConfig(
    handlers=[logging.handlers.RotatingFileHandler(filename=LOG_FILE_PATH, maxBytes=MAX_LOG_FILE_SIZE_BYTES, backupCount=5)],
    format="%(asctime)s [%(levelname)s] (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    level=logging.DEBUG,
)

UI = OverlayUI(opacity=1)

def main():
    TI = createTI(UI)
    if TI is None:
        return
    Scenarios.runResearching(UI, TI)


if __name__ == '__main__':
    logging.info("Program started")
    logging.info("###############")
    try:
        UI.start(main)
    except Exception as e:
        logging.critical(f"Error excepted: {e}")

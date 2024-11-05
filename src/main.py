import logging
import sys
from logging.handlers import RotatingFileHandler

from src.controllers import Scenarios
from src.UI.OverlayUI import OverlayUI
from src.controllers.ThaumInteractor import createTI
from src.utils.constants import LOG_FILE_PATH, MAX_LOG_FILE_SIZE_BYTES, DEBUG, LOG_LEVEL, MAX_LOG_FILES_COUNT
from src.utils.utils import createDirByFilePath

createDirByFilePath(LOG_FILE_PATH)
loggingHandlers = [logging.handlers.RotatingFileHandler(filename=LOG_FILE_PATH, maxBytes=MAX_LOG_FILE_SIZE_BYTES, backupCount=MAX_LOG_FILES_COUNT)]
if DEBUG:
    loggingHandlers.append(logging.StreamHandler(sys.stdout))  # output both to console and log-files
logging.basicConfig(
    handlers=loggingHandlers,
    format="%(asctime)s [%(levelname)s] (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    level=LOG_LEVEL,
    force=True,
)

UI = OverlayUI(opacity=1)

def main():
    TI = createTI(UI)
    if TI is None:
        logging.critical("Unknown error when creating ThaumcraftInteractor. It cannot be created")
        return
    Scenarios.beReadyForStartSolving(UI)


if __name__ == '__main__':
    logging.info("Program started")
    logging.info("###############")
    try:
        UI.start(main)
    except Exception as e:
        logging.critical(f"Error excepted: {e}")

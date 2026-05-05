import logging
import sys
from logging.handlers import RotatingFileHandler

from controllers import Scenarios
from UI.OverlayUI import OverlayUI
from configs.constants import LOG_FILE_PATH, MAX_LOG_FILE_SIZE_BYTES, DEBUG, LOG_LEVEL, MAX_LOG_FILES_COUNT
from utils import AppState
from utils.utils import createDirByFilePath

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
    AppState.rereadAllConfigs()

    try:
        if AppState.selectedLanguage is None:
            Scenarios.chooseLanguage(UI)
            return None

        if AppState.thaumWindowControls is None:
            Scenarios.configureThaumWindowCoords(UI)
            return None

        if AppState.selectedThaumVersion is None:
            Scenarios.chooseThaumVersion(UI)
            return None

        Scenarios.beReadyForCreatingTI(UI)
        return None
    except Exception as e:
        logging.critical(f"Error excepted in main thread: {e}")
        return None


if __name__ == '__main__':
    logging.info("Program started")
    logging.info("###############")
    try:
        UI.start(main)
    except Exception as e:
        logging.critical(f"Error excepted in UI thread: {e}")

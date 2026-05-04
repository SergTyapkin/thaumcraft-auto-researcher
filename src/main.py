import logging
import sys
from logging.handlers import RotatingFileHandler

from controllers.scenarios.scenario1_Enroll import enroll
from controllers.scenarios.scenario4_ChooseThaumVersion import chooseThaumVersion
from controllers.scenarios.scenario6_DetectAspectsCreateTI import beReadyForCreatingTI
from src.UI.OverlayUI import OverlayUI
from src.utils.constants import LOG_FILE_PATH, MAX_LOG_FILE_SIZE_BYTES, DEBUG, LOG_LEVEL, MAX_LOG_FILES_COUNT, \
    THAUM_CONTROLS_CONFIG_PATH, THAUM_VERSION_CONFIG_PATH
from src.utils.utils import createDirByFilePath, readJSONConfig

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
    try:
        pointsConfig = readJSONConfig(THAUM_CONTROLS_CONFIG_PATH)
        if pointsConfig is None:
            enroll(UI)
            return None

        selected_thaum_version = readJSONConfig(THAUM_VERSION_CONFIG_PATH)
        if selected_thaum_version is None:
            chooseThaumVersion(UI)
            return None

        beReadyForCreatingTI(UI)
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

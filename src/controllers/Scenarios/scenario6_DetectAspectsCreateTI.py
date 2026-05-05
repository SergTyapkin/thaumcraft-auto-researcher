import logging

from UI.OverlayUI import OverlayUI
from configs.translations import TEXTS
from controllers.ThaumInteractor import createTI
from controllers import Scenarios
from controllers.Scenarios.shared import createNextBackButtonsAndText, createButtonsAndText
from configs.constants import MARGIN
from utils import AppState
from utils.utils import renderDelay


def beReadyForCreatingTI(UI: OverlayUI):
    UI.clearAll()
    UI.createExitButton()

    def startCreatingTI():
        UI.clearAll()
        UI.createExitButton()
        createButtonsAndText(
            UI,
            AppState.translatedTexts[TEXTS.waitForDetectionAspects],
            [],
            MARGIN, MARGIN,
            False,
        )
        UI.repaint()
        renderDelay()
        directlyCreateTI(UI)

    createNextBackButtonsAndText(
        UI,
        AppState.translatedTexts[TEXTS.beReadyForDetectionAspects],
        startCreatingTI, [],
        Scenarios.chooseThaumVersion, [UI],
    )


def directlyCreateTI(UI):
    logging.info(f"Create TI")
    TI = createTI(UI, Scenarios.configureThaumWindowCoords, Scenarios.chooseThaumVersion)
    if TI is None:
        logging.critical(f"Unknown error when creating ThaumcraftInteractor. It cannot be created")
        return
    logging.info(f"TI successfully created")
    UI.repaint()
    renderDelay()
    TI.updateAvailableAspectsInInventory(Scenarios.detectionAspectsDialogue, [UI, TI])

import logging

from UI.OverlayUI import OverlayUI
from controllers.ThaumInteractor import createTI
from controllers.scenarios.scenario4_ChooseThaumVersion import chooseThaumVersion
from controllers.scenarios.scenario7_DetectionAspectsDialogue import detectionAspectsDialogue
from controllers.scenarios.shared import createNextBackButtonsAndText, createButtonsAndText
from utils.constants import MARGIN
from utils.utils import renderDelay


def beReadyForCreatingTI(UI: OverlayUI):
    UI.clearAll()
    UI.createExitButton()

    def startCreatingTI():
        UI.clearAll()
        UI.createExitButton()
        createButtonsAndText(
            UI,
            f"""Ждите и не двигайте курсором мыши!""",
            [],
            MARGIN, MARGIN,
            False,
        )
        UI.repaint()
        renderDelay()
        directlyCreateTI(UI)

    createNextBackButtonsAndText(
        UI,
        f"""Сейчас нейросеть определит имеющиеся аспекты в твоем столе, сконфигурированном ранее.
Не двигайте курсором мыши в процессе!""",
        startCreatingTI, [],
        chooseThaumVersion, [UI],
    )


def directlyCreateTI(UI):
    logging.info(f"Create TI")
    TI = createTI(UI)
    if TI is None:
        logging.critical(f"Unknown error when creating ThaumcraftInteractor. It cannot be created")
        return
    logging.info(f"TI successfully created")
    UI.repaint()
    renderDelay()
    TI.updateAvailableAspectsInInventory(detectionAspectsDialogue, [UI, TI])

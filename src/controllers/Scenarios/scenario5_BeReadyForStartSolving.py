import logging

from UI.OverlayUI import OverlayUI
from configs.translations import TEXTS
from controllers.ThaumInteractor import ThaumInteractor
from controllers import Scenarios
from controllers.Scenarios.shared import createNextBackButtonsAndText
from utils import AppState


def beReadyForStartSolving(UI: OverlayUI, TI: ThaumInteractor):
    logging.info(f"Be ready for solving scenario started")
    UI.clearAll()
    UI.createExitButton()

    createNextBackButtonsAndText(
        UI,
        AppState.translatedTexts[TEXTS.beReadyForStartSolving],
        Scenarios.runResearching, [UI, TI],
        Scenarios.chooseThaumVersion, [UI],
    )

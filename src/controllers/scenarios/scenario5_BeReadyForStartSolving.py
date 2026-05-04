import logging

from UI.OverlayUI import OverlayUI
from controllers.ThaumInteractor import ThaumInteractor
from controllers.scenarios.scenario4_ChooseThaumVersion import chooseThaumVersion
from controllers.scenarios.scenario8_Researchings import runResearching
from controllers.scenarios.shared import createNextBackButtonsAndText


def beReadyForStartSolving(UI: OverlayUI, TI: ThaumInteractor):
    logging.info(f"Be ready for solving scenario started")
    UI.clearAll()
    UI.createExitButton()

    createNextBackButtonsAndText(
        UI,
        f"""Сейчас нейросеть будет определять аспекты, находящиеся на поле.
Выложите записку исследования в ячейку стола, а инвентарь заполните записками исследований,
начиная с самого верхнего левого слота. Они будут исследоваться по очереди""",
        runResearching, [UI, TI],
        chooseThaumVersion, [UI],
    )

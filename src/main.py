from src.controllers import Scenarios
from src.UI.OverlayUI import OverlayUI
from src.controllers.ThaumInteractor import createTI

UI = OverlayUI(opacity=1)


def main():
    TI = createTI(UI)
    if TI is None:
        return
    Scenarios.runResearching(UI, TI)


if __name__ == '__main__':
    UI.start(main)

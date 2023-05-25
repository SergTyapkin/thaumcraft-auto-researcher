from src import Scenarios
from src.OverlayUI import OverlayUI
from src.ThaumInteractor import createTI

UI = OverlayUI(opacity=1)


def main():
    TI = createTI(UI)
    if TI is not None:
        Scenarios.runResearching(UI, TI)


if __name__ == '__main__':
    UI.start(main)

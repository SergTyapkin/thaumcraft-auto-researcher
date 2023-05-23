from src import Scenarios
from src.OverlayUI import OverlayUI
from src.ThaumInteractor import ThaumInteractor
from src.utils import readThaumControlsConfig

UI = OverlayUI(opacity=1)


def main():
    pointsConfig = readThaumControlsConfig()
    if pointsConfig is None:
        Scenarios.enroll(UI)
        return

    TI = ThaumInteractor(pointsConfig)
    Scenarios.runResearching(UI, TI)


if __name__ == '__main__':
    UI.start(main)

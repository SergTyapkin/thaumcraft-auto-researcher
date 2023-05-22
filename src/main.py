from src import Scenarios
from src.OverlayUI import OverlayUI


UI = OverlayUI(opacity=1)


def main():
    Scenarios.configureThaumWindow(UI)


if __name__ == '__main__':
    UI.start(main)

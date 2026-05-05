import logging

from PyQt5.QtGui import QColor

from UI.OverlayUI import OverlayUI
from UI.primitives import Text
from configs.translations import TEXTS
from controllers import Scenarios
from controllers.Scenarios.shared import createNextBackButtonsAndText, PointTextAnchor
from configs.constants import MARGIN
from utils.AppState import AppState


def chooseThaumVersion(UI: OverlayUI):
    UI.clearAll()
    UI.createExitButton()

    def onSubmit():
        if selectedVersion[0] is None:
            logging.warning(f"Trying to go next but thaum version is not selected")
            return
        logging.info(f"Selected thaum version: {selectedVersion[0]}")
        AppState.saveThaumVersion(selectedVersion[0])
        Scenarios.beReadyForCreatingTI(UI)

    (infoText, _, backButton) = createNextBackButtonsAndText(
        UI,
        AppState.translatedTexts[TEXTS.chooseThaumVersion],
        onSubmit, [],
        Scenarios.configureThaumWindowCoords, [UI],
    )
    recipesConfig = AppState.allAspectRecipes
    versions = list(recipesConfig.keys())
    versionsObjects = []

    selectedVersionObject: list[Text | None] = [None]
    selectedVersion: list[str | None] = [None]

    oldVersion = AppState.selectedThaumVersion
    if oldVersion is None:
        oldVersion = "4.2.2.0 - 4.2.3.5"
        logging.info(f"Selected version in config is none. Selecting default: {oldVersion}")
    else:
        logging.info(f"Selected in config version is: {oldVersion}")

    oldInfoTextCallback = infoText.onMoveCallback
    def updateVersionsPosition():
        oldInfoTextCallback()
        startCurY = backButton.y + backButton.h + MARGIN * 2
        curY = startCurY
        curX = PointTextAnchor.x
        for i in range(len(versionsObjects)):
            versionObject = versionsObjects[i]
            if curY > UI.height() - versionObject.h:
                curX += 300
                curY = startCurY
            versionObject.y = curY
            versionObject.x = curX
            curY += versionObject.h + MARGIN

    infoText.LT.onMoveCallback = updateVersionsPosition
    infoText.onMoveCallback = updateVersionsPosition
    startCurY = backButton.y + backButton.h + MARGIN * 2
    curY = startCurY
    curX = PointTextAnchor.x
    for i in range(len(versions)):
        version = versions[i]

        def onClickVersion(versionObject, version):
            logging.debug(f"Click on version {version}")
            selectVersion(versionObject, version)

        def selectVersion(versionObject, version):
            if selectedVersionObject[0] is not None:
                selectedVersionObject[0].setColor(QColor('white'))
            logging.debug(f"Version {version} selected in UI. Previous selected version is {selectedVersion[0]}")
            selectedVersion[0] = version
            selectedVersionObject[0] = versionObject
            selectedVersionObject[0].setColor(QColor('purple'))

        versionObject = UI.addObject(Text(
            0, 0,
            version,
            color=QColor('white'),
            withBackground=True,
            padding=MARGIN,
            UI=UI,
            onClickCallback=onClickVersion,
            hoverable=True,
        ))
        if curY > UI.height() - versionObject.h:
            curX += 300
            curY = startCurY
        versionObject.x = curX
        versionObject.y = curY
        curY += versionObject.h + MARGIN
        versionObject.onClickCallbackArgs = [versionObject, version]
        versionsObjects.append(versionObject)
        if oldVersion == version:
            selectVersion(versionObject, version)

    logging.info(f"Selecting version dialogue showed. Versions: {versions}")

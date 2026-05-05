import logging

from PyQt5.QtGui import QColor

from UI.OverlayUI import OverlayUI
from UI.primitives import Text
from configs.translations import TRANSLATIONS, TEXTS
from controllers import Scenarios
from controllers.Scenarios.shared import PointTextAnchor, createNextBackButtonsAndText
from configs.constants import MARGIN
from utils.AppState import AppState


def chooseLanguage(UI: OverlayUI):
    UI.clearAll()
    UI.createExitButton()

    def onSubmit():
        if selectedLanguage[0] is None:
            logging.warning(f"Trying to go next but language is not selected")
            return
        logging.info(f"Selected language: {selectedLanguage[0]}")
        AppState.saveLanguage(selectedLanguage[0])
        Scenarios.enroll(UI)

    (infoText, nextButton, _) = createNextBackButtonsAndText(
        UI,
        f"""Select language""",
        onSubmit, [],
        None, [],
        "Go next >",
        None
    )
    languagesKeys = list(TRANSLATIONS.keys())
    languagesNames = list(map(lambda trans: trans[TEXTS.languageName], TRANSLATIONS.values()))
    languagesTextObjects = []

    selectedLanguageObject: list[Text | None] = [None]
    selectedLanguage: list[str | None] = [None]

    oldLanguageKey = AppState.selectedLanguage
    if oldLanguageKey is None:
        oldLanguageKey = "English"
        logging.info(f"Selected language in config is none. Selecting default: {oldLanguageKey}")
    else:
        logging.info(f"Selected in config language is: {oldLanguageKey}")

    oldInfoTextCallback = infoText.onMoveCallback
    def updateTextsPosition():
        oldInfoTextCallback()
        startCurY = nextButton.y + nextButton.h + MARGIN * 2
        curY = startCurY
        curX = PointTextAnchor.x
        for i in range(len(languagesTextObjects)):
            textObject = languagesTextObjects[i]
            if curY > UI.height() - textObject.h:
                curX += 300
                curY = startCurY
            textObject.y = curY
            textObject.x = curX
            curY += textObject.h + MARGIN

    infoText.LT.onMoveCallback = updateTextsPosition
    infoText.onMoveCallback = updateTextsPosition
    startCurY = nextButton.y + nextButton.h + MARGIN * 2
    curY = startCurY
    curX = PointTextAnchor.x
    for i in range(len(languagesKeys)):
        languageKey = languagesKeys[i]
        languageName = languagesNames[i]

        def onClickLanguage(languageObject, languageKey):
            logging.debug(f"Click on language {languageKey}")
            selectLanguage(languageObject, languageKey)

        def selectLanguage(languageObject, languageKey):
            if selectedLanguageObject[0] is not None:
                selectedLanguageObject[0].setColor(QColor('white'))
            logging.debug(f"Language {languageKey} selected in UI. Previous selected language is {selectedLanguage[0]}")
            selectedLanguage[0] = languageKey
            selectedLanguageObject[0] = languageObject
            selectedLanguageObject[0].setColor(QColor('purple'))

        languageObject = UI.addObject(Text(
            0, 0,
            languageName,
            color=QColor('white'),
            withBackground=True,
            padding=MARGIN,
            UI=UI,
            onClickCallback=onClickLanguage,
            hoverable=True,
        ))
        if curY > UI.height() - languageObject.h:
            curX += 300
            curY = startCurY
        languageObject.x = curX
        languageObject.y = curY
        curY += languageObject.h + MARGIN
        languageObject.onClickCallbackArgs = [languageObject, languageKey]
        languagesTextObjects.append(languageObject)
        if oldLanguageKey == languageKey:
            selectLanguage(languageObject, languageKey)

    logging.info(f"Selecting language dialogue showed. Languages: {languagesKeys}")

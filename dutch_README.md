[//]: # (![GithubCI]&#40;https://github.com/SergTyapkin/thaumcraft-auto-researcher/actions/workflows/auto-translate-readme.yml/badge.svg&#41;)

[![](https://img.shields.io/badge/русский-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/russian_README.md)
[![](https://img.shields.io/badge/english-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/english_README.md)
[![](https://img.shields.io/badge/中文(简体)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/chinese%20(simplified)_README.md)
[![](https://img.shields.io/badge/中文(传统)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/chinese%20(traditional)_README.md)
[![](https://img.shields.io/badge/arabic(العربية)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/arabic_README.md)
[![](https://img.shields.io/badge/español-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/spanish_README.md)
[![](https://img.shields.io/badge/italiano-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/italian_README.md)
[![](https://img.shields.io/badge/Deutsch-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/dutch_README.md)
[![](https://img.shields.io/badge/hindi(हिन्दी)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/hindi_README.md)
[![](https://img.shields.io/badge/korean(한국어)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/korean_README.md)



# Automatische ontdekkingsreiziger voor Thaumcraft 4

[![Download latest .exe](https://dabuttonfactory.com/button.png?t=Download+latest++.exe&f=Open+Sans-Bold&ts=20&tc=fff&w=300&h=60&c=round&bgt=gradient&bgc=6B6BFF&ebgc=BB8EFF)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases/tag/v1.2.1)
<br> [![see all releases](https://dabuttonfactory.com/button.png?t=see+all+releases&f=Open+Sans-Bold-Italic&ts=12&tc=fff&w=300&h=16&c=round&bgt=gradient&bgc=2B8F3B&ebgc=5BBB3F)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
<details>
<summary>Changelog:</summary>

- Ondersteuning toegevoegd voor verschillende talen binnen het programma
- Configuraties worden opgeslagen in AppData. Bij het herstarten hoeft u de applicatie niet meer opnieuw te configureren
- Nu bepaalt het neurale netwerk de aspecten die op tafel liggen!
Dankzij dit is de snelheid van het onderzoek meer dan tien keer toegenomen.
- Verbeterde snelheid van het neurale netwerk dankzij de lokale caching
- Sneltoetsen toegevoegd voor fijnere bediening
- Non-stop onderzoeksmodus toegevoegd

> `v1.2._` - configuratie van alle aspecten met behulp van verschillende neurale netwerken en het maken van de ontbrekende

> `v1.1._` - configuratie van aspecten op de tafel door een neuraal netwerk met de mogelijkheid om door de gebruiker te worden gewijzigd

> `v1.0._` - configuratie van aspecten op de tafel door de gebruiker

> `v0._._` - pre-release MVP-versies
</details>

> _**Thaumcraft**_ is een mod voor het spel _Minecraft_, vaak geïnstalleerd in magische mod-assemblages op populaire servers

Het programma gebruikt twee neurale netwerken om aspecten op het scherm te bepalen en lost op algoritmische wijze onderzoeksaantekeningen op en rangschikt deze in de onderzoekstabel.
De gehele interactie-interface is doorschijnend en verschijnt bovenaan het spelvenster.

Het programma heeft **op geen enkele manier** interactie met de spelcode en wordt niet gedetecteerd door anti-cheats.
Het enige wat het doet is kijken naar **pixels op het scherm**, neurale netwerken gebruiken om te bepalen welke aspecten op het scherm staan, en **muis- en toetsenbordacties nabootsen** alsof een mens het doet.

> [!BELANGRIJK]
> Voor vragen, fouten en suggesties, schrijf: [t.me/Tyapkin_S](https://t.me/tyapkin_s)

<details>
<summary>Список поддерживаемых аддонов (развернуть...)</summary>

- Magische bijen
- Verboden magie
- Hebzucht
- GregTech
- GregTech NewHorizons
- Thaumic-laarzen
- Botanische add-ons
- Het Elysium
- Thaumische openbaringen
- Essentiële Thaumaturgie
- AbyssalCraft-integratie
</details>

https://github.com/user-attachments/assets/a2eaa3b7-c7fe-4fbc-9905-1b19a32d498f




# Hoe gebruik je dit?
> [!LET OP]
> Afbeeldingen en beschrijvingen komen niet overeen met de nieuwste versie van het programma. Het maakt gebruik van een soortgelijk systeem, maar meer geautomatiseerd. U kunt eenvoudig de aanwijzingen in het programma volgen en alles zal voor u duidelijk zijn.
> We zullen de onderstaande instructies zeker bijwerken, maar dat is het voor nu.

### Voorinstelling
> _Eenmalig uitgevoerd na de eerste start van het programma_
0. Download het programma van [releases](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
1. Demonstratie en verificatie dat het dradenkruis kan worden verplaatst.
Verplaats gewoon de rode stip naar de gele.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/enroll.png?raw=true)
2. U moet het programma vertellen waar de onderzoekstafelinterface zich bevindt.
Om dit te doen, moeten de hoeken van de gele rechthoek zo worden verplaatst dat ze langs de buitenrand van de tafel lopen, zoals weergegeven in de onderstaande schermafbeelding
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/find_table.png?raw=true)
3. Het is noodzakelijk om het programma gedetailleerder te laten weten waar de interactieknoppen zich in de betoveringstabel bevinden.
Verplaats hiervoor alle punten zoals weergegeven in de onderstaande schermafbeelding
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_controls.png?raw=true)
4. Selecteer uw Thaumcraft-versie en alle geïnstalleerde add-ons
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_version_and_addons.png?raw=true) 

Na het voltooien van al deze stappen worden alle gebruikersselecties opgeslagen in de map `C://users/%USER%/.ThaumcraftAutoResearcher`,
de volgende keer dat u het programma start, is dit niet nodig; de volgende stap wordt onmiddellijk getoond.
U kunt altijd terugkeren naar de configuratie door op de `Backspace`-toets te drukken

### Aspectketens oplossen
1. **Plaats een onderzoeksnotitie** uit het inventarisvak linksboven in het onderzoekstafelvak
Nadat u op 'Enter' heeft gedrukt, start het proces van het bepalen van aspecten op het veld met behulp van een neuraal netwerk.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/prepare_to_solving_aspects.png?raw=true)
Er wordt automatisch een oplossing gegenereerd met behulp van ketens van aspecten, die het programma gaat posten
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_solved.png?raw=true)

> [!TIP]
> Als de aspectketen te groot is of aspecten gebruikt die je niet hebt, druk dan op `R` om deze opnieuw te genereren
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_rerolled.png?raw=true)

> [!TIP]
> Als u iets in het spel moet doen zodat het spel de programma-interface niet overlapt, kunt u op `Ctrl+Shift+Spatie` drukken en
het programma pauzeert totdat u opnieuw op deze toetsencombinatie drukt.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/program_paused.png?raw=true)

> [!TIP]
> Als een van de cellen onjuist is gedefinieerd, kunt u op de cel klikken en selecteren wat de cel eigenlijk zou moeten zijn.
Hierna wordt de oplossing automatisch geregenereerd
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects.png?raw=true)
2. **Zorg ervoor dat er voldoende inkt in de inkttank zit**. Als ze opraken, stopt het algoritme voor het indelen van aspecten niet.
en onderzoeksaantekeningen zullen niet worden opgelost.
Druk vervolgens op 'Enter' en het proces van het opmaken van aspecten op de tafel volgens de resulterende ketens zal beginnen.
3. **Na het opmaken van de aspecten** wordt de onderzoeksnotitie in de inventaris geplaatst,
en in plaats daarvan wordt de volgende uit de inventaris op tafel gelegd.
Daarna herhaalt het proces zich opnieuw. Op deze manier kun je een groot aantal bankbiljetten die in de inventaris liggen, achter elkaar oplossen
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/next_research_putted.png?raw=true)

> [!TIP]
> - Om onderzoeksaantekeningen één voor één te kunnen blijven onderzoeken, zoals ze in de inventaris staan, kunt u op `Ctrl+Enter` drukken en vervolgens
Bij het bestuderen van elke volgende noot wacht het programma niet op bevestiging van de gebruiker met de 'Enter'-toets, maar begint het onmiddellijk met het posten van de oplossing.

> [!TIP]
> - Bij het indelen van aspecten wordt de toetsencombinatie `Ctrl+Shift+Alt` voorzien voor het geval het noodzakelijk is het programma dringend te beëindigen.





## In toekomstige versies...
- Adaptieve snelheid afhankelijk van de FPS in het spel
- Controle van de juistheid van de aangelegde kettingen
- Volgen van de inkttankstatus
- Vertaling naar andere talen binnen de applicatie




# Uitvoeren vanaf bron:
1. Installeer afhankelijkheden:
```shell
pip install -r requirements.txt
```

2. Voeg de map project src toe aan PYTHONPATH:
Ramen:
```cmd
set "PYTHONPATH=$($CWD);$($PYTHONPATH)"
```
-Unix:
```cmd
export PYTHONPATH=$(cwd):$PYTHONPATH
```

3. Uitvoeren vanuit de projectroot (vereist `Python 3.10` of hoger):
```shell
python -m src.main
```


## Bouw de applicatie in een .exe-bestand
1. Afhankelijkheden en builder installeren:
```shell
pip install -r requirements.txt
pip install auto-py-to-exe
```

2. ***\[Optionele stap]*** Download UPX (verkleint de grootte van het uiteindelijke exe-bestand)
https://github.com/upx/upx/releases/


3. Voer de build-opdracht uit vanuit de hoofdmap van het project (er wordt een interface geopend van waaruit u de build kunt uitvoeren):
```shell
auto-py-to-exe -c .\pyinstaller_configs\autoPyToExe.json
```

4. ***\[Optionele stap]*** Geef in de sectie **Geavanceerd** `--upx-dir` op (de locatie van de map met het uitvoerbare bestand `upx.exe`) en voer de build uit.
Het gecompileerde exe-bestand zal verschijnen in de map `output` in deze map


### Speciale dank
- [Acak1221](https://github.com/acak1221) voor het creëren van een neuraal netwerk voor het bepalen van aspecten in een oplossing
- [Limuranius](https://github.com/Limuranius) voor het creëren van een neuraal netwerk voor het bepalen van aspecten en hun aantal in de tabel, en veel werk aan het creëren van een lichtgewicht systeem voor het lanceren van neurale netwerken
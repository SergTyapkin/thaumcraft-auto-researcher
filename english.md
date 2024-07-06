![GithubCI](https://github.com/SergTyapkin/thaumcraft-auto-researcher/actions/workflows/auto-translate-readme.yml/badge.svg)

[![](https://img.shields.io/badge/русский-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/russian.md)
[![](https://img.shields.io/badge/english-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/english.md)
[![](https://img.shields.io/badge/中文(简体)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/chinese%20(simplified).md)
[![](https://img.shields.io/badge/中文(传统)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/chinese%20(traditional).md)
[![](https://img.shields.io/badge/arabic(العربية)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/arabic.md)
[![](https://img.shields.io/badge/español-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/spanish.md)
[![](https://img.shields.io/badge/italiano-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/italian.md)
[![](https://img.shields.io/badge/Deutsch-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/dutch.md)
[![](https://img.shields.io/badge/hindi(हिन्दी)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/hindi.md)
[![](https://img.shields.io/badge/korean(한국어)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/korean.md)


# Автоматический исследователь для Thaumcraft 4
> _**Thaumcraft**_ - мод для игры _Minecraft_, часто устанавливающийся в магические сборки модов на популярных серверах

Программа **автоматически решает и раскладывает** записки исследований в столе исследований.
Весь интерфейс взаимодействия полупрозрачный и показывается поверх всех окон.

Программа **никак** не взаимодействует с кодом игры и не определяется античитами. 
Все что она делает - это смотрит на **пиксели на экране**, и имитирует **действия мышью и клавиатурой**, как если бы это делал человек.

---

## [Releases](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
[latest version `v1.0.0`](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases/tag/v1.0.0)
<details>
<summary>Changelog:</summary>

- Улучшено качество решения цепочек а spectacles
- Resolution of aspect chains has been accelerated by ~2 times
- Added logging to .log files inside the executable .exe
- Added close button
</details>


For any questions, errors or suggestions, write to: [t.me/tyapkin_s](https://t.me/tyapkin_s)

## Operating procedure
### Initial setup
1. Demonstration and verification that crosshairs can be moved. 
Just move the red dot to the yellow one.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/enroll.png?raw=true)
2. You must tell the program where the research table interface is located. 
To do this, the corners of the yellow rectangle need to be moved so that they go along the outer perimeter of the table, as shown in the screenshot below
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/find_table.png?raw=true)
3. It is necessary to let the program know in more detail where the interaction buttons are located inside the enchantment table.
To do this, move all the points as shown in the screenshot below
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_controls.png?raw=true)
4. Select your Thaumcraft version and all installed addons
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_version_and_addons.png?raw=true) 

After performing all these actions, all user selections are saved,
the next time you start the program it is not necessary to do this; the next step will be shown immediately.
You can always return to the configuration by pressing the `Backspace` key

### Solving Aspect Chains
1. Research notes from the top left inventory slot will be automatically placed in the research table.
Click on an existing aspect in the field and select it from the list of aspects
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects.png?raw=true)
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects_1.png?raw=true)
2. For all other aspects, do the same, and also mark all the cells in which
aspects cannot be placed (empty). It should look similar to the screenshot below:
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects_2.png?raw=true)
3. If the aspect chain is too large or uses aspects you don't have, press `R` to regenerate it
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects_3.png?raw=true)
4. Before you begin, make sure you have enough ink in your ink tank. If they run out, the algorithm for laying out aspects will be interrupted.
Then press `Enter`, and the process of laying out aspects on the table according to the resulting chains will begin.
5. After finishing laying out the aspects, the research note will be placed in the inventory,
and instead of it in s The following from the inventory is placed.
The process can be started again. This way you can solve a large number of notes lying in the inventory one after another
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/solving_done.png?raw=true)


## In future versions
- Automatic detection of aspects on the table using a neural network.
- Automatic detection of available aspects in the table and their quantity, building chains based on this information.
- Editing source configs
- Checking the correctness of determining the initial aspects
- Checking the correctness of the laid out chains
- More supported versions and addons
- Ink tank status tracking
- Translation into other languages ​​within the application

---
## Run from source:
1. Install dependencies:
```shell
pip install -r requirements.txt
```

2. Run from the project root (requires `Python 3.10` or higher):
```shell
python ./src/main.py
```
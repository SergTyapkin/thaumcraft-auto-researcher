## [Download .exe releases](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
[latest version `v1.2.0`](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases/tag/v1.2.0)
<details>
<summary>Changelog:</summary>

- Configations are stored in Appdata. When restarting, you no longer need to re -configure the application
- Now the neural network determines the aspects on the table!
The speed of research due to this increased by more than 10 times.
- improved the speed of the neural network due to its local caching
- Added key combinations for thinner control
- Added non -stop research regime

> `v1.2._` - configuration of all aspects with several neuralities and craft of the missing

> `v1.1._` - configuration of aspects on the table with a neural network with the possibility of changing the user

> `v1.0._` - The configuration of aspects on the table by the user

> `v0 ._._` - pre -reliable mvp versions
</details>



![GithubCI](https://github.com/SergTyapkin/thaumcraft-auto-researcher/actions/workflows/auto-translate-readme.yml/badge.svg)

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



# Automatic researcher for Thaumcraft 4
> _ ** thaumcraft ** _ - a mod for the game _minecraft_, often installed in magical assembly of mods on popular servers

The program using two neural networks to determine the aspects on the screen ** algorithmically solves and lays out ** notes of research in the research table.
The entire interaction interface is translucent and is shown on top of all windows.

The program ** does not interact with the game code and is not determined by antithens.
All that she does is look at ** pixels on the screen **, with neural networks determines which aspects are on the screen, and imitates ** actions with a mouse and a keyboard **, as if a person did it.

> [!IMPORTANT]
> For any questions, errors and suggestions, write: [T.ME/TYAPKIN_S.0(https://t.me/tyapin_s)

<details>
<summary>Список поддерживаемых аддонов (развернуть...)</summary>

- Magic Bees
- Forbidden Magic
- Greed
- Grumping
- Gregtech Newhorizons
- Thaumic Boots
- Botanical addons
- The Elysium
- Thaumic Revelations
- Essential Thaumaturgy
- AbyssalCraft Integration
</details>

https://github.com/user-attachments/assets/a2eaa3b7-c7fe-4fbc-9905-1b19a32d498f




# How to use this?
> [!CAUTION]
> Pictures and description are not suitable for the latest version of the program. It uses a similar system, but more automated. You can just follow the prompts inside the program, and everything will be clear to you.
> We will surely update the instructions below, but so far.

## preliminary setting
> _ Is filled once after the first launch of the program_
0. Download the program from [Releases] (https://github.com/sergtyapkin/thaumcraft-auto-researcher/releases)
1. Demonstration and verification that points with crossroads can be moved.
Just move the red point to the yellow.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/enroll.png?raw=true)
2. It is necessary to specify the program where the study table interface is located.
To do this, the corners of the yellow rectangle must be moved so that they walk along the outer perimeter of the table, as shown in the screenshot below
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/find_table.png?raw=true)
3. It is necessary to let the program be known in more detail where the interaction buttons are inside the enchanting table.
To do this, move all points as shown in the screenshot below
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_controls.png?raw=true)
4. Select your Thaumcraft and all installed addons
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_version_and_addons.png?raw=true) 

After performing all these actions, all the user elections are preserved in the folder `C: // Users/%User%/. Thaumcraftautoresearcher`,
At the next time the program launches, this is not necessary, the next step will be shown immediately.
You can always return to the configuration by pressing the key `Backspace`

### Solution Chain of aspects
1. ** Put a research note ** from the left upper inventory slot into the research table
After clicking on `Enter`, the process of determining aspects on the field using a neural network will start.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/prepare_to_solving_aspects.png?raw=true)
The decision of the aspect chains will be automatically generated, which the program is going to lay out
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_solved.png?raw=true)

> [!TIP]
> If the aspect chain is too large or the aspects that you do not have is used in it, click `R` to overheat it
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_rerolled.png?raw=true)

> [!TIP]
> If you need to do anything in the game so that the game does not overlap the program interface, you can press `Ctrl+Shift+space, and
The program will suspend the work before the re -pressing of this combination of keys.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/program_paused.png?raw=true)

> [!TIP]
> If any of the cells is defined incorrectly, you can click on the cell and choose what the cell really should be.
After that, the decision will be automatically overlapled
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects.png?raw=true)
2. ** Make sure that in the inkwell enough ink **. If they end, the algorithm for laying out the aspects will not stop,
And the notes of research will not be resolved.
Then click `Enter`, and the process of laying out the aspects on the table on the received chains will begin.
3. ** After the end of laying out the aspects **, a note from the study will be put in the inventory,
And instead of it, the following from the inventory is put on the table.
Then the process will be repeated again. Thus, you can solve a large number of notes lying in the inventory one after another
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/next_research_putted.png?raw=true)

> [!TIP]
> - so that the notes of research continue to be explored in turn, as they are in the inventory, you can press `ctrl+enter`, and then
When studying each next note, the program will not expect `Enter 'confirmation from the user, but immediately begin to upload a solution.

> [!TIP]
> - During the layout of the aspects, a combination of keys `ctrl+shift+alt` in case the program is urgently completed.





## in the following versions ...
- adaptive speed of work depending on FPS in the game
- checking the correctness of the lined chains
- monitoring the condition of the inkwell
- translation into other languages ​​within the application




# Launch from the source:
1. Installation of dependencies:
```shell
pip install -r requirements.txt
```

2. Add the SRC folder in Pythonpath:
Windows:
```cmd
set "PYTHONPATH=$($CWD);$($PYTHONPATH)"
```
-Unix:
```cmd
export PYTHONPATH=$(cwd):$PYTHONPATH
```

3. Starting from the root of the project (the version of `python 3.10` or higher is required):
```shell
python -m src.main
```


## assembly of the application in .exe file
1. Installation of dependencies and collector:
```shell
pip install -r requirements.txt
pip install auto-py-to-exe
```

2. *** \ [optional step] *** download UPX (reduces the size of the final exe file)
https://github.com/upx/upx/releases/


3. Launching the assembly command from the root root (will open an interface from which you can run the assembly):
```shell
auto-py-to-exe -c .\pyinstaller_configs\autoPyToExe.json
```

4. *** \ [optional step] *** In the ** advanced ** section `--uPx-dir` (location of the folder with the executable file` upx.exe`) and start the assembly.
Compiled an exe file will appear in the `Output` folder in this directory


## Separate gratitude
- [acak1221] (https://github.com/acak1221) for creating a neural network of determining aspects in the solution
- [limuranius] (https://github.com/limuranius) for creating a neural network of determining the aspects and their number in the table, and a greater work to create a lightweight system of launching neural networks
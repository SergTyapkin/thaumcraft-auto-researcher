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


# Автоматический исследователь для Thaumcraft 4
> _**Thaumcraft**_ - мод для игры _Minecraft_, часто устанавливающийся в магические сборки модов на популярных серверах
## [Download .exe releases](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
[latest version `v1.1.3`](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases/tag/v1.1.3)
<details>
<summary>Changelog:</summary>

- Configs are saved in AppData. When restarting, you no longer need to reconfigure the application
- Now the neural network determines aspects on the table!
Thanks to this, the speed of research has increased more than 10 times.
- Improved neural network speed thanks to its local caching
- Added keyboard shortcuts for finer control
- Added non-stop research mode

> `v1.1._` - configuration of aspects on the table by the neural network with the ability to be changed by the user
>
> `v1.0._` - configuration of aspects on the table by the user
>
> `v0._._` - pre-release MVP versions
</details>

---
The program, using the neural network, **automatically solves and arranges** research notes in the research table.

The entire interaction interface is translucent and is shown on top of all windows.

The program **in no way** interacts with the game code and is not detected by anti-cheats. 
All it does is look at the **pixels on the screen**, and using the neural network, imitates **mouse and keyboard actions**, as if a person were doing it.

> [!IMPORTANT]
> For any questions, errors and suggestions write: [t.me/Tyapkin_S](https://t.me/tyapkin_s)

<details>
<summary>List of supported addons (expand...)</summary>

- Magic Bees
- Forbidden Magic
- Avaritia
- GregTech
- GregTech NewHorizons
- Thaumic Boots
- Botanical addons
- The Elysium
- Thaumic Revelations
- Essential Thaumaturgy
- AbyssalCraft Integration
</details>

https://github.com/user-attachments/assets/a2eaa3b7-c7fe-4fbc-9905-1b19a32d498f

---

# How to use it?
### Preliminary setup
> _Runs once after the first launch of the program_
0. Download the program from [releases](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
1. Demonstration and verification that the dots with crosshairs can be moved.

Just move the red dot to the yellow one.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/enroll.png?raw=true)
2. You need to tell the program where the research table interface is.

To do this, the corners of the yellow rectangle need to be moved so that they go along the outer perimeter of the table, as shown in the screenshot below
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/find_table.png?raw=true)
3. You need to let the program know in more detail where the interaction buttons are inside the enchantment table.
To do this, move all the dots as shown in the screenshot below
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_controls.png?raw=true)
4. Select your Thaumcraft version and all installed add-ons
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_version_and_addons.png?raw=true)

After completing all these steps, all user choices are saved in the `C://users/%USER%/.ThaumcraftAutoResearcher` folder,
the next time you start the program, you don't have to do this, the next step will be shown immediately.
You can always return to the configuration by pressing the `Backspace` key

### Resolving aspect chains
1. **Put the research note** from the upper left inventory slot into the research table slot
After pressing `Enter`, the process of determining aspects on the field using a neural network will start.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/prepare_to_solving_aspects.png?raw=true)
The solution will be automatically generated by the aspect chains that the program is about to post
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_solved.png?raw=true)

> [!TIP]
> If the aspect chain is too long or uses aspects that you do not have, press `R` to regenerate it
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_rerolled.png?raw=true)

> [!TIP]
> If you need to do something in the game so that the game is not blocked by the program interface, you can press `Ctrl+Shift+Space`, and
the program will pause until you press this key combination again.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/program_paused.png?raw=true)

> [!TIP]
> If any of the cells are defined incorrectly, you can click on the cell and select what the cell should actually bea.
After that, the solution will be automatically regenerated
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects.png?raw=true)
2. **Make sure there is enough ink in the inkwell**. If it runs out, the aspect placement algorithm will not stop,
and the research notes will not be solved.
Then press `Enter`, and the process of placing aspects on the table will begin according to the received chains.
3. **After finishing placing aspects**, the research note will be placed in the inventory,
and the next one from the inventory will be placed in the table instead.
Then the process will repeat again. In this way, you can solve a large number of notes lying in the inventory one after another
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/next_research_putted.png?raw=true)

> [!TIP]
> - To continue to study research notes in turn, as they are in the inventory, you can press `Ctrl+Enter`, and then
when studying each next note, the program will not wait for the user to confirm with the `Enter` key, but will immediately begin to lay out the solution.

> [!TIP]
> - When laying out aspects, the `Ctrl+Shift+Alt` key combination is provided in case it is necessary to urgently terminate the program.

----------

## In the following versions...
- Auto-detection of existing aspects in the table and their number, building chains based on this information.
- Adaptive speed depending on the FPS in the game
- Checking the correctness of the posted chains
- Tracking the inkwell state
- Translation into other languages ​​​​in the application

----------

# Launch from sources:
1. Installing dependencies:
```shell
pip install -r requirements.txt
```

2. Launching from the project root (requires `Python 3.10` or higher):
```shell
python ./src/main.py
```

---
## Building the application into an .exe file
1. Installing dependencies and the collector:
```shell
pip install -r requirements.txt
pip install auto-py-to-exe
```

2. ***\[Optional step]*** Download UPX (reduces the size of the resulting exe file)
https://github.com/upx/upx/releases/

3. Run the build command from the project root (will open an interface from which you can run the build):
```shell
auto-py-to-exe -c .\pyinstaller_configs\autoPyToExe.json
```

4. ***\[Optional step]*** In the **Advanced** section, specify `--upx-dir` (location of the folder with the executable file `upx.exe`) and run the build.
The compiled exe file will appear in the `output` folder in this directory

---
### Special thanks
- [Acak1221](https://github.com/acak1221) for creating the neural network that the program uses
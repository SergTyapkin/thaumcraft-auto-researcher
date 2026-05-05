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



# Automatic explorer for Thaumcraft 4

[![Download latest .exe](https://dabuttonfactory.com/button.png?t=Download+latest++.exe&f=Open+Sans-Bold&ts=20&tc=fff&w=300&h=60&c=round&bgt=gradient&bgc=6B6BFF&ebgc=BB8EFF)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases/tag/v1.2.1)
<br> [![see all releases](https://dabuttonfactory.com/button.png?t=see+all+releases&f=Open+Sans-Bold-Italic&ts=12&tc=fff&w=300&h=16&c=round&bgt=gradient&bgc=2B8F3B&ebgc=5BBB3F)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
<details>
<summary>Changelog:</summary>

- Added support for various languages ​​within the program
- Configs are saved in AppData. When restarting, you no longer need to reconfigure the application
- Now the neural network determines the aspects on the table!
Thanks to this, the speed of research has increased more than 10 times.
- Improved speed of the neural network thanks to its local caching
- Added keyboard shortcuts for finer control
- Added non-stop research mode

> `v1.2._` - configuration of all aspects using several neural networks and crafting the missing ones

> `v1.1._` - configuration of aspects on the table by a neural network with the ability to be changed by the user

> `v1.0._` - configuration of aspects on the table by the user

> `v0._._` - pre-release MVP versions
</details>

> _**Thaumcraft**_ is a mod for the game _Minecraft_, often installed in magic mod assemblies on popular servers

The program, using two neural networks to determine aspects on the screen, **algorithmically solves and arranges** research notes in the research table.
The entire interaction interface is translucent and appears on top of the game window.

The program does not interact **in any way** with the game code and is not detected by anti-cheats.
All it does is look at **pixels on the screen**, use neural networks to determine what aspects are on the screen, and **imitate mouse and keyboard actions** as if a human were doing it.

> [!IMPORTANT]
> For any questions, errors and suggestions, write: [t.me/Tyapkin_S](https://t.me/tyapkin_s)

<details>
<summary>Список поддерживаемых аддонов (развернуть...)</summary>

- Magic Bees
- Forbidden Magic
- Greed
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




# How to use this?
> [!CAUTION]
> Pictures and descriptions do not match the latest version of the program. It uses a similar system, but more automated. You can simply follow the prompts inside the program and everything will be clear to you.
> We will definitely update the instructions below, but that's it for now.

### Preset
> _Executed once after the first start of the program_
0. Download the program from [releases](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
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

After completing all these steps, all user selections are saved in the `C://users/%USER%/.ThaumcraftAutoResearcher` folder,
the next time you start the program it is not necessary to do this; the next step will be shown immediately.
You can always return to the configuration by pressing the `Backspace` key

### Solving Aspect Chains
1. **Put a research note** from the top left inventory slot into the research table slot
After pressing `Enter`, the process of determining aspects on the field using a neural network will start.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/prepare_to_solving_aspects.png?raw=true)
A solution will be automatically generated using chains of aspects, which the program is going to post
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_solved.png?raw=true)

> [!TIP]
> If the aspect chain is too large or uses aspects you don't have, press `R` to regenerate it
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_rerolled.png?raw=true)

> [!TIP]
> If you need to do something in the game so that the game does not overlap the program interface, you can press `Ctrl+Shift+Space`, and
the program will pause until you press this key combination again.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/program_paused.png?raw=true)

> [!TIP]
> If any of the cells are defined incorrectly, you can click on the cell and select what the cell actually should be.
After this, the solution will be automatically regenerated
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects.png?raw=true)
2. **Make sure there is enough ink in the ink tank**. If they run out, the algorithm for laying out aspects will not stop,
and research notes will not be resolved.
Then press `Enter`, and the process of laying out aspects on the table according to the resulting chains will begin.
3. **After finishing laying out the aspects**, the research note will be placed in the inventory,
and instead of it, the next one from the inventory is placed on the table.
Then the process will repeat again. This way you can solve a large number of notes lying in the inventory one after another
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/next_research_putted.png?raw=true)

> [!TIP]
> - In order for research notes to continue to be examined one by one, as they are in the inventory, you can press `Ctrl+Enter`, and then
When studying each next note, the program will not wait for confirmation from the user with the `Enter` key, but will immediately begin to post the solution.

> [!TIP]
> - When laying out aspects, the key combination `Ctrl+Shift+Alt` is provided in case it is necessary to urgently terminate the program.





## In future versions...
- Adaptive speed depending on the FPS in the game
- Checking the correctness of the laid out chains
- Ink tank status tracking
- Translation into other languages ​​within the application




# Run from source:
1. Install dependencies:
```shell
pip install -r requirements.txt
```

2. Add the project src folder to PYTHONPATH:
Windows:
```cmd
set "PYTHONPATH=$($CWD);$($PYTHONPATH)"
```
-Unix:
```cmd
export PYTHONPATH=$(cwd):$PYTHONPATH
```

3. Run from the project root (requires `Python 3.10` or higher):
```shell
python -m src.main
```


## Build the application into an .exe file
1. Install dependencies and builder:
```shell
pip install -r requirements.txt
pip install auto-py-to-exe
```

2. ***\[Optional step]*** Download UPX (reduces the size of the final exe file)
https://github.com/upx/upx/releases/


3. Run the build command from the project root (will open an interface from which you can run the build):
```shell
auto-py-to-exe -c .\pyinstaller_configs\autoPyToExe.json
```

4. ***\[Optional step]*** In the **Advanced** section, specify `--upx-dir` (the location of the folder with the `upx.exe` executable file) and run the build.
The compiled exe file will appear in the `output` folder in this directory


### Special thanks
- [Acak1221](https://github.com/acak1221) for creating a neural network for determining aspects in a solution
- [Limuranius](https://github.com/Limuranius) for creating a neural network for determining aspects and their number in the table, and a lot of work on creating a lightweight system for launching neural networks
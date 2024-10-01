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


# Thaumcraft 4 的自动浏览器
> _**Thaumcraft**_ 是游戏 _Minecraft_ 的一个模组，通常安装在流行服务器上的魔法模组组件中
## [Download .exe releases](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
[latest version `v1.1.2`](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases/tag/v1.1.2)
<details>
<summary>更改日志：</summary>

- 配置保存在AppData中。重启时，不再需要重新配置应用程序
- 现在神经网络决定了桌面上的各个方面！
得益于此，研究速度提高了十倍以上。
- 由于其本地缓存，提高了神经网络的速度
- 添加了键盘快捷键以实现更精细的控制
- 新增不间断研究模式

> `v1.1._` - 通过神经网络对表上的方面进行配置，并且能够由用户更改
>
> `v1.0._` - 用户在表上配置方面
>
> `v0._._` - 预发布 MVP 版本
</details>

---
该程序使用神经网络，**自动解决**研究笔记并在研究表中排列**。
整个交互界面是半透明的，出现在所有窗口的上方。

该程序不会**以任何方式**与游戏代码交互，并且不会被反作弊程序检测到。 
它所做的只是查看**屏幕上的像素**，并在神经网络的帮助下模拟**使用鼠标和键盘的动作**，就像一个人在做一样。

> [!重要]
> 如有任何问题、错误和建议，请写信：[t.me/Tyapkin_S](https://t.me/tyapkin_s)

<details> <summary>支持的插件列表（展开...）</summary>

- 魔法蜜蜂
- 禁忌魔法
- 阿瓦里蒂亚
- 格雷格科技
- 格雷科技新视野
- 奇术靴子
- 植物插件
- 极乐世界
- 奇术启示
- 基本奇术
- 深渊工艺整合
</details>

https://github.com/user-attachments/assets/a2eaa3b7-c7fe-4fbc-9905-1b19a32d498f

---


# 如何使用这个？
### 预设 
> _程序第一次启动后执行一次_
0.从[releases](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)下载程序
1. 十字准线可移动的演示与验证。 
只需将红点移动到黄点即可。
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/enroll.png?raw=true)
2. 您必须告诉程序研究表界面所在的位置。 
为此，需要移动黄色矩形的角，使其沿着表格的外周，如下面的屏幕截图所示
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/find_table.png?raw=true)
3. 有必要让程序更详细地知道交互按钮位于结界表内的位置。
为此，请移动所有点，如下面的屏幕截图所示
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_controls.png?raw=true)
4.选择您的Thaumcraft版本和所有已安装的插件
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_version_and_addons.png?raw=true) 

完成所有这些步骤后，所有用户选择都保存在 `C://users/%USER%/.ThaumcraftAutoResearcher` 文件夹中，
下次启动程序时无需执行此操作；将立即显示下一步。
您可以随时按“Backspace”键返回配置

### 解决方面链
1. **将研究笔记**从左上角的库存栏位放入研究桌栏位
按“Enter”后，将开始使用神经网络确定现场情况的过程。
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/prepare_to_solving_aspects.png?raw=true)
将使用程序将发布的方面链自动生成解决方案 ![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_solved.png?raw=true)

> [!提示]
> 如果切面链太大或使用了您没有的切面，请按“R”重新生成它
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_rerolled.png?raw=true)

> [!提示]
> 如果你需要在游戏中做一些事情，让游戏不与程序界面重叠，可以按`Ctrl+Shift+Space`，然后
程序将暂停，直到您再次按下该组合键。
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/program_paused.png?raw=true)

> [!提示]
> 如果任何单元格定义不正确，您可以单击该单元格并选择该单元格的实际内容。
之后，解决方案将自动重新生成
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects.png?raw=true)
2. **确保墨盒中有足够的墨水**。如果它们用完，布局方面的算法将不会停止，
和研究笔记不会得到解决。
然后按“Enter”，根据生成的链在表格上布置方面的过程将开始。
3. **布置完各个方面**后，研究笔记将被放入库存中，
而不是它，而是将库存中的下一个放在桌子上。
然后该过程将再次重复。这样你就可以依次解决库存中的大量纸币
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/next_research_putted.png?raw=true)

> [!提示]
> - 为了继续一项一项地检查研究笔记，因为它们在清单中，您可以按“Ctrl+Enter”，然后
当学习下一个注释时，程序不会等待用户使用“Enter”键确认，而是立即开始发布解决方案。

> [!提示]
> - 布置切面时，提供组合键“Ctrl+Shift+Alt”，以防需要紧急终止程序。


----------


## 在未来的版本中...
- 自动检测表中的可用方面及其数量，并根据此信息构建链。
- 根据游戏中的 FPS 自适应速度
- 检查布置的链条的正确性
- 墨水罐状态跟踪
- 里面翻译成其他语言 应用


----------

# 从源代码运行：
1.安装依赖项：
```shell
pip install -r requirements.txt
```

2. 从项目根运行（需要`Python 3.10`或更高版本）：
```shell
python ./src/main.py
```

---
## 将应用程序构建为 .exe 文件
1. 安装依赖项和构建器：
```shell
pip install -r requirements.txt
pip install auto-py-to-exe
```

2. ***\[可选步骤]*** 下载UPX（减少最终exe文件的大小）
https://github.com/upx/upx/releases/


3. 从项目根目录运行构建命令（将打开一个可以运行构建的界面）：
```shell
auto-py-to-exe -c .\pyinstaller_configs\autoPyToExe.json
```

4. ***\[可选步骤]*** 在 **高级** 部分中，指定 `--upx-dir` （包含 `upx.exe` 可执行文件的文件夹的位置）并运行构建。
编译后的exe文件会出现在该目录下的`output`文件夹中

---
### 特别感谢
- [Acak1221](https://github.com/acak1221) 用于创建程序使用的神经网络
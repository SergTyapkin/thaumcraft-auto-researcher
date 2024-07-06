![GithubCI](https://github.com/SergTyapkin/thaumcraft-auto-researcher/actions/workflows/auto-translate-readme.yml/badge.svg)

[![](https://img.shields.io/badge/русский-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/Russian.md)
[![](https://img.shields.io/badge/english-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/english.md)
[![](https://img.shields.io/badge/中文(简体)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/chinese%20(simplified).md)
[![](https://img.shields.io/badge/中文(传统)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/chinese%20(繁體).md)
[![](https://img.shields.io/badge/arabic(العربية)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/arabic.md)
[![](https://img.shields.io/badge/español-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/spanish.md)
[![](https://img.shields.io/badge/italiano-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/italian.md)
[![](https://img.shields.io/badge/Deutsch-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/dutch.md)
[![](https://img.shields.io/badge/hindi(हिन्दी)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/hindi.md)
[![](https://img.shields.io/badge/korean(한국어)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/korean.md)


# Автоматический исследователь для Thaumcraft 4
> _**Thaumcraft**_ - мод для игры _Minecraft_, часто устанавливающийся в магические сор

Програма **автоматически решает 和 раскладывает** записки исследований в столе иски исследований в столе иски исследовани
Весь интерфейс взаимодействия полупрозрачный 和 показывается поверх всехокон。

Програма **никак** не взаимодействует с кодом игры и и не определяется античитами. 
Все что она делает - это смотрит на **пиксели на экране**, имитирует **действи то ал человек。

---

## [Releases](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
[latest version `v1.0.0`](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases/tag/v1.0.0)
<details>
<summary>更改日誌：</summary>

- Улучшено качество решения цепочек а 眼鏡
- 方面鏈的解析速度加快了約 2 倍
- 新增了可執行檔 .exe 內的 .log 檔案的日誌記錄
- 新增關閉按鈕
</details>


如有任何問題、錯誤或建議，請寫信至：[t.me/tyapkin_s](https://t.me/tyapkin_s)

＃＃ 操作方法
＃＃＃ 初始設置
1. 十字準線可移動的示範與驗證。 
只需將紅點移到黃點即可。
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/enroll.png?raw=true)
2. 您必須告訴程式研究表介面所在的位置。 
為此，需要移動黃色矩形的角，使它們沿著表格的外周，如下面的螢幕截圖所示
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/find_table.png?raw=true)
3. 有必要讓程式更詳細地知道互動按鈕位於結界表內的位置。
為此，請移動所有點，如下面的螢幕截圖所示
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_controls.png?raw=true)
4.選擇您的Thaumcraft版本和所有已安裝的插件
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_version_and_addons.png?raw=true) 

執行所有這些操作後，所有使用者選擇都會被儲存，
下次啟動程序時無需執行此操作；將立即顯示下一步。
您可以隨時按下「Backspace」鍵返回配置

### 解決方面鏈
1.左上角庫存欄位的研究筆記將自動放置在研究表中。
點擊欄位中的現有方面並從方面清單中選擇它
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects.png?raw=true)
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects_1.png?raw=true)
2. 對於所有其他方面，執行相同的操作，並標記其中的所有儲存格
無法放置方面（空）。它應該類似於下面的螢幕截圖：
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects_2.png?raw=true)
3. 如果切面鏈太大或使用了您沒有的切面，請按「R」重新產生它
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects_3.png?raw=true)
4. 開始之前，請確保墨水盒中有足夠的墨水。如果它們用完，佈置方面的演算法將被中斷。
然後按下“Enter”，根據生成的鏈在表格上佈置方面的過程將開始。
5. 佈置完各個面向後，研究筆記將被放入庫存中，
而不是 s 中的它 放置以下物品。
該過程可以再次開始。這樣你就可以依序解決庫存中的大量紙幣
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/solving_done.png?raw=true)


## 在未來的版本中
- 使用神經網路自動偵測桌面上的各個方面。
- 自動檢測表中可用的方面及其數量，並根據此資訊建立鏈。
- 編輯來源配置
- 檢查確定初始方面的正確性
- 檢查佈置的鏈條的正確性
- 更多支援的版本和插件
- 墨水罐狀態跟踪
- 在應用程式內翻譯成其他語言

---
## 從原始碼運行：
1.安裝依賴項：
編碼區塊

2. 從專案根運行（需要`Python 3.10`或更高版本）：
編碼區塊
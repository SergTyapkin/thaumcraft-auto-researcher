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

Программа с помощью нейросети **автоматически решает и раскладывает** записки исследований в столе исследований.
Весь интерфейс взаимодействия полупрозрачный и показывается поверх всех окон.

Программа **никак** не взаимодействует с кодом игры и не определяется античитами. 
Все что она делает - это смотрит на **пиксели на экране**, и с помощью нейросети имитирует **действия мышью и клавиатурой**, как если бы это делал человек.

https://github.com/user-attachments/assets/a2eaa3b7-c7fe-4fbc-9905-1b19a32d498f


---

## [Download .exe releases](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
[latest version `v1.1.0`](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases/tag/v1.1.0)
<details>
<summary>Changelog:</summary>

- Теперь нейросеть определяет аспекты на столе!
Скорость исследований благодаря этому увеличилась более чем в 10 раз.
- Добавлены сочетания клавиш для более тонкого управления
- Добавлен безостановочный режим исследования
</details>


По любым вопросам, ошибкам и предложениям пишите: [t.me/tyapkin_s](https://t.me/tyapkin_s)

## Порядок работы
### Предварительная настройка 
> _Выполняется один раз после первого запуска программы_
1. Демонстрация и проверка того, что точки с перекрестьями можно двигать. 
Просто передвиньте красную точку на желтую.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/enroll.png?raw=true)
2. Необходимо указать программе, где находится интерфейс стола исследований. 
Для этого углы желтого прямоугольника необходимо передвинуть так, чтобы они шли по внешнему периметру стола, как показано на скриншоте ниже
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/find_table.png?raw=true)
3. Необходимо более детально дать знать программе, где внутри стола зачарований находятся кнопки взаимодействия.
Для этого передвиньте все точки, как показано на скриншоте ниже
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_controls.png?raw=true)
4. Выберите версию вашего Thaumcraft и все установленные аддоны
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_version_and_addons.png?raw=true) 

После выполнения всех этих действий, все выборы пользователя сохраняюся,
при следующем запуске программы это делать не обязательно, будет показан сразу следующий шаг.
Вернуться к конфигурации всегда можно, нажав клавишу `Backspace`

### Решение цепочек аспектов
1. **Положите записку исследований** из левого верхнего слота инвентаря в слот стола исследований
После нажатия на `Enter` запустится процесс определения аспектов на поле с помощью нейросети.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/prepare_to_solving_aspects.png?raw=true)
Автоматически будет сгенерировано решение цепочками аспектов, которое программа собирается выложить
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_solved.png?raw=true)
> - Если цепочка аспектов слишком большая или в ней используются аспекты, которых у вас нет, нажмите `R`, чтобы перегенерировать её
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_rerolled.png?raw=true)

> - Если необходимо сделать что-либо в игре так, чтобы игру не перекрывал интерфейс программы, можно нажать `Ctrl+Shift+Пробел`, и
программа приостановит работу до повторного нажатия этого сочетания клавиш.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/program_paused.png?raw=true)

> - Если какие-либо из ячеек определены неверно, на ячейку можно кликнуть и выбрать, какой на самом деле должна быть ячейка.
После этого решение будет автоматически перегенерировано
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects.png?raw=true)
2. **Убедитесь, что в чернильнице достаточно чернил**. Если они закончатся, алгоритм выкладывания аспектов не остановится,
а записки исследований не будут решены.
Затем нажмите `Enter`, и начнется процесс выкладывания аспектов на стол по полученным цепочкам.
3. **После окончания выкладывания аспектов**, записка исследований будет положена в инвентарь,
а вместо неё в стол положена следующая из инвентаря.
Затем процесс повторится заново. Таким образом можно решать большое количество записок, лежащих в инвентаре друг за другом
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/next_research_putted.png?raw=true)
> - Чтобы записки исследований продолжали исследоваться по очереди, как они лежат в инвентаре, можно нажать `Ctrl+Enter`, и тогда
при изучении каждой следующей записки программа не будет ждать от пользователя подтверждения клавишей `Enter`, а сразу начнет выкладывать решение.

> - Во время выкладывания аспектов предусмотрено сочетание клавиш `Ctrl+Shift+Alt` на случай, если необходимо экстренно завершить программу.


----------


## В следующих версиях
- Автоопределение имеющихся аспектов в столе и их количества, выстраивание цепочек на основе этой информации.
- Адаптивная скорость работы в зависимости от FPS в игре
- Проверка корректности выложенных цепочек
- Отслеживание состояния чернильницы
- Перевод на другие языки внутри приложения


----------

## Запуск из исходников:
1. Установка зависимостей:
```shell
pip install -r requirements.txt
```

2. Запуск из корня проекта (требуется версия `Python 3.10` или выше):
```shell
python ./src/main.py
```

---
## Сборка приложения в .exe файл
1. Установка зависимостей и сборщика:
```shell
pip install -r requirements.txt
pip install auto-py-to-exe
```

2. ***\[Необязательный шаг]*** Скачивание UPX (уменьшает размер итогового exe-файла)
https://github.com/upx/upx/releases/


3. Запуск команды сборки из корня проекта (откроет интерфейс, из которого можно будет запустить сборку):
```shell
auto-py-to-exe -c .\pyinstaller_configs\autoPyToExe.json
```

4. ***\[Необязательный шаг]*** В разделе **Advanced** указать `--upx-dir` (расположение папки с исполняемым файлом `upx.exe`) и запустить сборку.
Скомпилированный exe-файл появится в папке `output` в этой директории

---
### Отдельная благодарность
- [Acak1221](https://github.com/acak1221) за создание нейросети, которую использует программа

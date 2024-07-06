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
> _**Thaumcraft**__ - мод для игры _Minecraft_, часто устанавливаемый в магические сборки модов на популярных серверах

Программа **автоматически определяет и раскладывает** записи исследований в таблице исследований.
Весь интерфейс взаимодействия полупрозрачен и открывается над поверхностью всех окон.

Программа **никак** не взаимодействует с кодом игры и не определяется античитами. 
Все, что она делает - это изображено на **пикселях на экране**, и имитирует **действие мышью и клавиатурой**, как если бы это делал человек.

---

## [Releases](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
[latest version `v1.0.0`](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases/tag/v1.0.0)
<details>
<summary>Изменение:</summary>

- Улучшение качества решения цепочек а спектов
- Ускорено решение цепочек аспектов в ~2 раза
- Добавлено логирование в .log-файлы внутри исполняемого .exe
- Добавлена кнопка закрытия
</details>


По любым вопросам, ошибкам и предложениям пишите: [t.me/tyapkin_s](https://t.me/tyapkin_s)

## Порядок работы
### Первоначальная настройка
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
1. Записки исследований из левого верхнего слота инвентаря будут автоматически положены в стол исследований.
Кликните на существующий аспект на поле и выберите его из списка аспектов
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects.png?raw=true)
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects_1.png?raw=true)
2. Для всех остальных аспектов сделайте то же самое, а так же отметьте все ячейки, в которые
аспекты нельзя класть (пустые). Должно получиться аналогично скриншоту ниже:
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects_2.png?raw=true)
3. Если цепочка аспектов слишком большая или в ней используются аспекты, которых у вас нет, нажмите `R`, чтобы перегенерировать её
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects_3.png?raw=true)
4. Прежде чем начать, убедитесь, что в чернильнице достаточно чернил. Если они закончатся, алгоритм выкладывания аспектов будет прерван.
Затем нажмите `Enter`, и начнется процесс выкладывания аспектов на стол по полученным цепочкам.
5. После окончания выкладывания аспектов, записка исследований будет положена в инвентарь,
а вместо неё в с тол положена следующая из инвентаря.
Процесс можно начинать заново. Таким образом можно решать большое количество записок, лежащих в инвентаре друг за другом
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/solving_done.png?raw=true)


## В следующих версиях
- Автоопределение аспектов на столе с помощью нейросети.
- Автоопределение имеющихся аспектов в столе и их количества, выстраивание цепочек на основе этой информации.
- Редактирование исходных конфигов
- Проверка корректности определения исходных аспектов
- Проверка корректности выложенных цепочек
- Больше поддерживаемых версий и аддонов
- Отслеживание состояния чернильницы
- Перевод на другие языки внутри приложения

---
## Запуск из исходников:
1. Установка зависимостей:
```shell
pip install -r requirements.txt
```

2. Запуск из корня проекта (требуется версия `Python 3.10` или выше):
```shell
python ./src/main.py
```
![GithubCI](https://github.com/SergTyapkin/thaumcraft-auto-researcher/actions/workflows/auto-translate-readme.yml/badge.svg)

[![](https://img.shields.io/badge/русский-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLACIONES/russian.md)
[![](https://img.shields.io/badge/english-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLACIONES/english.md)
[![](https://img.shields.io/badge/中文(简体)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATION/chinese%20(simplified).md)
[![](https://img.shields.io/badge/中文(传统)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLACIONES/chinese%20(traditional).md)
[![](https://img.shields.io/badge/arabic(العربية)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLACIONES/arabic.md)
[![](https://img.shields.io/badge/español-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLACIONES/spanish.md)
[![](https://img.shields.io/badge/italiano-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLACIONES/italian.md)
[![](https://img.shields.io/badge/Deutsch-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLACIONES/dutch.md)
[![](https://img.shields.io/badge/hindi(हिन्दी)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLACIONES/hindi.md)
[![](https://img.shields.io/badge/korean(한국어)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLACIONES/korean.md)


# Автоматический исследователь для Thaumcraft 4
> _**Thaumcraft**_ - modo para juegos _Minecraft_, que se instala en modos de juegos mágicos en servidores populares

Программа **автоматически решает and раскладывает** записки исследований в столе исследований.
Весь интерфейс взаимодействия полупрозрачный и показывается поверх всех окон.

Программа **никак** не взаимодействует с кодом игры и не определяется античитами. 
Все что она делает - это смотрит на **пиксели на экране**, и имитирует **действия мышью и клавиатурой**, как если бы это чел овек.

---

## [Releases](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
[latest version `v1.0.0`](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases/tag/v1.0.0)
<details>
<summary>Registro de cambios:</summary>

- Улучшено качество решения цепочек а gafas
- La resolución de las cadenas de aspectos se ha acelerado aproximadamente 2 veces.
- Se agregó registro a archivos .log dentro del ejecutable .exe
- Añadido botón de cerrar
</details>


Para cualquier duda, error o sugerencia escribe a: [t.me/tyapkin_s](https://t.me/tyapkin_s)

## Procedimiento de operación
### Configuración inicial
1. Demostración y verificación de que el punto de mira se puede mover. 
Simplemente mueva el punto rojo al amarillo.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/enroll.png?raw=true)
2. Debes indicarle al programa dónde se encuentra la interfaz de la mesa de investigación. 
Para hacer esto, las esquinas del rectángulo amarillo deben moverse para que vayan a lo largo del perímetro exterior de la mesa, como se muestra en la siguiente captura de pantalla.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/find_table.png?raw=true)
3. Es necesario informarle al programa con más detalle dónde se encuentran los botones de interacción dentro de la mesa de encantamientos.
Para hacer esto, mueva todos los puntos como se muestra en la captura de pantalla a continuación.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_controls.png?raw=true)
4. Seleccione su versión de Thaumcraft y todos los complementos instalados.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_version_and_addons.png?raw=true) 

Después de realizar todas estas acciones, se guardan todas las selecciones del usuario,
la próxima vez que inicie el programa no es necesario hacerlo; el siguiente paso se mostrará inmediatamente.
Siempre puedes volver a la configuración presionando la tecla `Retroceso`

### Resolver cadenas de aspectos
1. Las notas de investigación del espacio superior izquierdo del inventario se colocarán automáticamente en la mesa de investigación.
Haga clic en un aspecto existente en el campo y selecciónelo de la lista de aspectos.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects.png?raw=true)
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects_1.png?raw=true)
2. Para todos los demás aspectos, haga lo mismo y marque también todas las celdas en las que
Los aspectos no se pueden colocar (vacíos). Debería verse similar a la captura de pantalla siguiente:
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects_2.png?raw=true)
3. Si la cadena de aspectos es demasiado grande o usa aspectos que no tienes, presiona `R` para regenerarla.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects_3.png?raw=true)
4. Antes de comenzar, asegúrese de tener suficiente tinta en el tanque de tinta. Si se agotan, se interrumpirá el algoritmo de disposición de aspectos.
Luego presione "Entrar" y comenzará el proceso de disposición de aspectos en la tabla de acuerdo con las cadenas resultantes.
5. Luego de terminar de exponer los aspectos, la nota de investigación se colocará en el inventario,
y en lugar de eso en s Se coloca lo siguiente del inventario.
El proceso se puede iniciar de nuevo. De esta forma podrás resolver una gran cantidad de notas que se encuentran en el inventario, una tras otra.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/solving_done.png?raw=true)


## En futuras versiones
- Detección automática de aspectos sobre la mesa mediante red neuronal.
- Detección automática de aspectos disponibles en la tabla y su cantidad, construyendo cadenas en base a esta información.
- Edición de configuraciones de origen
- Comprobar la exactitud de la determinación de los aspectos iniciales.
- Comprobar la corrección de las cadenas dispuestas.
- Más versiones y complementos compatibles
- Seguimiento del estado del tanque de tinta
- Traducción a otros idiomas dentro de la aplicación

---
## Ejecutar desde la fuente:
1. Instalar dependencias:
```shell
pip install -r requirements.txt
```

2. Ejecute desde la raíz del proyecto (requiere `Python 3.10` o superior):
```shell
python ./src/main.py
```
![GithubCI](https://github.com/SergTyapkin/thaumcraft-auto-researcher/actions/workflows/auto-translate-readme.yml/badge.svg)

[![](https://img.shields.io/badge/русский-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/russian_README.md)
[_MD_WDGT_c1fca2ee0d6b4a0da9f76 474abf0221e](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/english_README.md)
[![](https://img.shields.io/badge/中文(简体)-_?style=para-la-insignia&logotipo=readme&color=blanco)](https://github. com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/chino(simplificado)_README.md)
[![](https://img.shields.io/badge/中文(传统)-_?style=para-la-insignia&logotipo=readme&color=blanco)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/chino(tradicional)_README.md)
[![](https://img.shields.io/badge/arabic(العربية)-_?style=para-la-insignia&logotipo=readme&color=blanco)](https://github.com/SergTyapkin/thaumcraf t-auto-researcher/blob/README_TRANSLATIONS/README_arabic.md)
[![](https://img.shields.io/badge/español-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/README_spanish.md)
[_MD_WDGT_f58 6f5b3e23c42488ca37adc8a28bbd2](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/italian_README.md)
[![](https://img.shields.io/badge/Deutsch-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-au para-investigador/blob/README_TRANSLATIONS/dutch_README.md)
[![](https://img.shields.io/badge/hindi(हिन्दी)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/hindi_README.md)
[![](https://img.shields.io/badge/korean(한국어)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/korean_README.md)

# Aplicación automática para Thaumcraft 4 > _**Thaumcraft**_ - modo para juegos _Minecraft_, que se instala en modos mágicos populares ых serveras
## [Descargar versiones .exe](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
[última versión `v1.1.3`](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases/tag/v1.1.3)
<details>
<summary>Registro de cambios:</summary>

- Las configuraciones se guardan en AppData. Al reiniciar, ya no es necesario volver a configurar la aplicación.
- ¡Ahora la red neuronal determina los aspectos sobre la mesa!
Gracias a esto, la velocidad de la investigación se ha multiplicado por más de 10.
- Velocidad mejorada de la red neuronal gracias a su almacenamiento en caché local
- Se agregaron atajos de teclado para un control más preciso.
- Se agregó el modo de investigación sin parar.

> `v1.1._` - configuración de aspectos en la mesa mediante una red neuronal con la capacidad de ser cambiado por el usuario
>
> `v1.0._` - configuración de aspectos en la mesa por parte del usuario
>
> `v0._._` - versiones preliminares de MVP
</details>

---
El programa, utilizando una red neuronal, **resuelve y organiza** automáticamente las notas de investigación en la tabla de investigación.
Toda la interfaz de interacción es translúcida y aparece encima de todas las ventanas.

El programa no interactúa **de ninguna manera** con el código del juego y no es detectado por los anti-trampas. 
Lo único que hace es mirar **píxeles de la pantalla**, y con la ayuda de una red neuronal simula **acciones con el mouse y el teclado**, como si lo estuviera haciendo una persona.

> [!IMPORTANTE]
> Para cualquier duda, error y sugerencia escribe: [t.me/Tyapkin_S](https://t.me/tyapkin_s)

<details>
<summary>Lista de complementos compatibles (ampliar...)</summary>

- Abejas Mágicas
- Magia Prohibida
- Avaritia
- GregTech
- GregTech Nuevos Horizontes
- Botas Taumicas
- Complementos botánicos
- El Elíseo
- Revelaciones Taumicas
- Taumaturgia esencial
- Integración de AbyssalCraft
</details>

https://github.com/user-attachments/assets/a2eaa3b7-c7fe-4fbc-9905-1b19a32d498f

---


# ¿Cómo usar esto?
### Preestablecido 
> _Ejecutado una vez después del primer inicio del programa_
0. Descargue el programa desde [lanzamientos](https://github.com/SergTyapken/thaumcraft-auto-researcher/lanzamientos)
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

Después de completar todos estos pasos, todas las selecciones de los usuarios se guardan en la carpeta `C://users/%USER%/.ThaumcraftAutoResearcher`,
la próxima vez que inicie el programa no es necesario hacerlo; el siguiente paso se mostrará inmediatamente.
Siempre puedes volver a la configuración presionando la tecla `Retroceso`

### Resolver cadenas de aspectos
1. **Coloque una nota de investigación** desde el espacio superior izquierdo del inventario en el espacio de la mesa de investigación.
Después de presionar "Enter", se iniciará el proceso de determinación de aspectos en el campo utilizando una red neuronal.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/prepare_to_solving_aspects.png?raw=true)
Se generará automáticamente una solución mediante cadenas de aspectos, que el programa irá publicando
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_solved.png?raw=true)

> [!CONSEJO]
> Si la cadena de aspectos es demasiado grande o usa aspectos que no tienes, presiona `R` para regenerarla
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_rerolled.png?raw=true)

> [!CONSEJO]
> Si necesitas hacer algo en el juego para que el juego no se superponga a la interfaz del programa, puedes presionar `Ctrl+Shift+Espacio`, y
el programa se detendrá hasta que presione esta combinación de teclas nuevamente.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/program_paused.png?raw=true)

> [!CONSEJO]
> Si alguna de las celdas está definida incorrectamente, puede hacer clic en la celda y seleccionar qué celda debería estar realmenteA.
Después de esto, la solución se regenerará automáticamente.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects.png?raw=true)
2. **Asegúrese de que haya suficiente tinta en el tanque de tinta**. Si se agotan, el algoritmo de disposición de aspectos no se detendrá,
y las notas de investigación no se resolverán.
Luego presione "Entrar" y comenzará el proceso de disposición de aspectos en la tabla de acuerdo con las cadenas resultantes.
3. **Después de terminar de exponer los aspectos**, la nota de investigación se colocará en el inventario,
y en su lugar, se coloca sobre la mesa el siguiente del inventario.
Luego el proceso se repetirá nuevamente. De esta forma podrás resolver una gran cantidad de notas que se encuentran en el inventario, una tras otra.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/next_research_putted.png?raw=true)

> [!CONSEJO]
> - Para que las notas de investigación continúen siendo examinadas una por una, tal como están en el inventario, puede presionar `Ctrl+Enter` y luego
Al estudiar cada nota siguiente, el programa no esperará la confirmación del usuario con la tecla "Enter", sino que inmediatamente comenzará a publicar la solución.

> [!CONSEJO]
> - Al diseñar aspectos, se proporciona la combinación de teclas `Ctrl+Shift+Alt` en caso de que sea necesario finalizar urgentemente el programa.


----------


## En futuras versiones...
- Detección automática de aspectos disponibles en la tabla y su cantidad, construyendo cadenas en base a esta información.
- Velocidad adaptable dependiendo del FPS en el juego.
- Comprobar la corrección de las cadenas dispuestas.
- Seguimiento del estado del tanque de tinta
- Traducción a otros idiomas dentro de la aplicación


----------

# Ejecutar desde la fuente:
1. Instalar dependencias:
```shell
pip install -r requirements.txt
```

2. Ejecute desde la raíz del proyecto (requiere `Python 3.10` o superior):
```shell
python ./src/main.py
```

---
## Construya la aplicación en un archivo .exe
1. Instale dependencias y constructor:
```shell
pip install -r requirements.txt
pip install auto-py-to-exe
```

2. ***\[Paso opcional]*** Descargue UPX (reduce el tamaño del archivo exe final)
https://github.com/upx/upx/releases/


3. Ejecute el comando de compilación desde la raíz del proyecto (se abrirá una interfaz desde la cual puede ejecutar la compilación):
```shell
auto-py-to-exe -c .\pyinstaller_configs\autoPyToExe.json
```

4. ***\[Paso opcional]*** En la sección **Avanzado**, especifique `--upx-dir` (la ubicación de la carpeta con el archivo ejecutable `upx.exe`) y ejecute la compilación.
El archivo exe compilado aparecerá en la carpeta `output` en este directorio

---
### Gracias especiales
- [Acak1221](https://github.com/acak1221) para crear la red neuronal que utiliza el programa
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



# Explorador automático para Thaumcraft 4

[![Download latest .exe](https://dabuttonfactory.com/button.png?t=Download+latest++.exe&f=Open+Sans-Bold&ts=20&tc=fff&w=300&h=60&c=round&bgt=gradient&bgc=6B6BFF&ebgc=BB8EFF)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases/tag/v1.2.1)
<br> [![see all releases](https://dabuttonfactory.com/button.png?t=see+all+releases&f=Open+Sans-Bold-Italic&ts=12&tc=fff&w=300&h=16&c=round&bgt=gradient&bgc=2B8F3B&ebgc=5BBB3F)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
<details>
<summary>Changelog:</summary>

- Se agregó soporte para varios idiomas dentro del programa.
- Las configuraciones se guardan en AppData. Al reiniciar, ya no es necesario reconfigurar la aplicación.
- ¡Ahora la red neuronal determina los aspectos sobre la mesa!
Gracias a esto, la velocidad de la investigación se ha multiplicado por más de 10.
- Velocidad mejorada de la red neuronal gracias a su almacenamiento en caché local
- Se agregaron atajos de teclado para un control más preciso.
- Se agregó el modo de investigación sin parar.

> `v1.2._` - configuración de todos los aspectos utilizando varias redes neuronales y creando las que faltan

> `v1.1._` - configuración de aspectos en la mesa mediante una red neuronal con la capacidad de ser modificado por el usuario

> `v1.0._` - configuración de aspectos en la mesa por parte del usuario

> `v0._._` - versiones preliminares de MVP
</details>

> _**Thaumcraft**_ es un mod para el juego _Minecraft_, que a menudo se instala en conjuntos de mods mágicos en servidores populares.

El programa, que utiliza dos redes neuronales para determinar aspectos en la pantalla, **resuelve y organiza algorítmicamente** notas de investigación en la tabla de investigación.
Toda la interfaz de interacción es translúcida y aparece en la parte superior de la ventana del juego.

El programa no interactúa **de ninguna manera** con el código del juego y no es detectado por los anti-trampas.
Todo lo que hace es mirar **píxeles en la pantalla**, usar redes neuronales para determinar qué aspectos hay en la pantalla e **imitar las acciones del mouse y el teclado** como si lo estuviera haciendo un humano.

> [!IMPORTANTE]
> Para cualquier duda, error y sugerencia escribe: [t.me/Tyapkin_S](https://t.me/tyapkin_s)

<details>
<summary>Список поддерживаемых аддонов (развернуть...)</summary>

- Abejas Mágicas
- Magia Prohibida
- Codicia
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




# ¿Cómo usar esto?
> [!PRECAUCIÓN]
> Las imágenes y descripciones no coinciden con la última versión del programa. Utiliza un sistema similar, pero más automatizado. Simplemente puede seguir las instrucciones dentro del programa y todo le quedará claro.
> Definitivamente actualizaremos las instrucciones a continuación, pero eso es todo por ahora.

### Preestablecido
> _Ejecutado una vez después del primer inicio del programa_
0. Descargue el programa desde [lanzamientos](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
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
la próxima vez que inicie el programa no es necesario hacer esto; El siguiente paso se mostrará inmediatamente.
Siempre puedes volver a la configuración presionando la tecla `Retroceso`

### Resolver cadenas de aspectos
1. **Coloque una nota de investigación** desde el espacio superior izquierdo del inventario en el espacio de la mesa de investigación.
Después de presionar "Enter", se iniciará el proceso de determinación de aspectos en el campo utilizando una red neuronal.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/prepare_to_solving_aspects.png?raw=true)
Se generará automáticamente una solución mediante cadenas de aspectos, que el programa irá publicando.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_solved.png?raw=true)

> [!CONSEJO]
> Si la cadena de aspectos es demasiado grande o usa aspectos que no tienes, presiona `R` para regenerarla
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_rerolled.png?raw=true)

> [!CONSEJO]
> Si necesitas hacer algo en el juego para que el juego no se superponga a la interfaz del programa, puedes presionar `Ctrl+Shift+Espacio`, y
el programa se detendrá hasta que presione esta combinación de teclas nuevamente.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/program_paused.png?raw=true)

> [!CONSEJO]
> Si alguna de las celdas está definida incorrectamente, puede hacer clic en la celda y seleccionar cuál debería ser realmente la celda.
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





## En futuras versiones...
- Velocidad adaptable dependiendo del FPS en el juego.
- Comprobar la corrección de las cadenas dispuestas.
- Seguimiento del estado del tanque de tinta
- Traducción a otros idiomas dentro de la aplicación




# Ejecutar desde la fuente:
1. Instalar dependencias:
```shell
pip install -r requirements.txt
```

2. Agregue la carpeta src del proyecto a PYTHONPATH:
Ventanas:
```cmd
set "PYTHONPATH=$($CWD);$($PYTHONPATH)"
```
-Unix:
```cmd
export PYTHONPATH=$(cwd):$PYTHONPATH
```

3. Ejecute desde la raíz del proyecto (requiere `Python 3.10` o superior):
```shell
python -m src.main
```


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


### Gracias especiales
- [Acak1221](https://github.com/acak1221) para crear una red neuronal para determinar aspectos de una solución
- [Limuranius](https://github.com/Limuranius) por crear una red neuronal para determinar aspectos y su número en la tabla, y mucho trabajo en la creación de un sistema liviano para lanzar redes neuronales
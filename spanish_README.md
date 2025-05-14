## [descargar .exe verses] (https://github.com/sergtyapkin/thaumcraft-auto-researcher/releases)
[Última versión `v1.2.0`] (https://github.com/sergtyapkin/thaumcraft-auto-researcher/releases/tag/v1.2.0)
<details>
<summary>Changelog:</summary>

- Las configuraciones se almacenan en AppData. Al reiniciar, ya no necesita volver
- ¡Ahora la red neuronal determina los aspectos sobre la mesa!
La velocidad de investigación debido a esto aumentó en más de 10 veces.
- Mejoró la velocidad de la red neuronal debido a su almacenamiento en caché local
- Se agregaron combinaciones clave para un control más delgado
- Se agregó régimen de investigación sin parar

> `v1.2._` - Configuración de todos los aspectos con varias neuralidades y oficios de los faltantes

> `v1.1._` - Configuración de aspectos en la tabla con una red neuronal con la posibilidad de cambiar el usuario

> `v1.0._` - La configuración de aspectos en la tabla por parte del usuario

> `v0 ._._` - Versiones MVP preelacionadas
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



# Investigador automático para Thaumcraft 4
> _ ** thaumcraft ** _ - un mod para el juego _minecraft_, a menudo instalado en ensamblaje mágico de modificaciones en servidores populares

El programa que utiliza dos redes neuronales para determinar los aspectos en la pantalla ** Algorítmicamente resuelve y presenta ** notas de investigación en la tabla de investigación.
Toda la interfaz de interacción es translúcida y se muestra en la parte superior de todas las ventanas.

El programa ** no interactúa con el código de juego y no está determinado por Antithens.
Todo lo que hace es mirar ** píxeles en la pantalla **, con redes neuronales determina qué aspectos están en la pantalla, e imita ** acciones con un mouse y un teclado **, como si una persona lo hiciera.

> [! IMPORTANTE]
> Para cualquier pregunta, error y sugerencia, escriba: [t.me/tyapkin_s.0(https://t.me/tyapin_s)

<details>
<summary>Список поддерживаемых аддонов (развернуть...)</summary>

- abejas mágicas
- Magia prohibida
- Codicia
- Gruñadura
- Gregtech Newhorizons
- botas taumicas
- complementos botánicos
- El Elysium
- revelaciones taumicas
- Thaumaturgia esencial
- Integración de abysalcraft
</details>

https://github.com/user-attachments/assets/a2eaa3b7-c7fe-4fbc-9905-1b19a32d498f




# ¿Cómo usar esto?
> [! Precaución]
> Las imágenes y la descripción no son adecuadas para la última versión del programa. Utiliza un sistema similar, pero más automatizado. Puede seguir las indicaciones dentro del programa, y ​​todo será claro para usted.
> Seguramente actualizaremos las instrucciones a continuación, pero hasta ahora.

## Configuración preliminar
> _ Se llena una vez después del primer lanzamiento del programa_
0. Descargue el programa de [Lanzamientos] (https://github.com/sergtyapkin/thaumcraft-auto-researcher/releases)
1. Demostración y verificación que los puntos con encrucijada se pueden mover.
Simplemente mueva el punto rojo al amarillo.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/enroll.png?raw=true)
2. Es necesario especificar el programa donde se encuentra la interfaz de la tabla de estudio.
Para hacer esto, las esquinas del rectángulo amarillo deben moverse para que caminen por el perímetro exterior de la mesa, como se muestra en la captura de pantalla a continuación.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/find_table.png?raw=true)
3. Es necesario dejar que el programa se conozca con más detalle donde los botones de interacción están dentro de la tabla encantadora.
Para hacer esto, mueva todos los puntos como se muestra en la captura de pantalla a continuación
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_controls.png?raw=true)
4. Seleccione su ThaumCraft y todos los complementos instalados
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_version_and_addons.png?raw=true) 

Después de realizar todas estas acciones, todas las elecciones del usuario se conservan en la carpeta `c: // usuarios/%de usuario%/. ThaumCraftAutoreSearcher`,
En la próxima vez que se lance el programa, esto no es necesario, el siguiente paso se mostrará de inmediato.
Siempre puede volver a la configuración presionando la tecla `Backspace`

### Cadena de soluciones de aspectos
1. ** Ponga una nota de investigación ** desde la ranura del inventario superior izquierdo en la tabla de investigación
Después de hacer clic en `Enter`, se iniciará el proceso de determinar aspectos en el campo utilizando una red neuronal.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/prepare_to_solving_aspects.png?raw=true)
La decisión de las cadenas de aspecto se generará automáticamente, que el programa va a establecer
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_solved.png?raw=true)

> [! Tip]
> Si la cadena de aspecto es demasiado grande o los aspectos que no tiene se usan en ella, haga clic en `r` para sobrecalentarla
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_rerolled.png?raw=true)

> [! Tip]
> Si necesitas hacer algo en el juego para que el juego no superponga la interfaz del programa, puedes presionar `Ctrl+Shift+Space, y
El programa suspenderá el trabajo antes de la reducción de esta combinación de claves.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/program_paused.png?raw=true)

> [! Tip]
> Si alguna de las celdas se define incorrectamente, puede hacer clic en la celda y elegir cuál debería ser la celda.
Después de eso, la decisión se superpondrá automáticamente
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects.png?raw=true)
2. ** Asegúrese de que en el tintero suficiente tinta **. Si terminan, el algoritmo para diseñar los aspectos no se detendrá,
Y las notas de investigación no se resolverán.
Luego haga clic en `Enter` y comenzará el proceso de establecer los aspectos de la tabla en las cadenas recibidas.
3. ** Después del final de exponer los aspectos **, una nota del estudio se pondrá en el inventario,
Y en lugar de eso, lo siguiente del inventario se coloca sobre la mesa.
Entonces el proceso se repetirá nuevamente. Por lo tanto, puede resolver una gran cantidad de notas que se encuentran en el inventario uno tras otro
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/next_research_putted.png?raw=true)

> [! Tip]
> - para que las notas de investigación continúen explorándose a su vez, como están en el inventario, puede presionar `ctrl+enter`, y luego
Al estudiar cada nota siguiente, el programa no esperará la confirmación de 'Ingrese' del usuario, sino que inmediatamente comenzará a cargar una solución.

> [! Tip]
> - Durante el diseño de los aspectos, una combinación de claves `ctrl+shift+alt` en caso de que el programa se complete con urgencia.





## en las siguientes versiones ...
- Velocidad adaptativa de trabajo dependiendo de FPS en el juego
- Verificar la corrección de las cadenas forradas
- Monitoreo de la condición del tinta
- Traducción a otros idiomas dentro de la aplicación




# Lanzar desde la fuente:
1. Instalación de dependencias:
```shell
pip install -r requirements.txt
```

2. Agregue la carpeta SRC en Pythonpath:
Windows:
```cmd
set "PYTHONPATH=$($CWD);$($PYTHONPATH)"
```
-Unix:
```cmd
export PYTHONPATH=$(cwd):$PYTHONPATH
```

3. A partir de la raíz del proyecto (se requiere la versión de `Python 3.10` o superior):
```shell
python -m src.main
```


## ensamblaje de la aplicación en el archivo .exe
1. Instalación de dependencias y coleccionista:
```shell
pip install -r requirements.txt
pip install auto-py-to-exe
```

2. *** \ [Paso opcional] *** Descargar Upx (reduce el tamaño del archivo exe final)
https://github.com/upx/upx/releases/


3. Lanzamiento del comando de ensamblaje desde la raíz raíz (abrirá una interfaz desde la que puede ejecutar el ensamblaje):
```shell
auto-py-to-exe -c .\pyinstaller_configs\autoPyToExe.json
```

4. *** \ [Paso opcional] *** En la sección ** Avanzada ** `-UPX-DIR` (ubicación de la carpeta con el archivo ejecutable` Upx.exe`) e inicie el ensamblaje.
Compilado un archivo EXE aparecerá en la carpeta `salida 'en este directorio


## Gratitud separada
- [ACAK1221] (https://github.com/ACAK1221) para crear una red neuronal de determinación de aspectos en la solución
- [Limuranius] (https://github.com/limuranius) para crear una red neuronal de determinar los aspectos y su número en la tabla, y un mayor trabajo para crear un sistema liviano de lanzamiento de redes neuronales
from dataclasses import dataclass


@dataclass
class TEXTS:
    languageName = "languageName"

    enroll = "enroll"
    configureThaumWindow = "configureThaumWindow"
    confirmThaumWindowSlots = "confirmThaumWindowSlots"
    chooseThaumVersion = "chooseThaumVersion"
    beReadyForStartSolving = "beReadyForStartSolving"
    beReadyForDetectionAspects = "beReadyForDetectionAspects"
    waitForDetectionAspects = "waitForDetectionAspects"
    aspectsDetected = "aspectsDetected"
    aspectChanging = "aspectChanging"
    waitForSolvingPlacing = "waitForSolvingPlacing"
    solvingCreated = "solvingCreated"
    programPaused = "programPaused"
    startAutomaticMode = "startAutomaticMode"

    @dataclass
    class Buttons:
        cancel = "cancel"
        confirm = "confirm"
        backArrowed = "backArrowed"
        nextArrowed = "nextArrowed"
        back = "back"
        next = "next"
        cellIsEmpty = "cellIsEmpty"
        aspectData = "aspectData"
        backToSettings = "backToSettings"
        regenerateSolving = "regenerateSolving"
        placeSolving = "placeSolving"
        automaticMode = "automaticMode"
        setCellNotAvailable = "setCellNotAvailable"
        setCellFree = "setCellFree"
        notSelected = "notSelected"


TRANSLATIONS = {
    "Russian": {
        TEXTS.languageName: "Русский",

        TEXTS.enroll: """Привет. Сначала нужно будет дать знать программе, где на экране находится игра.
Для этого в этом окошке будет показан текст с подсказками.
Вот такие точки можно перемещать:
Закрыть программу всегда можно кликом по крестику в правом верхнем углу.

Чтобы двинуться дальше, переместите эту точку на жёлтую точку посередине экрана.
(Кстати, это окошко тоже можно перемещать).""",

        TEXTS.configureThaumWindow: """Отлично! Сперва обозначим окно стола исследований.
Откройте интерфейс стола исследований, а потом передвиньте две точки так, 
чтобы прямоугольник обозначал границу этого окна.""",

        TEXTS.confirmThaumWindowSlots: """Программа автоматически определила положения кнопок взаимодействия 
так, как показано. Скорее всего сделала она это не точно, так что внимательно посмотрите на точки,
и, если нужно, передвиньте их точно на нужные слоты / кнопки. 
От точности настройки зависит правильность работы программы! Вот список, где какие точки:

Желтые - слот для \"бумаги и пера\", слот для \"изучений\";
Зеленая область - выбор аспектов из стола 5х5. Важно, чтобы все
линии с точностью до пары пикселей разделяли аспекты;
Голубые - переход по страницам аспектов влево / вправо;
Розовые - удаление аспектов из смешивателя, смешение аспектов;
Шестиугольная область - место выкладывания аспектов в ячейки 
(очень важно совпадение всех центров ячеек на пересечениях линий);
Фиолетовая область - 9х3 внутренних слотов инвентаря.

(!!! После завершения этой конфигурации, если окно с игрой открыто не во весь экран, 
не передвигайте его по экрану !!!)""",

        TEXTS.chooseThaumVersion: """Выберите версию Thaumcraft.
От этого будут зависеть рецепты получения аспектов.
(Самая популярная версия - 4.2.3.5)

Выбери версию:""",

        TEXTS.beReadyForStartSolving: """Сейчас нейросеть будет определять аспекты, находящиеся на поле.
Выложите записку исследования в ячейку стола, а инвентарь заполните записками исследований,
начиная с самого верхнего левого слота. Они будут исследоваться по очереди""",

        TEXTS.beReadyForDetectionAspects: """Сейчас нейросеть определит имеющиеся аспекты в вашем столе, сконфигурированном ранее.
Не двигайте курсором мыши в процессе!""",

        TEXTS.waitForDetectionAspects: """Ждите и не двигайте курсором мыши!""",

        TEXTS.aspectsDetected: """Нейросеть определила аспекты в инвентаре и их количество.
Проверьте правильность определения. Ошибки определения можно исправить, нажав на ячейку.

Перелистывать страницы следует исключительно кнопками, нарисованными поверх игры!""",

        TEXTS.aspectChanging: """Чтобы изменить аспект в ячейке, выберите его из списка ниже
Чтобы изменить его количество, используйте клавиши цифр [0-9] и [Backspace]""",

        TEXTS.waitForSolvingPlacing: """Подождите, решение выкладывается на поле... 
Не двигайте мышью и не нажимайте никакие кнопки!

Для экстренного закрытия программы нажмите [Ctrl + Shift + Alt]""",

        TEXTS.solvingCreated: """Нейросеть определила аспекты на поле.
Если аспекты определены неверно, можно кликнуть на ячейку 
и выбрать, что в ней должно быть на самом деле. 

Чтобы приостановить программу, нажми [Ctrl + Shift + Пробел]""",

        TEXTS.programPaused: """Программа приостановлена.

Чтобы продолжить работу, нажмите [Ctrl + Shift + Пробел]""",

        TEXTS.startAutomaticMode: """Начать безостановочное исследование нескольких записок.
Записки должны быть разложены в инвентаре подряд, начиная с левого верхнего слота в инвентаре.
В столе исследований записки быть не должно""",

        TEXTS.Buttons.cancel: "Отмена",
        TEXTS.Buttons.confirm: "Подтвердить",
        TEXTS.Buttons.backArrowed: "<  Назад",
        TEXTS.Buttons.nextArrowed: "Далее  >",
        TEXTS.Buttons.back: "Назад",
        TEXTS.Buttons.next: "Далее",
        TEXTS.Buttons.cellIsEmpty: "Ячейка пуста или неизвестный аспект",
        TEXTS.Buttons.aspectData: "Данные аспекта:",
        TEXTS.Buttons.backToSettings: "Назад в настройки",
        TEXTS.Buttons.regenerateSolving: "Перегенерировать решение",
        TEXTS.Buttons.placeSolving: "Выложить решение",
        TEXTS.Buttons.automaticMode: "Безостановочный режим",
        TEXTS.Buttons.setCellNotAvailable: "Ячейка недоступна (N)",
        TEXTS.Buttons.setCellFree: "Ячейка свободна (F)",
        TEXTS.Buttons.notSelected: "не выбрано",
    },

    "English": {
        TEXTS.languageName: "English",

        TEXTS.enroll: """Hello. First, you need to let the program know where the game is on the screen.
This window will show text with hints.
These points can be moved:
You can always close the program by clicking the cross in the upper right corner.

To proceed, move this point to the yellow point in the middle of the screen.
(By the way, this window can also be moved by dragging the black point in the upper left corner).""",

        TEXTS.configureThaumWindow: """Great! First, let's mark the research table window.
Open the research table interface, then move the two points so 
that the rectangle marks the boundary of this window.""",

        TEXTS.confirmThaumWindowSlots: """The program has automatically determined the positions of interaction buttons 
as shown. Most likely it did not do it accurately, so carefully look at the points,
and if necessary, move them exactly to the required slots / buttons. 
The accuracy of the settings determines the correct operation of the program! Here is a list of which points are which:

Yellow - slot for \"paper and quill\", slot for \"studies\";
Green area - selection of aspects from the 5x5 table. It is important that all
lines separate aspects with accuracy of a couple of pixels;
Light blue - scrolling through aspect pages left / right;
Pink - removing aspects from the mixer, mixing aspects;
Hexagonal area - place for placing aspects in cells 
(it is very important that all cell centers match at line intersections);
Purple area - 9x3 minecraft inventory slots.

(!!! After completing this configuration, if the game window is not in fullscreen, 
do not move it around the screen !!!)""",

        TEXTS.chooseThaumVersion: """Choose the Thaumcraft version.
This will determine the aspect recipes.
(The most popular version is 4.2.3.5)

Select version:""",

        TEXTS.beReadyForStartSolving: """Now the neural network will detect aspects on the field.
Place a research note in the table slot, and fill the inventory with research notes,
starting from the top left slot. They will be researched one by one""",

        TEXTS.beReadyForDetectionAspects: """Now the neural network will detect the available aspects in your previously configured table.
Do not move the mouse cursor during the process!""",

        TEXTS.waitForDetectionAspects: """Wait and do not move the mouse cursor!""",

        TEXTS.aspectsDetected: """The neural network has detected aspects in the inventory and their quantities.
Check the correctness of the detection. Detection errors can be corrected by clicking on a cell.

Scrolling through pages should only be done using the buttons drawn over the game!""",

        TEXTS.aspectChanging: """To change an aspect in a cell, select it from the list below.
To change its quantity, use the number keys [0-9] and [Backspace]""",

        TEXTS.waitForSolvingPlacing: """Please wait, the solution is being placed on the field... 
Do not move the mouse or press any buttons!

For emergency program termination, press [Ctrl + Shift + Alt]""",

        TEXTS.solvingCreated: """The neural network has detected aspects on the field.
If aspects are detected incorrectly, you can click on a cell 
and choose what should actually be there.

To pause the program, press [Ctrl + Shift + Space]""",

        TEXTS.programPaused: """Program is paused.

To continue working, press [Ctrl + Shift + Space]""",

        TEXTS.startAutomaticMode: """Start non-stop research of multiple notes.
The notes must be placed in the inventory in a row, starting from the top left slot in the inventory.
There should be no research note in the research table""",

        TEXTS.Buttons.cancel: "Cancel",
        TEXTS.Buttons.confirm: "Confirm",
        TEXTS.Buttons.backArrowed: "<  Back",
        TEXTS.Buttons.nextArrowed: "Next  >",
        TEXTS.Buttons.back: "Back",
        TEXTS.Buttons.next: "Next",
        TEXTS.Buttons.cellIsEmpty: "Cell is empty or unknown aspect",
        TEXTS.Buttons.aspectData: "Aspect data:",
        TEXTS.Buttons.backToSettings: "Back to settings",
        TEXTS.Buttons.regenerateSolving: "Regenerate solution",
        TEXTS.Buttons.placeSolving: "Place solution",
        TEXTS.Buttons.automaticMode: "Automatic mode",
        TEXTS.Buttons.setCellNotAvailable: "Cell not available (N)",
        TEXTS.Buttons.setCellFree: "Cell is free (F)",
        TEXTS.Buttons.notSelected: "not selected",
    },

    "Italian": {
        TEXTS.languageName: "Italiano",

        TEXTS.enroll: """Ciao. Per prima cosa, devi far sapere al programma dove si trova il gioco sullo schermo.
Questa finestra mostrerà testo con suggerimenti.
Questi punti possono essere spostati:
Puoi sempre chiudere il programma facendo clic sulla croce nell'angolo in alto a destra.

Per procedere, sposta questo punto sul punto giallo al centro dello schermo.
(A proposito, questa finestra può anche essere spostata trascinando il punto nero nell'angolo in alto a sinistra).""",

        TEXTS.configureThaumWindow: """Ottimo! Per prima cosa, segniamo la finestra del tavolo di ricerca.
Apri l'interfaccia del tavolo di ricerca, quindi sposta i due punti in modo 
che il rettangolo segni il confine di questa finestra.""",

        TEXTS.confirmThaumWindowSlots: """Il programma ha determinato automaticamente le posizioni dei pulsanti di interazione 
come mostrato. Molto probabilmente non l'ha fatto con precisione, quindi guarda attentamente i punti,
e se necessario, spostali esattamente sugli slot / pulsanti richiesti. 
La precisione delle impostazioni determina il corretto funzionamento del programma! Ecco un elenco di quali punti sono quali:

Giallo - slot per \"carta e penna\", slot per \"studi\";
Area verde - selezione degli aspetti dalla tabella 5x5. È importante che tutte
le linee separino gli aspetti con precisione di un paio di pixel;
Azzurro - scorrimento delle pagine degli aspetti a sinistra / destra;
Rosa - rimozione degli aspetti dal miscelatore, miscelazione degli aspetti;
Area esagonale - posto per posizionare gli aspetti nelle celle 
(è molto importante che tutti i centri delle celle corrispondano alle intersezioni delle linee);
Area viola - 9x3 slot interni dell'inventario.

(!!! Dopo aver completato questa configurazione, se la finestra di gioco non è a schermo intero, 
non spostarla sullo schermo !!!)""",

        TEXTS.chooseThaumVersion: """Scegli la versione di Thaumcraft.
Questo determinerà le ricette degli aspetti.
(La versione più popolare è 4.2.3.5)

Seleziona versione:""",

        TEXTS.beReadyForStartSolving: """Ora la rete neurale rileverà gli aspetti sul campo.
Metti una nota di ricerca nello slot del tavolo e riempi l'inventario con note di ricerca,
iniziando dallo slot in alto a sinistra. Saranno ricercate una per una""",

        TEXTS.beReadyForDetectionAspects: """Ora la rete neurale rileverà gli aspetti disponibili nel tuo tavolo precedentemente configurato.
Non muovere il cursore del mouse durante il processo!""",

        TEXTS.waitForDetectionAspects: """Attendi e non muovere il cursore del mouse!""",

        TEXTS.aspectsDetected: """La rete neurale ha rilevato gli aspetti nell'inventario e le loro quantità.
Controlla la correttezza del rilevamento. Gli errori di rilevamento possono essere corretti facendo clic su una cella.

Lo scorrimento delle pagine dovrebbe essere fatto solo usando i pulsanti disegnati sopra il gioco!""",

        TEXTS.aspectChanging: """Per cambiare un aspetto in una cella, selezionalo dall'elenco qui sotto.
Per cambiare la sua quantità, usa i tasti numerici [0-9] e [Backspace]""",

        TEXTS.waitForSolvingPlacing: """Attendi, la soluzione viene posizionata sul campo... 
Non muovere il mouse o premere alcun pulsante!

Per la chiusura di emergenza del programma, premi [Ctrl + Shift + Alt]""",

        TEXTS.solvingCreated: """La rete neurale ha rilevato gli aspetti sul campo.
Se gli aspetti sono rilevati in modo errato, puoi fare clic su una cella 
e scegliere cosa dovrebbe esserci effettivamente.

Per mettere in pausa il programma, premi [Ctrl + Shift + Spazio]""",

        TEXTS.programPaused: """Programma in pausa.

Per continuare a lavorare, premi [Ctrl + Shift + Spazio]""",

        TEXTS.startAutomaticMode: """Avvia la ricerca senza sosta di più note.
Le note devono essere posizionate nell'inventario in fila, iniziando dallo slot in alto a sinistra nell'inventario.
Non dovrebbe esserci alcuna nota di ricerca nel tavolo di ricerca""",

        TEXTS.Buttons.cancel: "Annulla",
        TEXTS.Buttons.confirm: "Conferma",
        TEXTS.Buttons.backArrowed: "<  Indietro",
        TEXTS.Buttons.nextArrowed: "Avanti  >",
        TEXTS.Buttons.back: "Indietro",
        TEXTS.Buttons.next: "Avanti",
        TEXTS.Buttons.cellIsEmpty: "La cella è vuota o aspetto sconosciuto",
        TEXTS.Buttons.aspectData: "Dati aspetto:",
        TEXTS.Buttons.backToSettings: "Torna alle impostazioni",
        TEXTS.Buttons.regenerateSolving: "Rigenera soluzione",
        TEXTS.Buttons.placeSolving: "Posiziona soluzione",
        TEXTS.Buttons.automaticMode: "Modalità automatica",
        TEXTS.Buttons.setCellNotAvailable: "Cella non disponibile (N)",
        TEXTS.Buttons.setCellFree: "Cella libera (F)",
        TEXTS.Buttons.notSelected: "non selezionato",
    },

    "Dutch": {
        TEXTS.languageName: "Nederlands",

        TEXTS.enroll: """Hallo. Eerst moet je het programma laten weten waar het spel zich op het scherm bevindt.
Dit venster toont tekst met hints.
Deze punten kunnen worden verplaatst:
Je kunt het programma altijd sluiten door op het kruisje in de rechterbovenhoek te klikken.

Om verder te gaan, verplaats dit punt naar het gele punt in het midden van het scherm.
(Trouwens, dit venster kan ook worden verplaatst door het zwarte punt in de linkerbovenhoek te slepen).""",

        TEXTS.configureThaumWindow: """Geweldig! Laten we eerst het onderzoekstafelvenster markeren.
Open de onderzoekstafelinterface en verplaats de twee punten zodat 
de rechthoek de grens van dit venster markeert.""",

        TEXTS.confirmThaumWindowSlots: """Het programma heeft automatisch de posities van interactieknoppen bepaald 
zoals getoond. Hoogstwaarschijnlijk deed het dit niet nauwkeurig, dus kijk zorgvuldig naar de punten,
en verplaats ze indien nodig precies naar de vereiste slots / knoppen. 
De nauwkeurigheid van de instellingen bepaalt de correcte werking van het programma! Hier is een lijst van welke punten welke zijn:

Geel - slot voor \"papier en veer\", slot voor \"studies\";
Groen gebied - selectie van aspecten uit de 5x5 tabel. Het is belangrijk dat alle
lijnen aspecten scheiden met een nauwkeurigheid van een paar pixels;
Lichtblauw - bladeren door aspectpagina's links / rechts;
Roze - aspecten uit de mixer verwijderen, aspecten mixen;
Zeshoekig gebied - plaats voor het plaatsen van aspecten in cellen 
(het is erg belangrijk dat alle celcentra overeenkomen op lijnkruisingen);
Paars gebied - 9x3 interne inventarisslots.

(!!! Na het voltooien van deze configuratie, als het spelvenster niet op volledig scherm is, 
verplaats het dan niet over het scherm !!!)""",

        TEXTS.chooseThaumVersion: """Kies de Thaumcraft-versie.
Dit bepaalt de aspectrecepten.
(De meest populaire versie is 4.2.3.5)

Selecteer versie:""",

        TEXTS.beReadyForStartSolving: """Nu zal het neurale netwerk aspecten op het veld detecteren.
Plaats een onderzoeksnotitie in de tafelslot en vul de inventaris met onderzoeksnotities,
beginnend vanaf de linkerbovenste slot. Ze worden één voor één onderzocht""",

        TEXTS.beReadyForDetectionAspects: """Nu zal het neurale netwerk de beschikbare aspecten in uw eerder geconfigureerde tafel detecteren.
Beweeg de muiscursor niet tijdens het proces!""",

        TEXTS.waitForDetectionAspects: """Wacht en beweeg de muiscursor niet!""",

        TEXTS.aspectsDetected: """Het neurale netwerk heeft aspecten in de inventaris en hun hoeveelheden gedetecteerd.
Controleer de juistheid van de detectie. Detectiefouten kunnen worden gecorrigeerd door op een cel te klikken.

Bladeren door pagina's mag alleen worden gedaan met de knoppen die over het spel zijn getekend!""",

        TEXTS.aspectChanging: """Om een aspect in een cel te wijzigen, selecteert u het uit de onderstaande lijst.
Om de hoeveelheid te wijzigen, gebruikt u de cijfertoetsen [0-9] en [Backspace]""",

        TEXTS.waitForSolvingPlacing: """Even geduld, de oplossing wordt op het veld geplaatst... 
Beweeg de muis niet en druk op geen enkele knop!

Voor noodafsluiting van het programma, druk op [Ctrl + Shift + Alt]""",

        TEXTS.solvingCreated: """Het neurale netwerk heeft aspecten op het veld gedetecteerd.
Als aspecten onjuist zijn gedetecteerd, kunt u op een cel klikken 
en kiezen wat er werkelijk zou moeten zijn.

Om het programma te pauzeren, druk op [Ctrl + Shift + Spatie]""",

        TEXTS.programPaused: """Programma is gepauzeerd.

Om verder te werken, druk op [Ctrl + Shift + Spatie]""",

        TEXTS.startAutomaticMode: """Start non-stop onderzoek van meerdere notities.
De notities moeten op een rij in de inventaris worden geplaatst, beginnend vanaf de linkerbovenste slot in de inventaris.
Er mag geen onderzoeksnotitie in de onderzoekstafel zijn""",

        TEXTS.Buttons.cancel: "Annuleren",
        TEXTS.Buttons.confirm: "Bevestigen",
        TEXTS.Buttons.backArrowed: "<  Terug",
        TEXTS.Buttons.nextArrowed: "Volgende  >",
        TEXTS.Buttons.back: "Terug",
        TEXTS.Buttons.next: "Volgende",
        TEXTS.Buttons.cellIsEmpty: "Cel is leeg of onbekend aspect",
        TEXTS.Buttons.aspectData: "Aspectgegevens:",
        TEXTS.Buttons.backToSettings: "Terug naar instellingen",
        TEXTS.Buttons.regenerateSolving: "Oplossing opnieuw genereren",
        TEXTS.Buttons.placeSolving: "Oplossing plaatsen",
        TEXTS.Buttons.automaticMode: "Automatische modus",
        TEXTS.Buttons.setCellNotAvailable: "Cel niet beschikbaar (N)",
        TEXTS.Buttons.setCellFree: "Cel is vrij (F)",
        TEXTS.Buttons.notSelected: "niet geselecteerd",
    },

    "Spanish": {
        TEXTS.languageName: "Español",

        TEXTS.enroll: """Hola. Primero, debes informar al programa dónde está el juego en la pantalla.
Esta ventana mostrará texto con sugerencias.
Estos puntos se pueden mover:
Siempre puedes cerrar el programa haciendo clic en la cruz en la esquina superior derecha.

Para continuar, mueve este punto al punto amarillo en el centro de la pantalla.
(Por cierto, esta ventana también se puede mover arrastrando el punto negro en la esquina superior izquierda).""",

        TEXTS.configureThaumWindow: """¡Genial! Primero, marquemos la ventana de la mesa de investigación.
Abre la interfaz de la mesa de investigación, luego mueve los dos puntos para 
que el rectángulo marque el límite de esta ventana.""",

        TEXTS.confirmThaumWindowSlots: """El programa ha determinado automáticamente las posiciones de los botones de interacción 
como se muestra. Lo más probable es que no lo haya hecho con precisión, así que mira cuidadosamente los puntos,
y si es necesario, muévelos exactamente a las ranuras / botones requeridos. 
¡La precisión de la configuración determina el funcionamiento correcto del programa! Aquí hay una lista de qué puntos son cuáles:

Amarillo - ranura para \"papel y pluma\", ranura para \"estudios\";
Área verde - selección de aspectos de la tabla 5x5. Es importante que todas
las líneas separen aspectos con precisión de un par de píxeles;
Azul claro - desplazamiento por páginas de aspectos izquierda / derecha;
Rosa - eliminación de aspectos del mezclador, mezcla de aspectos;
Área hexagonal - lugar para colocar aspectos en celdas 
(es muy importante que todos los centros de las celdas coincidan en las intersecciones de líneas);
Área púrpura - 9x3 ranuras internas de inventario.

(!!! Después de completar esta configuración, si la ventana del juego no está en pantalla completa, 
no la muevas por la pantalla !!!)""",

        TEXTS.chooseThaumVersion: """Elige la versión de Thaumcraft.
Esto determinará las recetas de aspectos.
(La versión más popular es 4.2.3.5)

Seleccionar versión:""",

        TEXTS.beReadyForStartSolving: """Ahora la red neuronal detectará aspectos en el campo.
Coloca una nota de investigación en la ranura de la mesa y llena el inventario con notas de investigación,
comenzando desde la ranura superior izquierda. Se investigarán una por una""",

        TEXTS.beReadyForDetectionAspects: """Ahora la red neuronal detectará los aspectos disponibles en tu mesa previamente configurada.
¡No muevas el cursor del ratón durante el proceso!""",

        TEXTS.waitForDetectionAspects: """¡Espera y no muevas el cursor del ratón!""",

        TEXTS.aspectsDetected: """La red neuronal ha detectado aspectos en el inventario y sus cantidades.
Verifica la exactitud de la detección. Los errores de detección se pueden corregir haciendo clic en una celda.

¡El desplazamiento por las páginas solo debe hacerse usando los botones dibujados sobre el juego!""",

        TEXTS.aspectChanging: """Para cambiar un aspecto en una celda, selecciónalo de la lista a continuación.
Para cambiar su cantidad, usa las teclas numéricas [0-9] y [Retroceso]""",

        TEXTS.waitForSolvingPlacing: """Espera, la solución se está colocando en el campo... 
¡No muevas el ratón ni presiones ningún botón!

Para la terminación de emergencia del programa, presiona [Ctrl + Shift + Alt]""",

        TEXTS.solvingCreated: """La red neuronal ha detectado aspectos en el campo.
Si los aspectos se detectan incorrectamente, puedes hacer clic en una celda 
y elegir lo que realmente debería estar allí.

Para pausar el programa, presiona [Ctrl + Shift + Espacio]""",

        TEXTS.programPaused: """Programa en pausa.

Para continuar trabajando, presiona [Ctrl + Shift + Espacio]""",

        TEXTS.startAutomaticMode: """Iniciar investigación sin parar de múltiples notas.
Las notas deben colocarse en el inventario en fila, comenzando desde la ranura superior izquierda en el inventario.
No debe haber una nota de investigación en la mesa de investigación""",

        TEXTS.Buttons.cancel: "Cancelar",
        TEXTS.Buttons.confirm: "Confirmar",
        TEXTS.Buttons.backArrowed: "<  Atrás",
        TEXTS.Buttons.nextArrowed: "Siguiente  >",
        TEXTS.Buttons.back: "Atrás",
        TEXTS.Buttons.next: "Siguiente",
        TEXTS.Buttons.cellIsEmpty: "La celda está vacía o aspecto desconocido",
        TEXTS.Buttons.aspectData: "Datos del aspecto:",
        TEXTS.Buttons.backToSettings: "Volver a la configuración",
        TEXTS.Buttons.regenerateSolving: "Regenerar solución",
        TEXTS.Buttons.placeSolving: "Colocar solución",
        TEXTS.Buttons.automaticMode: "Modo automático",
        TEXTS.Buttons.setCellNotAvailable: "Celda no disponible (N)",
        TEXTS.Buttons.setCellFree: "Celda libre (F)",
        TEXTS.Buttons.notSelected: "no seleccionado",
    },

    "Arabic": {
        TEXTS.languageName: "العربية",

        TEXTS.enroll: """مرحباً. أولاً، تحتاج إلى إعلام البرنامج بمكان اللعبة على الشاشة.
ستظهر هذه النافذة نصاً مع تلميحات.
يمكن تحريك هذه النقاط:
يمكنك دائماً إغلاق البرنامج بالنقر على علامة الصليب في الزاوية اليمنى العليا.

للمتابعة، حرك هذه النقطة إلى النقطة الصفراء في منتصف الشاشة.
(بالمناسبة، يمكن أيضاً تحريك هذه النافذة عن طريق سحب النقطة السوداء في الزاوية اليسرى العليا).""",

        TEXTS.configureThaumWindow: """رائع! أولاً، دعنا نحدد نافذة طاولة البحث.
افتح واجهة طاولة البحث، ثم حرك النقطتين بحيث 
يحدد المستطيل حدود هذه النافذة.""",

        TEXTS.confirmThaumWindowSlots: """قام البرنامج تلقائياً بتحديد مواضع أزرار التفاعل 
كما هو موضح. على الأرجح لم يقم بذلك بدقة، لذا انظر بعناية إلى النقاط،
وإذا لزم الأمر، حركها بالضبط إلى الفتحات / الأزرار المطلوبة. 
دقة الإعدادات تحدد التشغيل الصحيح للبرنامج! إليك قائمة بأي النقاط هي:

أصفر - فتحة لـ \"الورقة والريشة\"، فتحة لـ \"الدراسات\"؛
منطقة خضراء - اختيار الجوانب من جدول 5x5. من المهم أن تفصل جميع
الخطوط بين الجوانب بدقة بضع بكسل؛
أزرق فاتح - التمرير عبر صفحات الجوانب يساراً / يميناً؛
وردي - إزالة الجوانب من الخلاط، خلط الجوانب؛
منطقة سداسية - مكان لوضع الجوانب في الخلايا 
(من المهم جداً أن تتطابق جميع مراكز الخلايا عند تقاطعات الخطوط)؛
منطقة أرجوانية - 9x3 فتحات داخلية للمخزون.

(!!! بعد إكمال هذا التكوين، إذا لم تكن نافذة اللعبة في وضع ملء الشاشة، 
لا تحركها حول الشاشة !!!)""",

        TEXTS.chooseThaumVersion: """اختر إصدار Thaumcraft.
سيحدد هذا وصفات الجوانب.
(الإصدار الأكثر شيوعاً هو 4.2.3.5)

حدد الإصدار:""",

        TEXTS.beReadyForStartSolving: """الآن ستكتشف الشبكة العصبية الجوانب في الحقل.
ضع مذكرة بحث في فتحة الطاولة، واملأ المخزون بمذكرات البحث،
بدءاً من الفتحة اليسرى العليا. سيتم البحث فيها واحدة تلو الأخرى""",

        TEXTS.beReadyForDetectionAspects: """الآن ستكتشف الشبكة العصبية الجوانب المتاحة في طاولتك التي تم تكوينها مسبقاً.
لا تحرك مؤشر الفأرة أثناء العملية!""",

        TEXTS.waitForDetectionAspects: """انتظر ولا تحرك مؤشر الفأرة!""",

        TEXTS.aspectsDetected: """اكتشفت الشبكة العصبية الجوانب في المخزون وكمياتها.
تحقق من صحة الاكتشاف. يمكن تصحيح أخطاء الاكتشاف بالنقر على خلية.

يجب أن يتم التمرير عبر الصفحات فقط باستخدام الأزرار المرسومة فوق اللعبة!""",

        TEXTS.aspectChanging: """لتغيير جانب في خلية، حدده من القائمة أدناه.
لتغيير كميته، استخدم مفاتيح الأرقام [0-9] و [Backspace]""",

        TEXTS.waitForSolvingPlacing: """يرجى الانتظار، يتم وضع الحل في الحقل... 
لا تحرك الفأرة أو تضغط على أي أزرار!

للإنهاء الطارئ للبرنامج، اضغط [Ctrl + Shift + Alt]""",

        TEXTS.solvingCreated: """اكتشفت الشبكة العصبية الجوانب في الحقل.
إذا تم اكتشاف الجوانب بشكل غير صحيح، يمكنك النقر على خلية 
واختيار ما يجب أن يكون هناك بالفعل.

لإيقاف البرنامج مؤقتاً، اضغط [Ctrl + Shift + مسافة]""",

        TEXTS.programPaused: """البرنامج متوقف مؤقتاً.

لمواصلة العمل، اضغط [Ctrl + Shift + مسافة]""",

        TEXTS.startAutomaticMode: """بدء البحث المتواصل لعدة مذكرات.
يجب وضع المذكرات في المخزون على التوالي، بدءاً من الفتحة اليسرى العليا في المخزون.
يجب ألا تكون هناك مذكرة بحث في طاولة البحث""",

        TEXTS.Buttons.cancel: "إلغاء",
        TEXTS.Buttons.confirm: "تأكيد",
        TEXTS.Buttons.backArrowed: "<  رجوع",
        TEXTS.Buttons.nextArrowed: "التالي  >",
        TEXTS.Buttons.back: "رجوع",
        TEXTS.Buttons.next: "التالي",
        TEXTS.Buttons.cellIsEmpty: "الخلية فارغة أو جانب غير معروف",
        TEXTS.Buttons.aspectData: "بيانات الجانب:",
        TEXTS.Buttons.backToSettings: "العودة إلى الإعدادات",
        TEXTS.Buttons.regenerateSolving: "إعادة توليد الحل",
        TEXTS.Buttons.placeSolving: "وضع الحل",
        TEXTS.Buttons.automaticMode: "الوضع التلقائي",
        TEXTS.Buttons.setCellNotAvailable: "الخلية غير متاحة (N)",
        TEXTS.Buttons.setCellFree: "الخلية فارغة (F)",
        TEXTS.Buttons.notSelected: "غير محدد",
    },

    "Chinese (Traditional)": {
        TEXTS.languageName: "繁體中文",

        TEXTS.enroll: """您好。首先，您需要讓程式知道遊戲在螢幕上的位置。
此視窗將顯示提示文字。
這些點可以移動：
您隨時可以點擊右上角的叉號來關閉程式。

要繼續，請將此點移至螢幕中央的黃點。
（順便一提，拖動左上角的黑點也可以移動此視窗）。""",

        TEXTS.configureThaumWindow: """太好了！首先，讓我們標記研究桌視窗。
打開研究桌介面，然後移動兩個點，使矩形標記此視窗的邊界。""",

        TEXTS.confirmThaumWindowSlots: """程式已自動確定了互動按鈕的位置，如圖所示。
很可能不太精確，因此請仔細查看這些點，
必要時將它們準確移動到所需的插槽/按鈕上。
設定的精確度決定了程式的正確運作！以下是各點的說明：

黃色 - 「紙和筆」插槽、「研究」插槽；
綠色區域 - 從 5x5 表格中選擇要素。重要的是所有
線條以幾個像素的精確度分隔要素；
淺藍色 - 要素頁面左右滾動；
粉紅色 - 從混合器中移除要素、混合要素；
六邊形區域 - 在單元格中放置要素的位置
（所有單元格中心在線條交叉處匹配非常重要）；
紫色區域 - 9x3 內部物品欄插槽。

（！！！完成此設定後，如果遊戲視窗不是全螢幕，
請不要將其移動到螢幕上！！！）""",

        TEXTS.chooseThaumVersion: """選擇 Thaumcraft 版本。
這將決定要素配方。
（最受歡迎的版本是 4.2.3.5）

選擇版本：""",

        TEXTS.beReadyForStartSolving: """現在神經網路將檢測場上的要素。
將研究筆記放入桌子插槽中，並用研究筆記填滿物品欄，
從左上角的插槽開始。它們將逐一被研究""",

        TEXTS.beReadyForDetectionAspects: """現在神經網路將檢測您先前設定的桌子中的可用要素。
過程中請勿移動滑鼠游標！""",

        TEXTS.waitForDetectionAspects: """請等待，不要移動滑鼠游標！""",

        TEXTS.aspectsDetected: """神經網路已檢測到物品欄中的要素及其數量。
檢查檢測的正確性。可以通過點擊單元格來修正檢測錯誤。

翻頁應僅使用繪製在遊戲上方的按鈕！""",

        TEXTS.aspectChanging: """要更改單元格中的要素，請從下方列表中選擇。
要更改其數量，請使用數字鍵 [0-9] 和 [Backspace]""",

        TEXTS.waitForSolvingPlacing: """請稍候，正在將解決方案放置到場上...
請勿移動滑鼠或按下任何按鈕！

如需緊急終止程式，請按 [Ctrl + Shift + Alt]""",

        TEXTS.solvingCreated: """神經網路已檢測到場上的要素。
如果要素檢測不正確，您可以點擊單元格
並選擇實際應有的內容。

要暫停程式，請按 [Ctrl + Shift + 空格]""",

        TEXTS.programPaused: """程式已暫停。

要繼續工作，請按 [Ctrl + Shift + 空格]""",

        TEXTS.startAutomaticMode: """開始不間斷研究多個筆記。
筆記必須在物品欄中連續放置，從物品欄的左上角插槽開始。
研究桌中不應有研究筆記""",

        TEXTS.Buttons.cancel: "取消",
        TEXTS.Buttons.confirm: "確認",
        TEXTS.Buttons.backArrowed: "<  返回",
        TEXTS.Buttons.nextArrowed: "下一步  >",
        TEXTS.Buttons.back: "返回",
        TEXTS.Buttons.next: "下一步",
        TEXTS.Buttons.cellIsEmpty: "單元格為空或未知要素",
        TEXTS.Buttons.aspectData: "要素數據：",
        TEXTS.Buttons.backToSettings: "返回設定",
        TEXTS.Buttons.regenerateSolving: "重新生成解決方案",
        TEXTS.Buttons.placeSolving: "放置解決方案",
        TEXTS.Buttons.automaticMode: "自動模式",
        TEXTS.Buttons.setCellNotAvailable: "單元格不可用 (N)",
        TEXTS.Buttons.setCellFree: "單元格空閒 (F)",
        TEXTS.Buttons.notSelected: "未選擇",
    },

    "Chinese (Simplified)": {
        TEXTS.languageName: "简体中文",

        TEXTS.enroll: """您好。首先，您需要让程序知道游戏在屏幕上的位置。
此窗口将显示提示文本。
这些点可以移动：
您可以随时点击右上角的叉号来关闭程序。

要继续，请将此点移至屏幕中央的黄点。
（顺便一提，拖动左上角的黑点也可以移动此窗口）。""",

        TEXTS.configureThaumWindow: """太好了！首先，让我们标记研究桌窗口。
打开研究桌界面，然后移动两个点，使矩形标记此窗口的边界。""",

        TEXTS.confirmThaumWindowSlots: """程序已自动确定了交互按钮的位置，如图所示。
很可能不太精确，因此请仔细查看这些点，
必要时将它们准确移动到所需的插槽/按钮上。
设置的精确度决定了程序的正确运行！以下是各点的说明：

黄色 - "纸和笔"插槽、"研究"插槽；
绿色区域 - 从 5x5 表格中选择要素。重要的是所有
线条以几个像素的精度分隔要素；
浅蓝色 - 要素页面左右滚动；
粉色 - 从混合器中移除要素、混合要素；
六边形区域 - 在单元格中放置要素的位置
（所有单元格中心在线条交叉处匹配非常重要）；
紫色区域 - 9x3 内部物品栏插槽。

（！！！完成此设置后，如果游戏窗口不是全屏，
请不要将其移动到屏幕上！！！）""",

        TEXTS.chooseThaumVersion: """选择 Thaumcraft 版本。
这将决定要素配方。
（最受欢迎的版本是 4.2.3.5）

选择版本：""",

        TEXTS.beReadyForStartSolving: """现在神经网络将检测场上的要素。
将研究笔记放入桌子插槽中，并用研究笔记填满物品栏，
从左上角的插槽开始。它们将被逐一研究""",

        TEXTS.beReadyForDetectionAspects: """现在神经网络将检测您先前设置的桌子中的可用要素。
过程中请勿移动鼠标光标！""",

        TEXTS.waitForDetectionAspects: """请等待，不要移动鼠标光标！""",

        TEXTS.aspectsDetected: """神经网络已检测到物品栏中的要素及其数量。
检查检测的正确性。可以通过点击单元格来修正检测错误。

翻页应仅使用绘制在游戏上方的按钮！""",

        TEXTS.aspectChanging: """要更改单元格中的要素，请从下方列表中选择。
要更改其数量，请使用数字键 [0-9] 和 [Backspace]""",

        TEXTS.waitForSolvingPlacing: """请稍候，正在将解决方案放置到场上...
请勿移动鼠标或按下任何按钮！

如需紧急终止程序，请按 [Ctrl + Shift + Alt]""",

        TEXTS.solvingCreated: """神经网络已检测到场上的要素。
如果要素检测不正确，您可以点击单元格
并选择实际应有的内容。

要暂停程序，请按 [Ctrl + Shift + 空格]""",

        TEXTS.programPaused: """程序已暂停。

要继续工作，请按 [Ctrl + Shift + 空格]""",

        TEXTS.startAutomaticMode: """开始不间断研究多个笔记。
笔记必须在物品栏中连续放置，从物品栏的左上角插槽开始。
研究桌中不应有研究笔记""",

        TEXTS.Buttons.cancel: "取消",
        TEXTS.Buttons.confirm: "确认",
        TEXTS.Buttons.backArrowed: "<  返回",
        TEXTS.Buttons.nextArrowed: "下一步  >",
        TEXTS.Buttons.back: "返回",
        TEXTS.Buttons.next: "下一步",
        TEXTS.Buttons.cellIsEmpty: "单元格为空或未知要素",
        TEXTS.Buttons.aspectData: "要素数据：",
        TEXTS.Buttons.backToSettings: "返回设置",
        TEXTS.Buttons.regenerateSolving: "重新生成解决方案",
        TEXTS.Buttons.placeSolving: "放置解决方案",
        TEXTS.Buttons.automaticMode: "自动模式",
        TEXTS.Buttons.setCellNotAvailable: "单元格不可用 (N)",
        TEXTS.Buttons.setCellFree: "单元格空闲 (F)",
        TEXTS.Buttons.notSelected: "未选择",
    },

    "French": {
        TEXTS.languageName: "Français",

        TEXTS.enroll: """Bonjour. Tout d'abord, vous devez indiquer au programme où se trouve le jeu sur l'écran.
Cette fenêtre affichera du texte avec des conseils.
Ces points peuvent être déplacés :
Vous pouvez toujours fermer le programme en cliquant sur la croix dans le coin supérieur droit.

Pour continuer, déplacez ce point sur le point jaune au milieu de l'écran.
(D'ailleurs, cette fenêtre peut également être déplacée en faisant glisser le point noir dans le coin supérieur gauche).""",

        TEXTS.configureThaumWindow: """Excellent ! D'abord, marquons la fenêtre de la table de recherche.
Ouvrez l'interface de la table de recherche, puis déplacez les deux points pour 
que le rectangle marque la limite de cette fenêtre.""",

        TEXTS.confirmThaumWindowSlots: """Le programme a automatiquement déterminé les positions des boutons d'interaction 
comme indiqué. Il ne l'a probablement pas fait avec précision, alors regardez attentivement les points,
et si nécessaire, déplacez-les exactement sur les emplacements / boutons requis. 
La précision des réglages détermine le bon fonctionnement du programme ! Voici une liste des points :

Jaune - emplacement pour \"papier et plume\", emplacement pour \"études\" ;
Zone verte - sélection des aspects dans le tableau 5x5. Il est important que toutes
les lignes séparent les aspects avec une précision de quelques pixels ;
Bleu clair - défilement des pages d'aspects gauche / droite ;
Rose - suppression des aspects du mélangeur, mélange des aspects ;
Zone hexagonale - endroit pour placer les aspects dans les cellules 
(il est très important que tous les centres des cellules correspondent aux intersections des lignes) ;
Zone violette - 9x3 emplacements d'inventaire internes.

(!!! Après avoir terminé cette configuration, si la fenêtre de jeu n'est pas en plein écran, 
ne la déplacez pas sur l'écran !!!)""",

        TEXTS.chooseThaumVersion: """Choisissez la version de Thaumcraft.
Cela déterminera les recettes des aspects.
(La version la plus populaire est 4.2.3.5)

Sélectionnez la version :""",

        TEXTS.beReadyForStartSolving: """Maintenant, le réseau neuronal détectera les aspects sur le terrain.
Placez une note de recherche dans l'emplacement de la table et remplissez l'inventaire de notes de recherche,
en commençant par l'emplacement en haut à gauche. Elles seront recherchées une par une""",

        TEXTS.beReadyForDetectionAspects: """Maintenant, le réseau neuronal détectera les aspects disponibles dans votre table précédemment configurée.
Ne déplacez pas le curseur de la souris pendant le processus !""",

        TEXTS.waitForDetectionAspects: """Attendez et ne déplacez pas le curseur de la souris !""",

        TEXTS.aspectsDetected: """Le réseau neuronal a détecté les aspects dans l'inventaire et leurs quantités.
Vérifiez l'exactitude de la détection. Les erreurs de détection peuvent être corrigées en cliquant sur une cellule.

Le défilement des pages ne doit se faire qu'avec les boutons dessinés sur le jeu !""",

        TEXTS.aspectChanging: """Pour changer un aspect dans une cellule, sélectionnez-le dans la liste ci-dessous.
Pour changer sa quantité, utilisez les touches numériques [0-9] et [Retour arrière]""",

        TEXTS.waitForSolvingPlacing: """Veuillez patienter, la solution est placée sur le terrain... 
Ne déplacez pas la souris et n'appuyez sur aucun bouton !

Pour l'arrêt d'urgence du programme, appuyez sur [Ctrl + Shift + Alt]""",

        TEXTS.solvingCreated: """Le réseau neuronal a détecté les aspects sur le terrain.
Si les aspects sont mal détectés, vous pouvez cliquer sur une cellule 
et choisir ce qui devrait réellement s'y trouver.

Pour mettre le programme en pause, appuyez sur [Ctrl + Shift + Espace]""",

        TEXTS.programPaused: """Programme en pause.

Pour continuer à travailler, appuyez sur [Ctrl + Shift + Espace]""",

        TEXTS.startAutomaticMode: """Démarrer la recherche sans arrêt de plusieurs notes.
Les notes doivent être placées dans l'inventaire à la suite, en commençant par l'emplacement en haut à gauche dans l'inventaire.
Il ne doit pas y avoir de note de recherche dans la table de recherche""",

        TEXTS.Buttons.cancel: "Annuler",
        TEXTS.Buttons.confirm: "Confirmer",
        TEXTS.Buttons.backArrowed: "<  Retour",
        TEXTS.Buttons.nextArrowed: "Suivant  >",
        TEXTS.Buttons.back: "Retour",
        TEXTS.Buttons.next: "Suivant",
        TEXTS.Buttons.cellIsEmpty: "La cellule est vide ou aspect inconnu",
        TEXTS.Buttons.aspectData: "Données de l'aspect :",
        TEXTS.Buttons.backToSettings: "Retour aux paramètres",
        TEXTS.Buttons.regenerateSolving: "Régénérer la solution",
        TEXTS.Buttons.placeSolving: "Placer la solution",
        TEXTS.Buttons.automaticMode: "Mode automatique",
        TEXTS.Buttons.setCellNotAvailable: "Cellule non disponible (N)",
        TEXTS.Buttons.setCellFree: "Cellule libre (F)",
        TEXTS.Buttons.notSelected: "non sélectionné",
    },

    "Hindi": {
        TEXTS.languageName: "हिन्दी",

        TEXTS.enroll: """नमस्ते। सबसे पहले, आपको प्रोग्राम को बताना होगा कि स्क्रीन पर गेम कहाँ है।
यह विंडो संकेतों के साथ पाठ दिखाएगी।
इन बिंदुओं को स्थानांतरित किया जा सकता है:
आप हमेशा ऊपरी दाएं कोने में क्रॉस पर क्लिक करके प्रोग्राम को बंद कर सकते हैं।

आगे बढ़ने के लिए, इस बिंदु को स्क्रीन के बीच में पीले बिंदु पर ले जाएँ।
(वैसे, ऊपरी बाएं कोने में काले बिंदु को खींचकर इस विंडो को भी स्थानांतरित किया जा सकता है)।""",

        TEXTS.configureThaumWindow: """बहुत अच्छे! पहले, शोध तालिका विंडो को चिह्नित करें।
शोध तालिका इंटरफ़ेस खोलें, फिर दो बिंदुओं को इस तरह ले जाएँ 
कि आयत इस विंडो की सीमा को चिह्नित करे।""",

        TEXTS.confirmThaumWindowSlots: """प्रोग्राम ने स्वचालित रूप से इंटरैक्शन बटनों की स्थिति निर्धारित कर ली है 
जैसा दिखाया गया है। संभवतः यह सटीक नहीं है, इसलिए बिंदुओं को ध्यान से देखें,
और यदि आवश्यक हो, तो उन्हें आवश्यक स्लॉट / बटनों पर सटीक रूप से ले जाएँ। 
सेटिंग्स की सटीकता प्रोग्राम के सही संचालन को निर्धारित करती है! यहाँ सूची है कि कौन से बिंदु क्या हैं:

पीला - \"कागज और कलम\" के लिए स्लॉट, \"अध्ययन\" के लिए स्लॉट;
हरा क्षेत्र - 5x5 तालिका से पहलुओं का चयन। यह महत्वपूर्ण है कि सभी
रेखाएँ कुछ पिक्सल की सटीकता के साथ पहलुओं को अलग करें;
हल्का नीला - पहलू पृष्ठों को बाएँ / दाएँ स्क्रॉल करना;
गुलाबी - मिक्सर से पहलुओं को हटाना, पहलुओं का मिश्रण;
षट्कोणीय क्षेत्र - कोशिकाओं में पहलुओं को रखने का स्थान 
(यह बहुत महत्वपूर्ण है कि सभी कोशिका केंद्र रेखा चौराहों पर मेल खाएँ);
बैंगनी क्षेत्र - 9x3 आंतरिक इन्वेंट्री स्लॉट।

(!!! इस कॉन्फ़िगरेशन को पूरा करने के बाद, यदि गेम विंडो फ़ुलस्क्रीन में नहीं है, 
तो इसे स्क्रीन पर न ले जाएँ !!!)""",

        TEXTS.chooseThaumVersion: """Thaumcraft संस्करण चुनें।
यह पहलू व्यंजनों को निर्धारित करेगा।
(सबसे लोकप्रिय संस्करण 4.2.3.5 है)

संस्करण चुनें:""",

        TEXTS.beReadyForStartSolving: """अब न्यूरल नेटवर्क क्षेत्र में पहलुओं का पता लगाएगा।
तालिका स्लॉट में एक शोध नोट रखें, और इन्वेंट्री को शोध नोटों से भरें,
सबसे ऊपरी बाएँ स्लॉट से शुरू करते हुए। उन पर एक-एक करके शोध किया जाएगा""",

        TEXTS.beReadyForDetectionAspects: """अब न्यूरल नेटवर्क आपकी पहले से कॉन्फ़िगर की गई तालिका में उपलब्ध पहलुओं का पता लगाएगा।
प्रक्रिया के दौरान माउस कर्सर न ले जाएँ!""",

        TEXTS.waitForDetectionAspects: """प्रतीक्षा करें और माउस कर्सर न ले जाएँ!""",

        TEXTS.aspectsDetected: """न्यूरल नेटवर्क ने इन्वेंट्री में पहलुओं और उनकी मात्रा का पता लगा लिया है।
पता लगाने की शुद्धता की जाँच करें। पता लगाने की त्रुटियों को सेल पर क्लिक करके ठीक किया जा सकता है।

पृष्ठों को स्क्रॉल करना केवल गेम के ऊपर बने बटनों का उपयोग करके किया जाना चाहिए!""",

        TEXTS.aspectChanging: """सेल में पहलू बदलने के लिए, नीचे दी गई सूची से इसे चुनें।
इसकी मात्रा बदलने के लिए, संख्या कुंजियों [0-9] और [Backspace] का उपयोग करें""",

        TEXTS.waitForSolvingPlacing: """कृपया प्रतीक्षा करें, समाधान क्षेत्र में रखा जा रहा है... 
माउस न ले जाएँ या कोई बटन न दबाएँ!

आपातकालीन प्रोग्राम समाप्ति के लिए, [Ctrl + Shift + Alt] दबाएँ""",

        TEXTS.solvingCreated: """न्यूरल नेटवर्क ने क्षेत्र में पहलुओं का पता लगा लिया है।
यदि पहलुओं का गलत पता लगाया गया है, तो आप सेल पर क्लिक कर सकते हैं 
और चुन सकते हैं कि वास्तव में वहाँ क्या होना चाहिए।

प्रोग्राम को रोकने के लिए, [Ctrl + Shift + Space] दबाएँ""",

        TEXTS.programPaused: """प्रोग्राम रोका गया है।

काम जारी रखने के लिए, [Ctrl + Shift + Space] दबाएँ""",

        TEXTS.startAutomaticMode: """कई नोटों का बिना रुके शोध शुरू करें।
नोटों को इन्वेंट्री में एक पंक्ति में रखा जाना चाहिए, इन्वेंट्री में सबसे ऊपरी बाएँ स्लॉट से शुरू करते हुए।
शोध तालिका में कोई शोध नोट नहीं होना चाहिए""",

        TEXTS.Buttons.cancel: "रद्द करें",
        TEXTS.Buttons.confirm: "पुष्टि करें",
        TEXTS.Buttons.backArrowed: "<  वापस",
        TEXTS.Buttons.nextArrowed: "आगे  >",
        TEXTS.Buttons.back: "वापस",
        TEXTS.Buttons.next: "आगे",
        TEXTS.Buttons.cellIsEmpty: "सेल खाली है या अज्ञात पहलू",
        TEXTS.Buttons.aspectData: "पहलू डेटा:",
        TEXTS.Buttons.backToSettings: "सेटिंग्स पर वापस जाएँ",
        TEXTS.Buttons.regenerateSolving: "समाधान पुनर्जीवित करें",
        TEXTS.Buttons.placeSolving: "समाधान रखें",
        TEXTS.Buttons.automaticMode: "स्वचालित मोड",
        TEXTS.Buttons.setCellNotAvailable: "सेल उपलब्ध नहीं (N)",
        TEXTS.Buttons.setCellFree: "सेल खाली है (F)",
        TEXTS.Buttons.notSelected: "चयनित नहीं",
    },

    "Korean": {
        TEXTS.languageName: "한국어",

        TEXTS.enroll: """안녕하세요. 먼저, 프로그램에게 화면에서 게임이 어디에 있는지 알려줘야 합니다.
이 창은 힌트와 함께 텍스트를 표시합니다.
이 점들은 이동할 수 있습니다:
오른쪽 상단 모서리의 십자를 클릭하여 언제든지 프로그램을 닫을 수 있습니다.

계속하려면 이 점을 화면 중앙의 노란색 점으로 이동하세요.
(참고로, 왼쪽 상단 모서리의 검은 점을 드래그하여 이 창도 이동할 수 있습니다).""",

        TEXTS.configureThaumWindow: """좋습니다! 먼저 연구대 창을 표시해 봅시다.
연구대 인터페이스를 열고 두 점을 이동하여 
직사각형이 이 창의 경계를 표시하도록 하세요.""",

        TEXTS.confirmThaumWindowSlots: """프로그램이 표시된 대로 상호작용 버튼의 위치를 자동으로 결정했습니다.
정확하지 않을 가능성이 높으니 점들을 주의 깊게 살펴보고,
필요한 경우 필요한 슬롯/버튼으로 정확히 이동하세요. 
설정의 정확성이 프로그램의 올바른 작동을 결정합니다! 다음은 어떤 점이 무엇인지 목록입니다:

노란색 - "종이와 펜" 슬롯, "연구" 슬롯;
녹색 영역 - 5x5 테이블에서 요소 선택. 모든 선이
몇 픽셀의 정확도로 요소를 분리하는 것이 중요합니다;
하늘색 - 요소 페이지 좌/우 스크롤;
분홍색 - 혼합기에서 요소 제거, 요소 혼합;
육각형 영역 - 셀에 요소를 배치하는 장소 
(모든 셀 중심이 선 교차점에서 일치하는 것이 매우 중요합니다);
보라색 영역 - 9x3 내부 인벤토리 슬롯.

(!!! 이 구성을 완료한 후, 게임 창이 전체 화면이 아니면 
화면에서 이동하지 마세요 !!!)""",

        TEXTS.chooseThaumVersion: """Thaumcraft 버전을 선택하세요.
이것이 요소 레시피를 결정합니다.
(가장 인기 있는 버전은 4.2.3.5입니다)

버전 선택:""",

        TEXTS.beReadyForStartSolving: """이제 신경망이 필드의 요소를 감지합니다.
연구 노트를 테이블 슬롯에 넣고, 인벤토리를 연구 노트로 채우세요,
왼쪽 상단 슬롯부터 시작하여. 하나씩 연구됩니다""",

        TEXTS.beReadyForDetectionAspects: """이제 신경망이 이전에 구성된 테이블에서 사용 가능한 요소를 감지합니다.
과정 중에 마우스 커서를 움직이지 마세요!""",

        TEXTS.waitForDetectionAspects: """기다리시고 마우스 커서를 움직이지 마세요!""",

        TEXTS.aspectsDetected: """신경망이 인벤토리의 요소와 수량을 감지했습니다.
감지의 정확성을 확인하세요. 감지 오류는 셀을 클릭하여 수정할 수 있습니다.

페이지 스크롤은 게임 위에 그려진 버튼만을 사용해야 합니다!""",

        TEXTS.aspectChanging: """셀의 요소를 변경하려면 아래 목록에서 선택하세요.
수량을 변경하려면 숫자 키 [0-9]와 [Backspace]를 사용하세요""",

        TEXTS.waitForSolvingPlacing: """잠시 기다려 주세요, 해결책이 필드에 배치되고 있습니다... 
마우스를 움직이거나 버튼을 누르지 마세요!

비상 프로그램 종료는 [Ctrl + Shift + Alt]를 누르세요""",

        TEXTS.solvingCreated: """신경망이 필드의 요소를 감지했습니다.
요소가 잘못 감지된 경우, 셀을 클릭하여 
실제로 있어야 할 것을 선택할 수 있습니다.

프로그램을 일시 중지하려면 [Ctrl + Shift + Space]를 누르세요""",

        TEXTS.programPaused: """프로그램이 일시 중지되었습니다.

계속 작업하려면 [Ctrl + Shift + Space]를 누르세요""",

        TEXTS.startAutomaticMode: """여러 노트의 논스톱 연구를 시작합니다.
노트는 인벤토리의 왼쪽 상단 슬롯부터 시작하여 인벤토리에 연속으로 배치해야 합니다.
연구대에 연구 노트가 없어야 합니다""",

        TEXTS.Buttons.cancel: "취소",
        TEXTS.Buttons.confirm: "확인",
        TEXTS.Buttons.backArrowed: "<  뒤로",
        TEXTS.Buttons.nextArrowed: "다음  >",
        TEXTS.Buttons.back: "뒤로",
        TEXTS.Buttons.next: "다음",
        TEXTS.Buttons.cellIsEmpty: "셀이 비어 있거나 알 수 없는 요소",
        TEXTS.Buttons.aspectData: "요소 데이터:",
        TEXTS.Buttons.backToSettings: "설정으로 돌아가기",
        TEXTS.Buttons.regenerateSolving: "해결책 재생성",
        TEXTS.Buttons.placeSolving: "해결책 배치",
        TEXTS.Buttons.automaticMode: "자동 모드",
        TEXTS.Buttons.setCellNotAvailable: "셀 사용 불가 (N)",
        TEXTS.Buttons.setCellFree: "셀이 비어 있음 (F)",
        TEXTS.Buttons.notSelected: "선택되지 않음",
    },
}

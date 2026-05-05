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



# Esploratore automatico per Thaumcraft 4

[![Download latest .exe](https://dabuttonfactory.com/button.png?t=Download+latest++.exe&f=Open+Sans-Bold&ts=20&tc=fff&w=300&h=60&c=round&bgt=gradient&bgc=6B6BFF&ebgc=BB8EFF)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases/tag/v1.2.1)
<br> [![see all releases](https://dabuttonfactory.com/button.png?t=see+all+releases&f=Open+Sans-Bold-Italic&ts=12&tc=fff&w=300&h=16&c=round&bgt=gradient&bgc=2B8F3B&ebgc=5BBB3F)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
<details>
<summary>Changelog:</summary>

- Aggiunto il supporto per varie lingue all'interno del programma
- Le configurazioni vengono salvate in AppData. Al riavvio non è più necessario riconfigurare l'applicazione
- Ora la rete neurale determina gli aspetti sul tavolo!
Grazie a ciò, la velocità della ricerca è aumentata più di 10 volte.
- Miglioramento della velocità della rete neurale grazie al caching locale
- Aggiunte scorciatoie da tastiera per un controllo più preciso
- Aggiunta la modalità di ricerca non-stop

> `v1.2._` - configurazione di tutti gli aspetti utilizzando diverse reti neurali e creando quelle mancanti

> `v1.1._` - configurazione degli aspetti sul tavolo tramite una rete neurale con possibilità di modifica da parte dell'utente

> `v1.0._` - configurazione degli aspetti sul tavolo da parte dell'utente

> `v0._._` - versioni MVP pre-rilascio
</details>

> _**Thaumcraft**_ è un mod per il gioco _Minecraft_, spesso installato in gruppi di mod magici su server popolari

Il programma, utilizzando due reti neurali per determinare gli aspetti sullo schermo, **risolve e organizza algoritmicamente** le note di ricerca nella tabella di ricerca.
L'intera interfaccia di interazione è traslucida e appare nella parte superiore della finestra di gioco.

Il programma non interagisce **in alcun modo** con il codice del gioco e non viene rilevato dagli anti-cheat.
Tutto ciò che fa è guardare i **pixel sullo schermo**, utilizzare le reti neurali per determinare quali aspetti sono presenti sullo schermo e **imitare le azioni del mouse e della tastiera** come se lo stesse facendo un essere umano.

> [!IMPORTANTE]
> Per qualsiasi domanda, errore e suggerimento, scrivi: [t.me/Tyapkin_S](https://t.me/tyapkin_s)

<details>
<summary>Список поддерживаемых аддонов (развернуть...)</summary>

- Api magiche
- Magia proibita
- Avidità
-GregTech
- GregTech Nuovi Orizzonti
- Stivali taumici
- Componenti aggiuntivi botanici
- L'Eliseo
- Rivelazioni Thaumiche
- Taumaturgia Essenziale
- Integrazione AbyssalCraft
</details>

https://github.com/user-attachments/assets/a2eaa3b7-c7fe-4fbc-9905-1b19a32d498f




# Come usarlo?
> [!ATTENZIONE]
> Immagini e descrizioni non corrispondono all'ultima versione del programma. Utilizza un sistema simile, ma più automatizzato. Puoi semplicemente seguire le istruzioni all'interno del programma e tutto ti sarà chiaro.
> Aggiorneremo sicuramente le istruzioni riportate di seguito, ma per ora è tutto.

### Preimpostato
> _Eseguito una volta dopo il primo avvio del programma_
0. Scarica il programma da [releases](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
1. Dimostrazione e verifica della possibilità di spostamento del mirino.
Basta spostare il punto rosso su quello giallo.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/enroll.png?raw=true)
2. È necessario indicare al programma dove si trova l'interfaccia della tabella di ricerca.
Per fare ciò è necessario spostare gli angoli del rettangolo giallo in modo che corrano lungo il perimetro esterno del tavolo, come mostrato nello screenshot qui sotto
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/find_table.png?raw=true)
3. È necessario far sapere al programma in modo più dettagliato dove si trovano i pulsanti di interazione all'interno della tabella degli incantesimi.
Per fare ciò, sposta tutti i punti come mostrato nello screenshot qui sotto
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_controls.png?raw=true)
4. Seleziona la tua versione Thaumcraft e tutti i componenti aggiuntivi installati
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_version_and_addons.png?raw=true) 

Dopo aver completato tutti questi passaggi, tutte le selezioni dell'utente vengono salvate nella cartella `C://users/%USER%/.ThaumcraftAutoResearcher`,
la prossima volta che avvierete il programma non sarà necessario farlo; il passaggio successivo verrà mostrato immediatamente.
Puoi sempre tornare alla configurazione premendo il tasto "Backspace".

### Risoluzione delle catene di aspetti
1. **Inserisci una nota di ricerca** dallo slot dell'inventario in alto a sinistra nello slot del tavolo di ricerca
Dopo aver premuto "Invio", inizierà il processo di determinazione degli aspetti sul campo utilizzando una rete neurale.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/prepare_to_solving_aspects.png?raw=true)
Una soluzione verrà generata automaticamente utilizzando catene di aspetti, che il programma pubblicherà
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_solved.png?raw=true)

> [!CONSIGLIO]
> Se la catena degli aspetti è troppo grande o utilizza aspetti che non hai, premi "R" per rigenerarla
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_rerolled.png?raw=true)

> [!CONSIGLIO]
> Se devi fare qualcosa nel gioco in modo che il gioco non si sovrapponga all'interfaccia del programma, puoi premere `Ctrl+Shift+Spazio` e
il programma verrà messo in pausa finché non si premerà nuovamente questa combinazione di tasti.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/program_paused.png?raw=true)

> [!CONSIGLIO]
> Se una qualsiasi delle celle è definita in modo errato, puoi fare clic sulla cella e selezionare quale dovrebbe essere effettivamente la cella.
Successivamente, la soluzione verrà rigenerata automaticamente
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects.png?raw=true)
2. **Assicurarsi che ci sia abbastanza inchiostro nel serbatoio**. Se si esauriscono, l'algoritmo per la disposizione degli aspetti non si fermerà,
e le note di ricerca non verranno risolte.
Quindi premere "Invio" e inizierà il processo di disposizione degli aspetti sulla tabella in base alle catene risultanti.
3. **Dopo aver terminato di esporre gli aspetti**, la nota di ricerca verrà inserita nell'inventario,
e al suo posto si mette sul tavolo quello successivo dell'inventario.
Quindi il processo si ripeterà di nuovo. In questo modo puoi risolvere un gran numero di note che si trovano nell'inventario una dopo l'altra
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/next_research_putted.png?raw=true)

> [!CONSIGLIO]
> - Affinché le note di ricerca continuino ad essere esaminate una per una, così come sono nell'inventario, puoi premere `Ctrl+Invio`, quindi
Durante lo studio di ogni nota successiva, il programma non attenderà la conferma da parte dell'utente con il tasto "Invio", ma inizierà immediatamente a pubblicare la soluzione.

> [!CONSIGLIO]
> - Durante la disposizione degli aspetti viene fornita la combinazione di tasti `Ctrl+Shift+Alt` nel caso in cui sia necessario terminare urgentemente il programma.





## Nelle versioni future...
- Velocità adattiva a seconda degli FPS nel gioco
- Verifica della correttezza delle catene stese
- Monitoraggio dello stato del serbatoio dell'inchiostro
- Traduzione in altre lingue all'interno dell'applicazione




# Esegui dal sorgente:
1. Installa le dipendenze:
```shell
pip install -r requirements.txt
```

2. Aggiungi la cartella src del progetto a PYTHONPATH:
Finestre:
```cmd
set "PYTHONPATH=$($CWD);$($PYTHONPATH)"
```
-Unix:
```cmd
export PYTHONPATH=$(cwd):$PYTHONPATH
```

3. Esegui dalla root del progetto (richiede `Python 3.10` o versione successiva):
```shell
python -m src.main
```


## Crea l'applicazione in un file .exe
1. Installa le dipendenze e il builder:
```shell
pip install -r requirements.txt
pip install auto-py-to-exe
```

2. ***\[Passaggio facoltativo]*** Scarica UPX (riduce la dimensione del file exe finale)
https://github.com/upx/upx/releases/


3. Esegui il comando build dalla root del progetto (si aprirà un'interfaccia da cui potrai eseguire la build):
```shell
auto-py-to-exe -c .\pyinstaller_configs\autoPyToExe.json
```

4. ***\[Passaggio facoltativo]*** Nella sezione **Avanzate**, specificare `--upx-dir` (il percorso della cartella con il file eseguibile `upx.exe`) ed eseguire la build.
Il file exe compilato apparirà nella cartella "output" in questa directory


### Un ringraziamento speciale
- [Acak1221](https://github.com/acak1221) per creare una rete neurale per determinare gli aspetti in una soluzione
- [Limuranius](https://github.com/Limuranius) per aver creato una rete neurale per determinare gli aspetti e il loro numero nella tabella, e molto lavoro sulla creazione di un sistema leggero per il lancio di reti neurali
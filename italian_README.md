## [Download .exe Release] (https://github.com/sergtyapkin/thaumcraft-auto-researcher/releases)
[Ultima versione `v1.2.0`] (https://github.com/sergtyapkin/thaumcraft-auto-researcher/releases/tag/v1.2.0)
<details>
<summary>Changelog:</summary>

- Le configurazioni sono archiviate in AppData. Quando si riavvia, non è più necessario ri -configurazione dell'applicazione
- Ora la rete neurale determina gli aspetti sul tavolo!
La velocità della ricerca dovuta a questo è aumentata di oltre 10 volte.
- Miglioramento della velocità della rete neurale a causa della sua memorizzazione nella cache locale
- Aggiunte combinazioni chiave per il controllo più sottile
- Aggiunto regime di ricerca non -stop

> `v1.2._` - Configurazione di tutti gli aspetti con diverse neuralità e mestieri delle mancanti

> `v1.1._` - Configurazione degli aspetti sulla tabella con una rete neurale con la possibilità di modificare l'utente

> `v1.0._` - La configurazione degli aspetti sulla tabella dell'utente

> `v0 ._._` - versioni MVP pre -affidabili
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



# Ricercatore automatico per Thaumcraft 4
> _ ** thaumcraft ** _ - una mod per il gioco _minecraft_, spesso installato in un gruppo magico di mod su server popolari

Il programma che utilizza due reti neurali per determinare gli aspetti sullo schermo ** algoritmicamente risolve e espone ** Note di ricerca nella tabella di ricerca.
L'intera interfaccia di interazione è traslucida ed è mostrata sopra tutte le finestre.

Il programma ** non interagisce con il codice di gioco e non è determinato da Antithens.
Tutto ciò che fa è guardare ** pixel sullo schermo **, con le reti neurali determina quali aspetti sono sullo schermo e imita ** azioni con un mouse e una tastiera **, come se una persona lo facesse.

> [! Importante]
> Per qualsiasi domanda, errori e suggerimenti, scrivi: [T.me/tyapkin_s.0(https://t.me/tyapin_s)

<details>
<summary>Список поддерживаемых аддонов (развернуть...)</summary>

- Api magiche
- Magia proibita
- Avidità
- Grumping
- Gregtech Newhorizons
- Stivali thaumici
- componenti aggiuntivi botanici
- L'Elysium
- Rivelazioni taumiche
- Thaumaturgia essenziale
- Integrazione di Abyssalcraft
</details>

https://github.com/user-attachments/assets/a2eaa3b7-c7fe-4fbc-9905-1b19a32d498f




# Come usarlo?
> [! Attenzione]
> Le immagini e la descrizione non sono adatte per l'ultima versione del programma. Utilizza un sistema simile, ma più automatizzato. Puoi semplicemente seguire le istruzioni all'interno del programma e tutto ti sarà chiaro.
> Aggiorneremo sicuramente le istruzioni di seguito, ma finora.

## impostazione preliminare
> _ Viene riempito una volta dopo il primo lancio del programma_
0. Scarica il programma da [Release] (https://github.com/sergtyapkin/thaumcraft-auto-researcher/releases)
1. Dimostrazione e verifica che i punti con Crossroads possono essere spostati.
Basta spostare il punto rosso sul giallo.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/enroll.png?raw=true)
2. È necessario specificare il programma in cui si trova l'interfaccia della tabella di studio.
Per fare ciò, gli angoli del rettangolo giallo devono essere spostati in modo che camminino lungo il perimetro esterno del tavolo, come mostrato nello screenshot sotto
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/find_table.png?raw=true)
3
Per fare ciò, sposta tutti i punti come mostrato nello screenshot seguente
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_controls.png?raw=true)
4. Seleziona il tuo thaumcraft e tutti i componenti aggiuntivi installati
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_version_and_addons.png?raw=true) 

Dopo aver eseguito tutte queste azioni, tutte le elezioni dell'utente sono conservate nella cartella `C: // Utenti/%Utente%/. ThaumcraftAutoResearcher`,
Alla prossima avviamento del programma, questo non è necessario, il passaggio successivo verrà mostrato immediatamente.
È sempre possibile tornare alla configurazione premendo il tasto `backspace`

### Soluzione catena di aspetti
1. ** Metti una nota di ricerca ** dalla fessura dell'inventario superiore sinistro nella tabella di ricerca
Dopo aver fatto clic su `Invio`, inizierà il processo di determinazione degli aspetti sul campo utilizzando una rete neurale.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/prepare_to_solving_aspects.png?raw=true)
La decisione delle catene di aspetto verrà generata automaticamente, che il programma sta per presentare
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_solved.png?raw=true)

> [! Suggerimento]
> Se la catena di aspetti è troppo grande o gli aspetti che non hai vengono utilizzati in esso, fai clic su `r` per surriscaldarlo
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_rerolled.png?raw=true)

> [! Suggerimento]
> Se hai bisogno di fare qualsiasi cosa nel gioco in modo che il gioco non si sovrappone all'interfaccia del programma, puoi premere `Ctrl+Shift+Space e
Il programma sospenderà il lavoro prima della repressione di questa combinazione di chiavi.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/program_paused.png?raw=true)

> [! Suggerimento]
> Se una delle celle è definita in modo errato, è possibile fare clic sulla cella e scegliere quale dovrebbe essere la cella.
Successivamente, la decisione verrà automaticamente sovrapposta
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects.png?raw=true)
2. ** Assicurati che nell'inchiostro abbastanza a getto d'inchiostro **. Se finiscono, l'algoritmo per la disposizione degli aspetti non si fermerà,
E le note della ricerca non saranno risolte.
Quindi fai clic su `Invio` e inizierà il processo di definizione degli aspetti sulla tabella sulle catene ricevute.
3. ** Dopo la fine della definizione degli aspetti **, una nota dello studio verrà inserita nell'inventario,
E invece di questo, il seguente inventario viene messo sul tavolo.
Quindi il processo verrà ripetuto di nuovo. Pertanto, puoi risolvere un gran numero di note che si trovano nell'inventario una dopo l'altra
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/next_research_putted.png?raw=true)

> [! Suggerimento]
> - in modo che le note della ricerca continuino ad essere esplorate a loro volta, in quanto sono nell'inventario, è possibile premere `ctrl+enter` e poi
Quando si studia ogni nota successiva, il programma non si aspetterà una conferma di `immettere 'dall'utente, ma inizierà immediatamente a caricare una soluzione.

> [! Suggerimento]
> - Durante il layout degli aspetti, una combinazione di chiavi `ctrl+shift+alt` nel caso in cui il programma sia urgentemente completato.





## nelle seguenti versioni ...
- Velocità di lavoro adattiva a seconda dell'FPS nel gioco
- Controllo della correttezza delle catene foderate
- Monitoraggio delle condizioni del calamaio
- traduzione in altre lingue all'interno dell'applicazione




# Avvia dalla fonte:
1. Installazione di dipendenze:
```shell
pip install -r requirements.txt
```

2. Aggiungi la cartella SRC in Pythonpath:
Windows:
```cmd
set "PYTHONPATH=$($CWD);$($PYTHONPATH)"
```
-Unix:
```cmd
export PYTHONPATH=$(cwd):$PYTHONPATH
```

3. A partire dalla radice del progetto (è richiesta la versione di `Python 3.10` o superiore):
```shell
python -m src.main
```


## Assembly dell'applicazione nel file .exe
1. Installazione di dipendenze e collezionista:
```shell
pip install -r requirements.txt
pip install auto-py-to-exe
```

2. *** \ [Passaggio opzionale] *** Scarica UPX (riduce la dimensione del file EXE finale)
https://github.com/upx/upx/releases/


3. Avvio del comando Assembly dalla radice della radice (aprirà un'interfaccia da cui è possibile eseguire l'assemblaggio):
```shell
auto-py-to-exe -c .\pyinstaller_configs\autoPyToExe.json
```

4. *** \ [Passaggio opzionale] *** Nella sezione ** avanzata ** `--upx-dir` (posizione della cartella con il file eseguibile` upx.exe`) e avviare l'assemblaggio.
Compilato un file exe apparirà nella cartella `output 'in questa directory


## gratitudine separata
- [ACAK1221] (https://github.com/acak1221) per la creazione di una rete neurale di determinare gli aspetti nella soluzione
- [Limuranius] (https://github.com/limuranius) per la creazione di una rete neurale per determinare gli aspetti e il loro numero nella tabella e un lavoro maggiore per creare un sistema leggero di lancio di reti neurali
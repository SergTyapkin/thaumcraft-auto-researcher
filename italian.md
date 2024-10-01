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


# Esploratore automatico per Thaumcraft 4
> _**Thaumcraft**_ è un mod per il gioco _Minecraft_, spesso installato in gruppi di mod magici su server popolari
## [Download .exe releases](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
[latest version `v1.1.2`](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases/tag/v1.1.2)
<details>
<summary>Changelog:</summary>

- Le configurazioni vengono salvate in AppData. Al riavvio non è più necessario riconfigurare l'applicazione
- Ora la rete neurale determina gli aspetti sul tavolo!
Grazie a ciò, la velocità della ricerca è aumentata più di 10 volte.
- Miglioramento della velocità della rete neurale grazie al caching locale
- Aggiunte scorciatoie da tastiera per un controllo più preciso
- Aggiunta la modalità di ricerca non-stop

> `v1.1._` - configurazione degli aspetti sul tavolo tramite una rete neurale con possibilità di modifica da parte dell'utente
>
> `v1.0._` - configurazione degli aspetti sul tavolo da parte dell'utente
>
> `v0._._` - versioni MVP pre-rilascio
</details>

---
Il programma, utilizzando una rete neurale, **risolve e organizza automaticamente** le note di ricerca nella tabella di ricerca.
L'intera interfaccia di interazione è traslucida e appare sopra tutte le finestre.

Il programma non interagisce **in alcun modo** con il codice del gioco e non viene rilevato dagli anti-cheat. 
Tutto ciò che fa è guardare i **pixel sullo schermo** e, con l'aiuto di una rete neurale, simula **azioni con mouse e tastiera**, come se fosse una persona a farlo.

> [!IMPORTANTE]
> Per qualsiasi domanda, errore e suggerimento scrivere a: [t.me/Tyapkin_S](https://t.me/tyapkin_s)

<details> <summary>Elenco dei componenti aggiuntivi supportati (espandi...)</summary>

- Api magiche
- Magia proibita
- Avarizia
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

---


# Come usarlo?
### Preimpostato 
> _Eseguito una volta dopo il primo avvio del programma_
0. Scarica il programma da [releases](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
1. Dimostrazione e verifica della possibilità di spostamento del mirino. 
Basta spostare il punto rosso su quello giallo.
_MD_WDGT_41b954938papà472391990e843a066793
2. È necessario indicare al programma dove si trova l'interfaccia della tabella di ricerca. 
Per fare ciò è necessario spostare gli angoli del rettangolo giallo in modo che corrano lungo il perimetro esterno del tavolo, come mostrato nello screenshot qui sotto
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/find_table.png?raw=true)
3. È necessario far sapere al programma in modo più dettagliato dove si trovano i pulsanti di interazione all'interno della tabella degli incantesimi.
Per fare ciò, sposta tutti i punti come mostrato nello screenshot qui sotto
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_controls.png?raw=true)
4. Seleziona la tua versione Thaumcraft e tutti i componenti aggiuntivi installati
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_version_and_addons.png?raw=true) 

Dopo aver completato tutti questi passaggi, tutte le selezioni dell'utente vengono salvate nella cartella `C://users/%USER%/.ThaumcraftAutoResearcher`,
al successivo avvio del programma non sarà necessario eseguire questa operazione; verrà mostrato immediatamente il passo successivo.
Puoi sempre tornare alla configurazione premendo il tasto "Backspace".

### Risoluzione delle catene di aspetti
1. **Inserisci una nota di ricerca** dallo slot dell'inventario in alto a sinistra nello slot del tavolo di ricerca
Dopo aver premuto "Invio", inizierà il processo di determinazione degli aspetti sul campo utilizzando una rete neurale.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/prepare_to_solving_aspects.png?raw=true)
Una soluzione verrà generata automaticamente utilizzando catene di aspetti, che il programma pubblicherà ![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_solved.png?raw=true)

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
3. **Dopo aver finito di esporre gli aspetti**, la nota di ricerca verrà inserita nell'inventario,
e al suo posto si mette sul tavolo quello successivo dell'inventario.
Quindi il processo si ripeterà di nuovo. In questo modo puoi risolvere un gran numero di note che si trovano nell'inventario una dopo l'altra
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/next_research_putted.png?raw=true)

> [!CONSIGLIO]
> - Affinché le note di ricerca continuino ad essere esaminate una per una, così come sono nell'inventario, puoi premere `Ctrl+Invio`, quindi
Durante lo studio di ogni nota successiva, il programma non attenderà la conferma da parte dell'utente con il tasto "Invio", ma inizierà immediatamente a pubblicare la soluzione.

> [!CONSIGLIO]
> - Durante la disposizione degli aspetti viene fornita la combinazione di tasti `Ctrl+Shift+Alt` nel caso in cui sia necessario terminare urgentemente il programma.


----------


## Nelle versioni future...
- Rilevamento automatico degli aspetti disponibili nella tabella e della loro quantità, costruendo catene basate su queste informazioni.
- Velocità adattiva a seconda degli FPS nel gioco
- Controllo della correttezza delle catene stese
- Monitoraggio dello stato del serbatoio dell'inchiostro
- Traduzione in altre lingue all'interno applicazioni


----------

# Esegui dal sorgente:
1. Installa le dipendenze:
```shell
pip install -r requirements.txt
```

2. Esegui dalla root del progetto (richiede `Python 3.10` o versione successiva):
```shell
python ./src/main.py
```

---
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

4. ***\[Passaggio facoltativo]*** Nella sezione **Avanzate**, specificare `--upx-dir` (il percorso della cartella con il file eseguibile `upx.exe`) ed eseguire la build .
Il file exe compilato apparirà nella cartella "output" in questa directory

---
### Un ringraziamento speciale
- [Acak1221](https://github.com/acak1221) per creare la rete neurale utilizzata dal programma
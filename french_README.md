![GithubCI](https://github.com/SergTyapkin/thaumcraft-auto-researcher/actions/workflows/auto-translate-readme.yml/badge.svg)

[![](https://img.shields.io/badge/русский-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/russian_README.md)
[_MD_WDGT_c1fca2ee0d6b4a0da9f76 474abf0221e](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/english_README.md)
[![](https://img.shields.io/badge/中文(简体)-_?style=for-the-badge&logo=readme&color=white)](https://github. com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/chinese%20(simplified)_README.md)
[![](https://img.shields.io/badge/中文(传统)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/chinese%20(traditional)_README.md)
[![](https://img.shields.io/badge/arabic(العربية)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraf t-auto-researcher/blob/README_TRANSLATIONS/arabe_README.md)
[![](https://img.shields.io/badge/español-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/espagnol_README.md)
[_MD_WDGT_f58 6f5b3e23c42488ca37adc8a28bbd2](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/italian_README.md)
[![](https://img.shields.io/badge/Deutsch-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-au à-chercheur/blob/README_TRANSLATIONS/néerlandais_README.md)
[![](https://img.shields.io/badge/hindi(हिन्दी)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRAN SLATIONS/hindi_README.md)
[![](https://img.shields.io/badge/korean(한국어)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/korean_README.md)

# Outil automatique pour Thaumcraft 4 > _**Thaumcraft**_ - un module pour les jeux _Minecraft_, qui est utilisé dans les modules de jeux magiques les plus populaires serverah
## [Télécharger les versions .exe](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
[dernière version `v1.1.3`](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases/tag/v1.1.3)
<details>
<summary>Journal des modifications :</summary>

- Les configurations sont enregistrées dans AppData. Au redémarrage, vous n'avez plus besoin de reconfigurer l'application
- Désormais, le réseau de neurones détermine les aspects sur la table !
Grâce à cela, la vitesse de recherche a été multipliée par plus de 10.
- Vitesse améliorée du réseau neuronal grâce à sa mise en cache locale
- Ajout de raccourcis clavier pour un contrôle plus fin
- Ajout du mode de recherche non-stop

> `v1.1._` - configuration des aspects sur la table par un réseau de neurones avec possibilité de modification par l'utilisateur
>
> `v1.0._` - configuration des aspects sur la table par l'utilisateur
>
> `v0._._` - versions préliminaires de MVP
</details>

---
Le programme, à l'aide d'un réseau neuronal, **résout et organise automatiquement** les notes de recherche dans le tableau de recherche.
L'ensemble de l'interface d'interaction est translucide et apparaît au-dessus de toutes les fenêtres.

Le programme n'interagit **en aucune façon** avec le code du jeu et n'est pas détecté par les anti-triche. 
Tout ce qu'il fait, c'est regarder les **pixels sur l'écran** et, à l'aide d'un réseau neuronal, il simule des **actions avec une souris et un clavier**, comme si une personne le faisait.

> [!IMPORTANT]
> Pour toute question, erreur et suggestion, écrivez : [t.me/Tyapkin_S](https://t.me/tyapkin_s)

<details>
<summary>Liste des modules complémentaires pris en charge (développer...)</summary>

- Abeilles magiques
- Magie interdite
-Avaritie
-GregTech
- GregTech NewHorizons
- Bottes thaumiques
- Addons botaniques
- L'Elysée
- Révélations thaumiques
- Thaumaturgie essentielle
- Intégration d'AbyssalCraft
</details>

https://github.com/user-attachments/assets/a2eaa3b7-c7fe-4fbc-9905-1b19a32d498f

---


# Comment l'utiliser ?
### Préréglage 
> _Exécuté une fois après le premier démarrage du programme_
0. Téléchargez le programme depuis [versions](https://github.com/SergTyapkdans/thaumcraft-auto-researcher/releases)
1. Démonstration et vérification que le réticule peut être déplacé. 
Déplacez simplement le point rouge vers le jaune.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/enroll.png?raw=true)
2. Vous devez indiquer au programme où se trouve l'interface de la table de recherche. 
Pour ce faire, les coins du rectangle jaune doivent être déplacés afin qu'ils longent le périmètre extérieur de la table, comme indiqué dans la capture d'écran ci-dessous.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/find_table.png?raw=true)
3. Il est nécessaire d'indiquer au programme plus en détail où se trouvent les boutons d'interaction à l'intérieur de la table d'enchantement.
Pour ce faire, déplacez tous les points comme indiqué dans la capture d'écran ci-dessous
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_controls.png?raw=true)
4. Sélectionnez votre version de Thaumcraft et tous les addons installés
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_version_and_addons.png?raw=true) 

Après avoir terminé toutes ces étapes, toutes les sélections de l'utilisateur sont enregistrées dans le dossier `C://users/%USER%/.ThaumcraftAutoResearcher`,
la prochaine fois que vous démarrerez le programme, il n'est pas nécessaire de le faire ; l'étape suivante s'affichera immédiatement.
Vous pouvez toujours revenir à la configuration en appuyant sur la touche « Retour arrière »

### Résolution des chaînes d'aspect
1. **Placez une note de recherche** de l'emplacement d'inventaire en haut à gauche dans l'emplacement de la table de recherche
Après avoir appuyé sur « Entrée », le processus de détermination des aspects sur le terrain à l'aide d'un réseau neuronal commencera.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/prepare_to_solving_aspects.png?raw=true)
Une solution sera automatiquement générée à l'aide de chaînes d'aspects, que le programme va publier
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_solved.png?raw=true)

> [!ASTUCE]
> Si la chaîne d'aspect est trop grande ou utilise des aspects que vous n'avez pas, appuyez sur `R` pour la régénérer
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/aspects_rerolled.png?raw=true)

> [!ASTUCE]
> Si vous devez faire quelque chose dans le jeu pour que le jeu ne chevauche pas l'interface du programme, vous pouvez appuyer sur « Ctrl+Shift+Espace », et
le programme se mettra en pause jusqu'à ce que vous appuyiez à nouveau sur cette combinaison de touches.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/program_paused.png?raw=true)

> [!ASTUCE]
> Si l'une des cellules est mal définie, vous pouvez cliquer sur la cellule et sélectionner quelle cellule elle doit réellement être.UN.
Après cela, la solution sera automatiquement régénérée
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects.png?raw=true)
2. **Assurez-vous qu'il y a suffisamment d'encre dans le réservoir d'encre**. S'ils sont épuisés, l'algorithme de présentation des aspects ne s'arrêtera pas,
et les notes de recherche ne seront pas résolues.
Appuyez ensuite sur « Entrée » et le processus de disposition des aspects sur la table en fonction des chaînes résultantes commencera.
3. **Après avoir fini de présenter les aspects**, la note de recherche sera placée dans l'inventaire,
et à sa place, le suivant de l'inventaire est placé sur la table.
Ensuite, le processus se répétera. De cette façon, vous pouvez résoudre un grand nombre de notes dans l'inventaire les unes après les autres.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/next_research_putted.png?raw=true)

> [!ASTUCE]
> - Pour que les notes de recherche continuent d'être examinées une à une, telles qu'elles sont dans l'inventaire, vous pouvez appuyer sur `Ctrl+Entrée`, puis
Lors de l'étude de chaque note suivante, le programme n'attendra pas la confirmation de l'utilisateur avec la touche « Entrée », mais commencera immédiatement à publier la solution.

> [!ASTUCE]
> - Lors de la présentation des aspects, la combinaison de touches « Ctrl+Shift+Alt » est fournie au cas où il serait nécessaire de terminer d'urgence le programme.


----------


## Dans les futures versions...
- Détection automatique des aspects disponibles dans le tableau et de leur quantité, construisant des chaînes basées sur ces informations.
- Vitesse adaptative en fonction du FPS du jeu
- Vérifier l'exactitude des chaînes disposées
- Suivi de l'état du réservoir d'encre
- Traduction dans d'autres langues au sein de l'application


----------

# Exécuter à partir des sources :
1. Installez les dépendances :
```shell
pip install -r requirements.txt
```

2. Exécutez à partir de la racine du projet (nécessite « Python 3.10 » ou supérieur) :
```shell
python ./src/main.py
```

---
## Créez l'application dans un fichier .exe
1. Installez les dépendances et le générateur :
```shell
pip install -r requirements.txt
pip install auto-py-to-exe
```

2. ***\[Étape facultative]*** Téléchargez UPX (réduit la taille du fichier exe final)
https://github.com/upx/upx/releases/


3. Exécutez la commande build à partir de la racine du projet (ouvrira une interface à partir de laquelle vous pourrez exécuter la build) :
```shell
auto-py-to-exe -c .\pyinstaller_configs\autoPyToExe.json
```

4. ***\[Étape facultative]*** Dans la section **Avancé**, spécifiez `--upx-dir` (l'emplacement du dossier contenant le fichier exécutable `upx.exe`) et exécutez la build.
Le fichier exe compilé apparaîtra dans le dossier « output » de ce répertoire

---
### Remerciements particuliers
- [Acak1221](https://github.com/acak1221) pour créer le réseau neuronal utilisé par le programme
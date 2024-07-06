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


# Appareil automatique pour Thaumcraft 4
> _**Thaumcraft**_ - un module pour les jeux _Minecraft_, qui est utilisé dans les modules de jeux magiques sur les serveurs populaires

Le programme **récupère automatiquement et étend** les informations sur les informations volées.
Vous avez des interactions très dangereuses et vous avez des problèmes avec vous.

Le programme **никак** n'est pas compatible avec les jeux de code ni n'utilise des anticipats. 
C'est ce qui s'est passé - cela s'est produit sur **les pixels de l'écran** et a simulé **la musique et le clavier**, car c'est ce que vous avez fait.

---

## [Releases](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
[latest version `v1.0.0`](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases/tag/v1.0.0)
<details>
<summary>Journal des modifications : </summary>

- Улучшено качество решения цепочек а lunettes
- La résolution des chaînes d'aspect a été accélérée d'environ 2 fois
- Ajout de la journalisation aux fichiers .log dans l'exécutable .exe
- Ajout d'un bouton de fermeture
</details>


Pour toute question, erreur ou suggestion, écrivez à : [t.me/tyapkin_s](https://t.me/tyapkin_s)

## Mode opératoire
### La configuration initiale
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

Après avoir effectué toutes ces actions, toutes les sélections de l'utilisateur sont enregistrées,
la prochaine fois que vous démarrerez le programme, il n'est pas nécessaire de le faire ; l'étape suivante s'affichera immédiatement.
Vous pouvez toujours revenir à la configuration en appuyant sur la touche « Retour arrière »

### Résolution des chaînes d'aspect
1. Les notes de recherche de l'emplacement d'inventaire en haut à gauche seront automatiquement placées dans le tableau de recherche.
Cliquez sur un aspect existant dans le champ et sélectionnez-le dans la liste des aspects
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects.png?raw=true)
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects_1.png?raw=true)
2. Pour tous les autres aspects, faites de même et marquez également toutes les cellules dans lesquelles
les aspects ne peuvent pas être placés (vides). Cela devrait ressembler à la capture d'écran ci-dessous :
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects_2.png?raw=true)
3. Si la chaîne d'aspects est trop grande ou utilise des aspects que vous n'avez pas, appuyez sur « R » pour la régénérer.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects_3.png?raw=true)
4. Avant de commencer, assurez-vous que votre réservoir d'encre contient suffisamment d'encre. S'ils sont épuisés, l'algorithme de présentation des aspects sera interrompu.
Appuyez ensuite sur « Entrée » et le processus de disposition des aspects sur la table en fonction des chaînes résultantes commencera.
5. Après avoir fini de présenter les aspects, la note de recherche sera placée dans l'inventaire,
et à la place de cela dans s Les éléments suivants de l'inventaire sont placés.
Le processus peut être relancé. De cette façon, vous pouvez résoudre un grand nombre de notes dans l'inventaire les unes après les autres.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/solving_done.png?raw=true)


## Dans les versions futures
- Détection automatique des aspects sur la table à l'aide d'un réseau neuronal.
- Détection automatique des aspects disponibles dans le tableau et de leur quantité, construisant des chaînes basées sur ces informations.
- Modification des configurations sources
- Vérifier l'exactitude de la détermination des aspects initiaux
- Vérifier l'exactitude des chaînes disposées
- Plus de versions et d'addons pris en charge
- Suivi de l'état du réservoir d'encre
- Traduction dans d'autres langues au sein de l'application

---
## Exécuter à partir des sources :
1. Installez les dépendances :
```shell
pip install -r requirements.txt
```

2. Exécutez à partir de la racine du projet (nécessite « Python 3.10 » ou supérieur) :
```shell
python ./src/main.py
```
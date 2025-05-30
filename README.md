# Doeraene super platformer - Jeu en Python avec Arcade

Bienvenue dans **Doeraene super platformer**, un jeu de plateforme en 2D que nous avons entièrement codé avec Python en utilisant la bibliothèque [Arcade](https://api.arcade.academy/en/latest/). C’est un jeu de réflexion et d’exploration dans un univers de créatures, de portails, d’interrupteurs, et d’énigmes !

---

##  C’est quoi ce jeu ?

C’est un jeu dans lequel vous incarnez un personnage qui se déplace dans un monde rempli de:
- **plateformes mouvantes**
- **monstres à éviter ou neutraliser**
- **leviers à activer**
- **portes à ouvrir**
- **portails à traverser**
- **pièces à récupérer**

Chaque élément du jeu (monstres, portes, interrupteurs, etc.) est modélisé par des **classes Python**. Par exemple :
- `Switch` représente les interrupteurs à activer.
- `Gate` sont des portes qui s’ouvrent avec les interrupteurs.
- `Portal` modélise les portails de téléportation.
- `Bat` et `Blob` sont des monstres avec des mouvements différents.
- `PBlock`, `HBlock` et `VBlock` définissent des zones de plateformes dynamiques.

---

## Règles et astuces
### Objectif
Tout simplement, finir le niveau. Pour ceci il sera nécéssaire de passer par le panneau **Exit**. Mais attention! Celui-ci n'eat que disponible une fois que le nombre nécéssaire de pièces est collectionné. Celui-ci s'affiche en bas à droite de l'écran et est unique à chaque niveau.

### Armes
Le joueur est équippé de deux armes: 

- L'**épée**, qui tranche ses ennemis au moindre contact, l'arme idéale pour du corps-à-corps

- L'**arc**, qui de ses flèches permet de tuer à longue distance de ses ennemis

Afin de les manier, appuyez sur le ***click gauche*** de votre souris/trackpad. Changer d'arme équipée peut être fait en appuyant sur le ***click droit***. L'arme sera orientée dans la direction de la souris (par rapport au joueur).


### Monstres

Il y a deux types de monstres que vous pourrez rencontrer: 
- Les **Blobs**, des monstres lents qui parcours les sols de la map. 
- Les **Bats**, des chauves-souris impardonnables qui èrent les cieux des niveaux. N'hésitez pas à sortir votre arcs pour les neutraliser!

### Dangers

Un moindre contact avec ces monstres vous sera fatal. Vous mourrez également au contact de la ***lave*** ainsi qu'une chute dans le ***vide absolu***. Le niveau sera alors recommancé. 

### Interrupteurs

Vous trouverez sur la map des ***interrupteurs***. Activez les au contact de votre épée, arc ou d'une flèche afin de faire apparaître/disparraître:

- Les ***portes***, qui peuvent s'ouvrir afin de dévoiler un passage, ou se fermer afin de dévoiler un chemin. Ces portes sont solides, elle vous empêchent de passer, et vous permettent de marcher dessus

- Les ***portails***, qui vous téléportent à leur lieu d'arrivée. Lorsque qu'un interrupteur active un portail, il apparaîtra ainsi que le portail d'arrivée. Passez à travers pour vous téléporter! Le portail d'arrivée fait uniquement acte de présence: vous ne pouvez pas revenir en arrière! Une fois que les portail ont été utilisés, ils disparaîssent.

Certains interrupteurs ne peuvent être utilisés qu'une certain nombre de fois. Si votre arme ne l'active plus, elle n'est pas défaillante: c'est l'interrupteur qui résiste.

## Lancer le jeu

### Prérequis

Assurez-vous d’avoir installé :
<!-- Instructions: on suppose que les amis ont uv installé -->

- Python (version 3.10+ recommandée)
- [Arcade](https://pypi.org/project/arcade/)


```bash
uv add arcade
```

### Commande de démarrage


Lancez le jeu à l'aide de cette commande:
```bash
uv run main.py
```


### Amusez vous bien!



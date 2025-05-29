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

Chaque élément du jeu (monstres, portes, interrupteurs, etc.) est modélisé par des **classes Python**. Par exemple :
- `Switch` représente les interrupteurs à activer.
- `Gate` sont des portes qui s’ouvrent avec les interrupteurs.
- `Portal` modélise les portails de téléportation.
- `Bat` et `Blob` sont des monstres avec des mouvements différents.
- `PBlock`, `HBlock` et `VBlock` définissent des zones de plateformes dynamiques.

---

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



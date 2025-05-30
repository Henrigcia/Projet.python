# Design

## Class Diagram

```mermaid
classDiagram

%% Base Arcade types (no boxes)
GameView --|> arcade.View
Monster --|> arcade.Sprite
Switch --|> arcade.Sprite
Portal --|> arcade.Sprite
Bat --|> Monster
Blob --|> Monster

%% GameView
class GameView {
    +List~arcade.SpriteList~ sprite_lists
    +List~Tuple~ vectors
    +List~bool~ booleans
    +List~int~ integers

    +setup()
    +load_map()
    +on_draw()
    +on_key_press(key, modifiers)
    +on_mouse_press(x, y, button, modifiers)
    +on_update(delta_time: float)
    +camera()
    +reset_game()
}

%% GameView dependencies (imports)
GameView ..> Gate
GameView ..> Switch
GameView ..> Portal
GameView ..> Monster
GameView ..> Blob
GameView ..> Bat
GameView ..> Platforms
GameView ..> HSeries
GameView ..> VSeries
GameView ..> ConnectedCells
GameView ..> PBlock
GameView ..> HBlock
GameView ..> VBlock

%% Monster base
class Monster {
    +float center_x
    +float center_y

    +move_monster()
    +kill_monster()
}



%% Bat subclass
class Bat {
    +float fix_center_x
    +float fix_center_y
    +float area_x
    +float area_y
    +int frames

    +distort_movement()
}

%% Gate
class Gate {
    +int x
    +int y
    +bool active

    +open()
    +open_gate()
    +close_gate()
}

%% Switch



class Switch {
    +int x
    +int y
    +arcade.Sprite appearance
    +bool status = False
    +bool disabled = False
    +List~SwitchAction~ switch_on
    +List~SwitchAction~ switch_off
    +float last_hit = 0

    +update(delta_time: float = 1/60)
    +change_gate(gate: Gate)
    <<static>>
    +switchdraw(switch: Switch) arcade.Sprite

    +toggle()
    +action()
    +switch_action_on()
    +switch_action_off()
}

class SwitchAction {
    +Kind kind
    +int x
    +int y
    +int go_x
    +int go_y
}

class Kind {
    +open_gate: str
    +close_gate: str
    +open_portal: str
    +disable: str
}

Switch *-- SwitchAction : contains
SwitchAction ..> Kind : uses


%% Portal
class Portal {
    +int x
    +int y
    +int teleport_x
    +int teleport_y
    +arcade.Sprite connected

    +action_portal()
}

%% ConnectedCells hierarchy

class ConnectedCells {
    +set~tuple~ cells
    +set~tuple~ visited
    +list~list~ islands

    +get_neighbors()
    +DFS()
    +build_islands()
}

class Platforms {
    +get_neighbors()
}

class HSeries {
    +get_neighbors()
}

class VSeries {
    +get_neighbors()
}

Platforms --|> ConnectedCells
HSeries --|> ConnectedCells
VSeries --|> ConnectedCells

%% PBlock base
class PBlock {
    +float boundary_low
    +float boundary_high
    +float d_a
    +float d_b
    +arcade.SpriteList~arcade.Sprite~ platform_list

    +add_platform()
}

class HBlock {
    +add_platform()
}

class VBlock {
    +add_platform()
}

HBlock --|> PBlock
VBlock --|> PBlock

%% Inheritance connections
Monster --|> arcade.Sprite
Switch --|> arcade.Sprite
Portal --|> arcade.Sprite
Blob --|> Monster
Bat --|> Monster

```

## Analyse de Complexité — `load_level`

Nous pouvons calculer la complexité théorique de nos deux fonctions comme suit :

### `load_level`

Notre fonction, qui charge la map et s'occupe des mouvements des blocs, commence par lire sur chaque ligne les signes présents dans le dictionnaire de symboles.  
Nous sommes donc en **O(n)**.

Or, chaque cellule qui est une liste de blocs avec leurs positions est ensuite de nouveau parcourue pour créer le chemin des plateformes. Mais la fonction doit aussi parcourir les colonnes également. Donc la fonction doit parcourir ligne et colonne. Ainsi, on se retrouverait donc en au plus **O(n x m)**.

> Où `n` et  `m` sont les lignes et colonnes de la map.  
> Cependant on peut noter qu'il y a une très légère variation de temps de chargement entre les agmentations d'entités comme expliqué ci-dessous.

### Temps d'exécution de `load_level` en fonction du nombre de blobs

# Analyse des Temps d'Exécution - Fonction `load_level`

## Données Mesurées

### Pour Taille Double

| Test | Temps Initial (s) | Temps après Augmentation (s) |
|------|--------------------|------------------------------|
| 1    | 0.027755970429861918 | 0.028490098790207412       |
| 2    | 0.01896880860993406  | 0.017972407710039988       |
| 3    | 0.04006303873000434  | 0.04369001929997467        |
| 4    | 0.05778578641009517  | 0.06058161033986835        |
| 5    | 0.05781755476986291  | 0.05971685093012638        |
| 6    | 0.08264228809974156  | 0.08546410908980761        |

### Pour Taille Triple

| Test | Temps Initial (s) | Temps après Augmentation (s) |
|------|--------------------|------------------------------|
| 1    | 0.027506365400040523 | 0.030002202509786004      |
| 2    | 0.017484945190080908 | 0.018159345540043434      |
| 3    | 0.03974397553014569  | 0.04194625606003683       |
| 4    | 0.0585319597797934   | 0.060174164710042534      |
| 5    | 0.05781747670000186  | 0.058971569929854015      |
| 6    | 0.08631786619022024  | 0.0880277935101185        |

### Pour Taille Quadruple

| Test | Temps Initial (s) | Temps après Augmentation (s) |
|------|--------------------|------------------------------|
| 1    | 0.030608712949906476 | 0.028147280380071606      |
| 2    | 0.018413947929802818 | 0.018724664979963564      |
| 3    | 0.03965045527991606  | 0.041414136849925856      |
| 4    | 0.05758686486020451  | 0.06724758060998283       |
| 5    | 0.057213650009944106 | 0.09630883875011932       |
| 6    | 0.07942514786001993  | 0.13672808399016503       |

---

## Résultats

- Les temps mesurés après augmentation restent **très proches** des temps initiaux.
- Les écarts sont faibles et semblent plutôt constants.


### Rapports Moyens des Temps (approximation)

- Pour **taille double** : rapports proches de **1.01** à **1.05**  
- Pour **taille triple** : rapports proches de **1.01** à **1.05**  
- Pour **taille quadruple** : rapports variables, mais généralement ≤ **1.2**.

---

## Conclusion sur la Complexité

La fonction **`load_level`** semble présenter une **complexité proche de linéaire (O(n x m))** :  
Les temps d’exécution n’augmentent que marginalement lorsque la taille des données est doublée, triplée ou quadruplée.  

## Analyse de Complexité — `on_update`

Ici, on peut calculer chaque partie que exécute la fonction `on_update`.  
La plupart des calculs se font à travers la recherche d'éléments dans une liste.

À chaque fois qu'on fait une recherche, une suppression, un ajout ou une vérification de collision, on est en **O(n)**,  
où `n` est le nombre d’éléments dans la liste.

Or, certains éléments (flèches, etc.) dépendent d'autres paramètres comme les murs, les plateformes, ou encore la taille de la map.  
Ainsi, presque chaque liste varie entre **O(n)** et **O(n²)**.

En sommant chaque portion de code, on peut conclure que la complexité globale de notre fonction `on_update` se rapproche de **O(n²)**.

# Analyse des Temps d'Exécution

## Données Mesurées

| Test | Temps Initial (s)   | Temps après Augmentation (s) |
|------|---------------------|------------------------------|
| 1    | 0.0002614976830082014 | 0.0008421041060064454       |
| 2    | 0.0002620382030145265 | 0.001358495810010936       |
| 3    | 0.0002545341759978328 | 0.06340233693100163        |
| 4    | 0.00033160607499303297| 0.062059607645001964       |
| 5    | 0.00041971688999910836| 0.06296813303400996        |
| 6    | 0.0002747605479962658 | 0.00043539295499795116     |
| 7    | 0.0002069993560144212 | 0.002476617988024373       |
| 8    | 0.00022044210400781595| 0.001094399881985737       |
| 9    | 0.000241684228007216  | 0.0019125435989990364      |

## Intérpretation

- On voit nettement une grosse augmentation du temps entre la map initiale et celle augmentée.
- La croissance est donc au moins linéaire.

## Résultats

- **Rapport moyen des temps après augmentation / temps initial** : environ **69**.
- Cela suggère une augmentation des temps d’exécution bien plus forte qu’une croissance linéaire.

## Conclusion sur la Complexité

Les résultats empiriques suggèrent une **complexité quadratique (O(n²))**.  
On remarque l’augmentation est beaucoup plus marquée, indiquant la présence de boucles imbriquées ou d’interactions croisées qui font croître le coût en O(n²).



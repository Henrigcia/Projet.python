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

Or, chaque cellule qui est une liste de blocs avec leurs positions est ensuite de nouveau parcourue pour créer le chemin des plateformes. Ainsi, on se retrouverait donc en **O(n²)** car en plus de parcourir la map a la recherche de cellule on parcourt les cellules en elles-mêmes.

> Où `n` est la taille de la map.  
> On le voit bien lorsqu'on fait varier le paramètre de la largeur et la hauteur de celle-ci car le temps augemente entres les différentes maps.

### Temps d'exécution de `load_level` en fonction du nombre de blobs

![Temps d'exécution](00b53f51-7bcc-4248-9352-e8966094b09a.png)

Sur ce graphique on peut noter comment évolue la différence de temps d'appel entre les différentes cartes. On peut voir qu'il y a une légère stabilité mais celle-ci n'est pas constante avant que la taille ne quadruple et dès que la taille quadruple on s'aperçoit que la différence commence peu à peu à croître de manière quadratique. Ainsi à partir de la taille quadruplée notre fonction sera bel et bien en **O(n²)**. Ce qui convient avec les calculs théoriques.


## Analyse de Complexité — `on_update`

Ici, on peut calculer chaque partie que exécute la fonction `on_update`.  
La plupart des calculs se font à travers la recherche d'éléments dans une liste.

À chaque fois qu'on fait une recherche, une suppression, un ajout ou une vérification de collision, on est en **O(n)**,  
où `n` est le nombre d’éléments dans la liste.

Or, certains éléments (flèches, etc.) dépendent d'autres paramètres comme les murs, les plateformes, ou encore la taille de la map.  
Ainsi, presque chaque liste varie entre **O(n)** et **O(n²)**.

En sommant chaque portion de code, on peut conclure que la complexité globale de notre fonction `on_update` se rapproche de **O(n²)**.

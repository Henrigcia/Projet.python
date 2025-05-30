# Journal

## Progression

Format :

    * [fait/à faire] Tâche      Durée (en minutes; remplacer les ??)

Ajoutez au fur et à mesure les tâches qui seront demandées chaque semaine.
Vous pouvez ajouter vos propres tâches si vous le jugez utile (p.ex. avec une décomposition plus fine).

* [x] Créer le LOG.md                                                  1
* [x] S'inscrire en binôme                                             1
* [x] Découverte d'Arcade                                              120
* [x] Meilleure gestion du clavier                                     100
* [x] Meilleure gestion de la caméra                                   180
* [ ] `README.md` à jour, expliquant comment jouer                     45
* [x] Charger la map depuis un fichier                                 120
* [x] Implémenter la lave                                              20
* [x] Blobs: mouvement                                                 150
* [x] Epée: apparition et dégats                                       200
* [x] Epée: angle et placement                                         50
* [x] Score: pièces                                                    30
* [x] Score: texte                                                     10
* [x] Chauves souris: mouvement                                        120
* [x] Niveaux                                                          180 
* [x] Arc angle                                                        150
* [x] Flèches: vitesse apparition et dégats                            240
* [x] Panneau et lecture de prochaine map                              120
* [x] Lecture de carte                                                 180
* [x]Creation d'un algo pour platformes en manuel                      90
* [x] Plateformes qui bougent                                          180
* [x] Gates et levier (lecture YAML)                                   1500
* [x] Portails                                                         750
* [x] Pixel art Doeraene et direction du sprite                        45
* [x] Lecture de flèches map pour les platformes                       360  
* [x] Score contrainte                                                 60
* [x] Affichage de mort etc                                            30
* [x] Refactoring et relecture des fichiers                            800
* [x] Tous les tests                                                   300
* [x] Design: mermaid graph                                            90

---

## À faire (prochaine étape)

Mettez ici ce que vous pensez devoir être la ou les 2 prochaines étapes pour chacune/chacun.

---

## Suivi

### Semaine 2
Création de projet et suivi du tutoriel il a fallu gérer la gravité par rapport au joueur et chargement de la map ainsi que l'affichage de certains objets sur la map.
### Semaine 3
Charger la map depuis un fichier s'avérait être plus difficile que prévu. Nous avons fini par réussir. Des modifications ont du être implémentée à ce sujet lors du rajout des levier et des portes (lecture YAML). La lave en "no-go" était plutºt facile à réaliser. Mouvement des blobs à finaliser la semaine prochaine.
### Semaine 4
Finalisation du mouvement des blobs. Faire apparaitre l'épée était basic. Les calculs de vecteurs et d'angles sont une autre histoire... Pour l'insant, le direction de l'épée n'est que correcte dans le premier cadran trigonométrique.
### Semaine 5
Nous avons réussi avec succès l'orientation de l'épée. Elle change même de main en fonction de l'angle! Nous avons changé l'implémentation d'une "arme" afin qu'elle prenne en compte l'arc.
Création des chauves souris et de l'arc, problématique de la limite de déplacement de la chauve-souris, et d'une mouvement le plus "smooth" possible. Pour l'arc, les flèches disparaissent une fois que l'arc n'est plus dessiné. De plus, la flèche a une vitesse constante delon l'axe y: à corriger la semaine prochaine!
### Semaine 6
Ici on a refactoré plusieurs aspects de notre code afin de avoir un code plus lisible. Ajout de la classe Monster afin d'éviter la duplication de code liée aux monstres. Finalisation des flèches a pris énormément de temps également. On peut maintenant tirer plusieurs flèches à la fois (création de arrow list) et leur vitesse dépend de leur angle dans le on_update. 
### Semaine 7
Ici encore des améliorations du code avec du refactoring. Rien de précis à signaler.
### Semaine 8
Création des platformes en manuel avec une classe à part. Cération des classes Switch et Gate. Recherche sur le fonctionnement de YAML et beaucoup de difficulté à en extraitre des informations lisibles et utiles. PS: Heureusement qu'il nous reste 2 semaines pour ceci 
### Semaine 9
Beaucoup de changements pour les switch et gate. Class Action créée et essais d'implémenter cette lecture YAML dans GameView. Pour l'instant, les gates disparaissent mais leur hitbox est toujours là (problématique d'avoir mis gate dans wall_list probablement). Les switch garde les 2 sprites associés à "on" et "off".m
### Semaine 10
Réflexion d'un algorithme pour faire bouger les platformes. Finalisation des switch et gate. Presque tout marche, à part quelques collisions et le fait que l'épée active le switch plusieurs fois (Car sa collision est sur plusieures frames) -> Nous aurons surement besoin d'un delta time lié aux switches.
### Semaine 11
Le mouvement des platformes presque terminé. Création de nouveau fichier afin d'espacier le code, algo de lecture de carte trouvé. Il reste à gérer les fleches. Gates et Switch terminés! Le delta time que nous avions évoqués la semaine passée a marché à merveille! Toutefois, les gates ouvertes en début du loading de map apparaissent comme fermées...
### Semaine 12
Création algo pour lecture de flèches et finalisation des platformes bougeantes. Finalisation des platformes et de la lecture des flèches. Gates complètement finies 
### Semaine 13
Finalisation des gates et platformes, notemment pour des cas spéciaux, comme la lave ou les leviers. Implémentations personnelles: Ajout de la classe Portal qui gère la téléportation du joueur. Réflexion des fonctions qui les feront fonctionner, et ajout d'un Portal "d'arrivée", qui est uniquement visuel (et donc on ne peut pas passer à travers). Contrainte du nombre de pièce pour terminer un niveau implémentée.
### Semaine 14
Finalisation du code refactoring et tests. Creation d'un message lorsque le joueur tente de changer de niveau sans assez de pièces. Création du schéma "mermaid" dans Design et tests de performance sur nos map et fonctions. Vérification de tout globalement. 
# Answers: Questions et réponses

### Comment avez-vous conçu la lecture du fichier ? Comment l’avez-vous structurée de sorte à pouvoir la tester de manière efficace ?

- À partir d'une liste de symboles, notre fonction load_level parcours les lignes et les colonnes du fichier text. Lorsque qu'il détecte un symbole de la liste (à l'aide de condition "if), il ajoute son sprite, avec les coordonnées ligne-colonne correspondantes à la liste de sprite correspondante au symbol. Les tests étaient purement manuels, en démarrant le programme et en regardant si tous les blocs apparaissent, et si ils sont au bon endroit. Avec un minimum de trail and error, notre fonction accomplit bien ses objectifs.


### Comment avez-vous adapté vos tests existants au fait que la carte ne soit plus la même qu’au départ ? Est-ce que vos tests résisteront à d’autres changements dans le futur ? Si oui, pourquoi ? Si non, que pensez-vous faire plus tard ?

* Nos tests étant purements manuels, nous répétions juste les étapes pour chaque nouveu symbol ou sprite. Pour les monstres, nous initialisons aussi leur direction et vitesse (plus la "limit box" pour les mouvement des chauve_souris) 


### Le code qui gère la lave ressemble-t-il plus à celui de l’herbe, des pièces, ou des blobs ? Expliquez votre réponse.

* Le code de la lave ressemble plus à celui des pièces. Ceci pour deux raisons principales: elle n'a pas de mouvement (contrairement aux blobs) et a un effet de collision avec le joueur(contrairement à l'herbe). Par élimination, nous estimons que son code est plus ressemblant à celui des pièces.

### Comment détectez-vous les conditions dans lesquelles les blobs doivent changer de direction ?

* La méthode move_monster vérifie à chaque instant si il y a une collision entre le blob et wall_list à la position du blob + sa taille selon x, et sa position y -1. Si le blob est à la fin d'une platforme, cette collision n'existera pas, dans ce cas il se retourne et change de direction de mouvement. Ceci prend en compte le cas où le prochain blob est de la lave (car elle n'est pas dans wall_list). Si le bloc se cogne contre un mur, il change également de direction


### Quelles formules utilisez-vous exactement pour l’épée ? Comment passez-vous des coordonnées écran aux coordonnées monde ?

* Nous crééons un le vecteur qui part du joueur jusqu'à la souris en utilisant la fonction unproject(). Ensuite nous normalisons ce vecteur (avec vec.normalise()), et à l'ide de formules trigonométriques adaptons l'orientation de l'épée.

### Comment testez-vous l’épée ? Comment testez-vous que son orientation est importante pour déterminer si elle touche un monstre ?

* Nous testons d'abord quatre orientations possibles (sud-ouest, nord-ouest, nord-est, sud-est), puis le joueur se téléporte et tape d'abord dans la direction opposée du blob. Après assertion que le blob est encore vivant, nous tapons dans le bon sens, et nous assurons qu'il est bien mort cette fois.

### Comment transférez-vous le score de la joueuse d’un niveau à l’autre ?

* Le score se réinitialise chaque niveau. Nous avons fait ce choix, car il était plus logique en raison des conditions de passage d'un niveau.

### Où le remettez-vous à zéro ? Avez-vous du code dupliqué entre les cas où la joueuse perd parce qu’elle a touché un ou monstre ou de la lave ? 

* Dans le load_level, il a suffit d'implémenter un "self.score=0". La joueuse ne perd pas ses pièces lorsqu'elle meurt. Aucune duplication de code à ce niveau là.

### Comment modélisez-vous la “next-map” ? Où la stockez-vous, et comment la traitez-vous quand la joueuse atteint le point E ?

* Le "next-map" apparait en haut de chaque fichier map.txt. Si next-map n'est pas encore défini, load_level charge la première map "FIRST_MAP". Si next-map est défini (accédé en lecture YAML), load_level charge la map en question.

### Que se passe-t-il si la joueuse atteint le E mais la carte n’a pas de next-map ?

* Dans ce cas, nous avons fait en sorte que load_level charge le fichier FIRST_MAP.

### Quelles formules utilisez-vous exactement pour l’arc et les flèches ?

* L'arc fonctionne exactement de la même manière que l'épée (On utilise le même vecteur et les mêmes formules). Les flèches adaptent leur vitesse au vecteur qui les constitue. Par exemple, plus la flèche est à son apogée plus elle est lente (Principe de ballistique basique). On appelle arrows.update() and la fonction on_update afin que leur vitesse et direction s'actualise à chaque frame.

### Quelles formules utilisez-vous exactement pour le déplacement des chauves-souris (champ d’action, changements de direction, etc.) ?

<!--Refaire stephan-->

* On leur crée un mouvement par défaut des monstres et ensuite on leur crée un champ d'action autour duquel ils peuvent naviguer. On distort leur mouvement avec les fonctions mathematiques de Arcade. On leur cree un sorte de rectangle autour et des qu'elles touchent la "limite" on leur randomise la direction avec un angle dans laquelle elles partent. On recalcule les vitesses dans les deux directions et on fait ce processus a chque fois que une chauve souris touche un "mur" invisible.

### Comment avez-vous structuré votre programme pour que les flèches puissent poursuivre leur vol ?

* Chaque nouveau tir crée une nouvelle flèche, indépendante du joueur, et des autres flèches. Elles pourront donc toutes avoir un mouvement et une direction différente.

### Comment gérez-vous le fait que vous avez maintenant deux types de monstres, et deux types d’armes ? Comment faites-vous pour ne pas dupliquer du code entre ceux-ci ?

* Nous avons créé une surclasse Monster pour les blobs et les chauve-souris, qui implémente leur mouvement simple, et leur mort. Pour les armes, une classe parente paraissait inutile, car seul de petits détails sont communs à l'arc et l'épée.

### Quel algorithme utilisez-vous pour identifier tous les blocs d’une plateformes, et leurs limites de déplacement ?

<!--Refaire stephan-->

Stephan:

* Notre algorithme prend un set des positions des blocs qui apparaissent la map et les stock. En lui definissant ce que constitue une platforme il va creer des iles de blocs en les rassemblant. Ensuite notre algo' regarde les blocs a gauche et a droite et au dessus et dessous et les place dans une liste avec les voisins de ceux-ci, ces voisins peuvent etre des condidats potentiels pour creer l'ile (platformes). De plus l'algo check si on a deja visite la cellule constituee de blocs. Si le voisin n'a pas deja ete visite et fait partie de la platforme on le rajoute dans la liste des blocs qui font la platforme. On itere sur toutes les coordonnees dans le set. En faisant tout ca il cree alors un set qui retourne les positions cette fois-ci des blocs qui constituent la platforme. Ainsi on obtient donc grace a cet algorithe toutes les positions des "iles" (platformes) que forment les differents blocs.  

### Sur quelle structure travaille cet algorithme ? Quels sont les avantages et inconvénients de votre choix ?

<!--Refaire stephan-->

Stephan:

* Il repose sur le fait de iterer sur les positions des blocs a travers la lecture de la carte. Le DFS va creer un arbre avec les differents blocs et leur voisins qu'il parcourt pour verifier que la definition de platfrome est efffectuee. Son gros avantage est que l'algo est plutot simple a implementer. Il est particulierement efficace dans notre cas pour former les differentes cellules (voisins dans le graphe) et iterer sur eux. Cependant la recherche grace au DFS (sur quoi repose l'algo) peut etre un peu lente s'il y a beaucoup de blocs et pas toujours optimale.

### Quelle bibliothèque utilisez-vous pour lire les instructions des interrupteurs ? Dites en une ou deux phrases pourquoi vous avez choisi celle-là.

* Nous utilisons PyYAML car elle semblait être la plus populaire, et aussi la plus téléchargée. Dans la confiance que nous apportons à la communauté de programmeurs, cela nous a suffit.

### Comment votre design général évolue-t-il pour tenir compte des interrupteurs et des portails ?

* L'implémentation du YAML dans notre programme n'a rien changé de particulier. Elle nous a cependant permis d'implémenter facilement les portails de téléportation (ajout personnel). 
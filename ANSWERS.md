# Answers: Questions et réponses

### Comment avez-vous conçu la lecture du fichier ? Comment l’avez-vous structurée de sorte à pouvoir la tester de manière efficace ?

- À partir d'une liste de symboles, notre fonction load_level parcours les lignes et les colonnes du fichier text. Lorsque qu'il détecte un symbole de la liste (à l'aide de condition "if"), il ajoute son sprite, avec les coordonnées ligne-colonne correspondantes à la liste de sprite correspondante au symbol. Les tests étaient purement manuels, en démarrant le programme et en regardant si tous les blocs apparaissent, et si ils sont au bon endroit. Avec un minimum de trial and error, notre fonction accomplit bien ses objectifs.


### Comment avez-vous adapté vos tests existants au fait que la carte ne soit plus la même qu’au départ ? Est-ce que vos tests résisteront à d’autres changements dans le futur ? Si oui, pourquoi ? Si non, que pensez-vous faire plus tard ?

* Nos tests étant purements manuels, nous répétions juste les étapes pour chaque nouveau symbole ou sprite. Pour les monstres, nous initialisons aussi leur direction et vitesse (plus la "limit box" pour les mouvement des chauve-souris) 


### Le code qui gère la lave ressemble-t-il plus à celui de l’herbe, des pièces, ou des blobs ? Expliquez votre réponse.

* Le code de la lave ressemble plus à celui des pièces. Ceci pour deux raisons principales: elle n'a pas de mouvement (contrairement aux blobs) et a un effet de collision avec le joueur(contrairement à l'herbe). Par élimination, nous estimons que son code est plus ressemblant à celui des pièces.

### Comment détectez-vous les conditions dans lesquelles les blobs doivent changer de direction ?

* La méthode move_monster vérifie à chaque instant si il y a une collision entre le blob et wall_list à la position du blob + sa taille selon x, et sa position y -1. Si le blob est à la fin d'une platforme, cette collision n'existera pas, dans ce cas il se retourne et change de direction de mouvement. Ceci prend en compte le cas où le prochain bloc est de la lave (car elle n'est pas dans wall_list). Si le blob se cogne contre un mur, il change également de direction.


### Quelles formules utilisez-vous exactement pour l’épée ? Comment passez-vous des coordonnées écran aux coordonnées monde ?

* Nous crééons un le vecteur qui part du joueur jusqu'à la souris en utilisant la fonction unproject(). Ensuite nous normalisons ce vecteur (avec vec.normalise()), et à l'aide de formules trigonométriques adaptons l'orientation de l'épée.

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

* L'arc fonctionne exactement de la même manière que l'épée (On utilise le même vecteur et les mêmes formules). Les flèches adaptent leur vitesse au vecteur qui les constitue. Par exemple, plus la flèche est à son apogée plus elle est lente (Principe de ballistique basique). On appelle arrows.update() et la fonction on_update afin que leur vitesse et direction s'actualise à chaque frame.

### Quelles formules utilisez-vous exactement pour le déplacement des chauves-souris (champ d’action, changements de direction, etc.) ?

* On définit d'abord une zone de déplacement pour les chauves-souris, délimitée par une sorte de rectangle invisible. Elles peuvent se déplacer librement à l'intérieur de cette zone. Leur mouvement est ensuite modifié à l’aide de fonctions mathématiques fournies par la bibliothèque Arcade, ce qui permet d’ajouter un effet de distorsion ou de rendre leur trajectoire plus organique.

* Lorsqu’une chauve-souris atteint les bords de cette zone, elle est repositionnée aléatoirement à l’intérieur de la limite, avec une nouvelle direction également choisie de façon aléatoire. On recalcule alors sa vitesse sur les axes X et Y en fonction de cet angle aléatoire. Ce processus se répète chaque fois qu’elle entre en contact avec un des "murs" invisibles de sa zone de déplacement.

### Comment avez-vous structuré votre programme pour que les flèches puissent poursuivre leur vol ?

* Chaque nouveau tir crée une nouvelle flèche, indépendante du joueur, et des autres flèches. Elles pourront donc toutes avoir un mouvement et une direction différente.

### Comment gérez-vous le fait que vous avez maintenant deux types de monstres, et deux types d’armes ? Comment faites-vous pour ne pas dupliquer du code entre ceux-ci ?

* Nous avons créé une surclasse Monster pour les blobs et les chauve-souris, qui implémente leur mouvement simple, et leur mort. Pour les armes, une classe parente paraissait inutile, car seul de petits détails sont communs à l'arc et l'épée.

### Quel algorithme utilisez-vous pour identifier tous les blocs d’une plateformes, et leurs limites de déplacement ?



* Notre algorithme débute en stockant dans un ensemble (set) les positions de tous les blocs présents sur la carte. Ensuite, il définit ce qui constitue une plateforme en regroupant les blocs adjacents pour former des îles, c’est-à-dire des ensembles connexes de blocs. Pour identifier ces îles, l’algorithme adopte une approche similaire à une recherche en profondeur (DFS, Depth-First Search). Il parcourt chaque coordonnée de l’ensemble et, pour chaque bloc, il vérifie les voisins situés à gauche, à droite, au-dessus et en dessous afin de déterminer s’ils appartiennent à la même plateforme. Si un voisin est identifié comme faisant partie de la plateforme et qu’il n’a pas encore été visité, il est ajouté à la liste des blocs formant l’île et devient le point de départ pour une exploration en profondeur. Cette exploration continue jusqu’à ce que tous les blocs connectés soient découverts. Ainsi, chaque appel de DFS génère un ensemble complet de positions décrivant une île unique. En répétant cette procédure pour toutes les coordonnées du set, l’algorithme parvient à identifier l’intégralité des îles (ou plateformes) formées par les différents blocs de la carte.


### Sur quelle structure travaille cet algorithme ? Quels sont les avantages et inconvénients de votre choix ?



* Il repose sur l’itération des positions des blocs lors de la lecture de la carte. Le DFS (Depth-First Search) est utilisé pour explorer et créer un arbre reliant les différents blocs et leurs voisins. Cet arbre est ensuite parcouru pour vérifier si la définition de la plateforme est respectée. Le principal avantage de cette approche est sa simplicité d’implémentation : l’algorithme est clair et direct. De plus, il s’avère particulièrement efficace pour identifier et regrouper les cellules (les voisins du graphe) en plateformes complètes. Toutefois, la recherche en profondeur (qui constitue la base de l’algorithme) peut devenir un peu lente lorsque le nombre de blocs augmente considérablement, et elle n’est pas toujours optimale en termes de performance pure.

### Quelle bibliothèque utilisez-vous pour lire les instructions des interrupteurs ? Dites en une ou deux phrases pourquoi vous avez choisi celle-là.

* Nous utilisons PyYAML car elle semblait être la plus populaire, et aussi la plus téléchargée. Dans la confiance que nous apportons à la communauté de programmeurs, cela nous a suffit.

### Comment votre design général évolue-t-il pour tenir compte des interrupteurs et des portails ?

* L'implémentation du YAML dans notre programme n'a rien changé de particulier. Elle nous a cependant permis d'implémenter facilement les portails de téléportation (ajout personnel). 
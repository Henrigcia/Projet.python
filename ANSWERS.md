Le code qui gère la lave ressemble-t-il plus à celui de l’herbe, des pièces, ou des blobs ? Expliquez votre réponse.

Stephan:

Comme la lave est quelque chose de immobile qui n'a pas de mouvement particuliers, son design est très proche des pieces. Car les deux n'ont pas de collision potentielle avec le joeur hormis lorsqu'il saute et donc meurt ou ramasse une piece. De plus les deux emettent un son lorsqu'on passe dessus.

Comment détectez-vous les conditions dans lesquelles les blobs doivent changer de direction ?

Stephan:

Premierement il a fallu creer un fichier a part contenant les differentes sous-classe de monster. Dedans il y a le mouvement des blobs. Tout d'abord dans la classe parent de blob il y le mouvement par defaut, ensuite on check si le blob est toujours sur un bloc si c'est le cas on change sa direction et sa vitesse en oppose et sinon on lui pose des boundaries sur le bloc ou il est ou et on refait la meme logique. Comme ceux-ci ne se deplacent que a gauche ou a droite il faut checker pour x >0 donc droite et x <0 donc gauche. Ainsi il est limite sur son bloc.

Comment transférez-vous le score de la joueuse d’un niveau à l’autre ?

Stephan:

On initialise une variable scrore a 0 qui compte le nombre de pieces ramassees et qui le stock. Cette variable evolue de +1 a chaque nouvelle piece et pour la garder sans la renitialiser on l'a rappelee a chaque nouvelle map chargee sans la renitialiser dans sa boucle ou on check la collision de la piece et du joueur.

Où le remettez-vous à zéro ? Avez-vous du code dupliqué entre les cas où la joueuse perd parce qu’elle a touché un ou monstre ou de la lave ?

Stephan:

On la remet a zero uniquement lorsque le joueur meurt sur le niveau en queston. On le fait dans load_map.

Comment modélisez-vous la “next-map” ? Où la stockez-vous, et comment la traitez-vous quand la joueuse atteint le point E ?

Stephan:

C'est une variable str qu'on ecrit avec des "" dans la map en question. On split en deux la ligne pour savoir si c'est bien ecrit "next-map" avec son prochain nom et lorsque on check la collision avec le panneau on appelle la fonction load_level mais sur la variable next-map.

Que se passe-t-il si la joueuse atteint le E mais la carte n’a pas de next-map ?

Stephan:

A ce niveau-la une erreur se declanche car la il n'y pas de next-map dans le fichier et le jeu se ferme avec un message d'erreur.

Quelles formules utilisez-vous exactement pour le déplacement des chauves-souris (champ d’action, changements de direction, etc.) ?

Stephan:

On leur cree un mouvement par defaut des monstres et ensuite on leur cree un champ d'action autour duquel ils peuvent naviguer. On distort leur mouvement avec les fonctions mathematiques de Arcade. On leur cree un sorte de rectangle autour et des qu'elles touchent la "limite" on leur randomise la direction avec un angle dans laquelle elles partent. On recalcule les vitesses dans les deux directions et on fait ce processus a chque fois que une chauve souris touche un "mur" invisible.

Quel algorithme utilisez-vous pour identifier tous les blocs d’une plateformes, et leurs limites de déplacement ?

Stephan:

Notre algorithme prend un set des positions des blocs qui apparaissent la map et les stock. En lui definissant ce que constitue une platforme il va creer des iles de blocs en les rassemblant. Ensuite notre algo' regarde les blocs a gauche et a droite et au dessus et dessous et les place dans une liste avec les voisins de ceux-ci, ces voisins peuvent etre des condidats potentiels pour creer l'ile (platformes). De plus l'algo check si on a deja visite la cellule constituee de blocs. Si le voisin n'a pas deja ete visite et fait partie de la platforme on le rajoute dans la liste des blocs qui font la platforme. On itere sur toutes les coordonnees dans le set. En faisant tout ca il cree alors un set qui retourne les positions cette fois-ci des blocs qui constituent la platforme. Ainsi on obtient donc grace a cet algorithe toutes les positions des "iles" (platformes) que forment les differents blocs.  

Sur quelle structure travaille cet algorithme ? Quels sont les avantages et inconvénients de votre choix ?

Stephan:

Il repose sur le fait de iterer sur les positions des blocs a travers la lecture de la carte. Sur ce qu'on appelle DFS. Il a l'avantage...
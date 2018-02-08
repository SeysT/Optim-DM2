Autheur: Thibaut Seys
Date: 08/02/2018
Lien github: https://github.com/SeysT/Optim-DM2

# Optimisation - Devoir-Maison 2 : Exposition au musée

## Organisation et utilisation du code source

L'implémentation de la CLI se trouve dans le fichier `museum_solver.py`. Ce fichier attend deux arguments obligatoires et un optionnel. Le premier est le chemin vers le fichier de données, le deuxième le type de solveur à utiliser et le troisième, optionnel, le fichier solution à partir duquel effectuer une recherche local. Voici quelques examples d'utilisation :
```sh
python museum_solver.py Data/input_1.txt linear
python museum_solver.py Data/input_1.txt local
python museum_solver.py Data/input_9.txt linear
python museum_solver.py Data/input_9.txt local
python museum_solver.py Data/input_9.txt local Data/linear_output_9.txt
```

## 1ère tentative de résolution : programmation linéaire à variables entières

La modélisation et la résolution du problème par la programmation linéaire se situent dans le fichier `linear_museum_solver.py`. Pour modéliser un programme linéaire, nous allons avoir besoin de définir les variables du problèmes, les contraintes et la fonction objectif.

### Modélisation des variables

Pour modéliser les variables, nous allons avoir besoin de discrétiser notre grille. Sur chacune des positions ainsi obtenues nous allons définir autant de variables booléennes que nous avons de type de caméras, dans nos différents exemples 2. La variable vaudra 1 si l'on pose une caméra de ce type et 0 sinon.

### Modélisation des contraintes

L'idée pour modéliser les contraintes est de regarder la position de chaque oeuvre d'art. Pour chacune de ces positions et pour chaque type de caméra on va regarder les positions de la grille qui appartiennent au disque ayant pour centre la position de l'oeuvre d'art choisie et pour rayon celui du type de caméra choisi.

**Note** : Pour optimiser l'établissement des contraintes, on ne va pas rechercher sur toutes les positions de la grille mais sur les positions dans le carré ayant pour centre la position de l'oeuvre d'art choisie et ayant pour côté le double du rayon de la caméra choisie.

### La fonction objectif

Notre fonction objectif est le coût total des caméras que nous allons chercher à minimiser. Il s'agit de la somme des variables booléennes définies ci-dessus pondérées par le prix du type de caméra qu'elle représente.

### Résultats

Les résultats présentés ici ont été obtenues à partir du fichier d'entrées **Data/input_9.txt** fournis par l'énoncé. Nous avons utilisé la commande suivante pour générer les résultats :
```sh
$ python museum_solver.py Data/input_9.txt linear
```
Les résultats obtenus sont présents dans les fichiers **Data/linear_output_9.png** et **Data/linear_output_9.txt**. Le coût total obtenu est de 2680 et la cartographie de la solution est présentée ci-après :

![linear_output_9](https://raw.githubusercontent.com/SeysT/Optim-DM2/master/Data/linear_output_9.png)

## 2ème tentative de résolution : recherche local

La modélisation et la résolution du problème par recherche local se situent dans le fichier `local_museum_solver.py`. Pour modéliser le problème sous forme de recherche local, nous allons avoir besoin de partir d'une solution existante, de définir le voisinage de cette solution et la fonction objectif permettant de comparer deux solutions voisines.

### Trouver une solution existante

Dans notre implémentation nous avons deux choix différents comme départ d'une solution : soit nous donnons une solution déjà existant et la recherche local intervient comme un post-traitement, soit nous partons de la solution extrêment simple d'une caméra de rayon minimal par oeuvre (solution implémentée).

**Note** : Pour partir d'une solution un peu plus élaborée, on pourrait utiliser une autre méthode. A chaque itération on choisit une position d'une oeuvre parmi celles restantes. On ajoute à cette position une caméra d'un type aléatoire parmi celles disponibles. On retire ensuite de la liste des oeuvres restantes toutes celles présentes dans le rayon de la nouvelle caméra.

### Fonction objectif

La fonction objectif nous permettant de comparer deux solutions différentes sera la même que celle utilisée pour la programmation linéaire. On va additionner le prix de chaque caméra retenue dans la solution.

### Voisinage d'une solution

**Version naïve** (solution implémentée) : pour explorer le voisinage d'une solution on va rajouter une caméra de manière aléatoire : on choisit aléatoirement un type de caméra parmi ceux existants et une position sur la grille. On ajoute une caméra à cette position et on supprime les caméras alentours qui ne participent pas à la couverture des oeuvres d'art. Pour cela on liste l'ensemble des oeuvres couvertes par la caméra que l'on souhaite ajouter. On liste ensuite les autres caméras concurrentes, c'est-à-dire les caméras qui intersectionnent la caméra que l'on souhaite ajouter. On regarde la liste des oeuvres impactées, c'est-à-dire celles couvertes par les caméras concurrentes. On va ensuite ajouter à la liste des oeuvres couvertes par la nouvelle caméra les oeuvres couvertes par chacune des caméras concurrentes tant que cette liste est différente des oeuvres impactées. On supprime ensuite de la solution les caméras concurrentes restantes.

**Idées d'améliorations** (non testées et implémentées) :
- Au lieu d'ajouter des oeuvres aléatoirement sur toutes les positions de la grille, on pourrait seulement regarder les positions assez proches des oeuvres d'art.
- Lors de la suppression des caméras proches de la nouvelle caméra ajoutée, on peut ne pas supprimer les caméras qui surveillent une liste d'oeuvres incluse dans la liste des oeuvres couvertes par la nouvelle caméra.

### Tentative d'implémentation et résultats

L'implémentation se trouvant dans le fichier `local_museum_solver.py` implémente la version naïve pour la recherche d'une solution voisine de la solution existante. Cette implémentation n'est pas très efficace puisqu'elle ne permet pas d'améliorer la solution trouvée par programmation linéaire et lorsqu'on utilise la solution triviale comme solution de départ, la résolution est lente. Voici les résulats obtenus pour un essai de résolution lors du lancement de cette commande :
```sh
$ python museum_solver.py Data/input_9.txt local
```
Le coût total obtenu est de 4968 et la cartographie de la solution est présentée ci-après :

![local_output_9](https://raw.githubusercontent.com/SeysT/Optim-DM2/master/Data/local_output_9.png)

## Liste des fichiers utilisés

- **museum_solver.py** : implémentation de la CLI permettant d'appeler les autres solvers
- **linear_museum_solver.py** : implémentation de la modélisation et la résolution du problème par programmation linéaire
- **local_museum_solver.py** : implémentation de la modélisation et la résolution du problème par recherche local
- **utils.py** : fonctions permettant la résolution du problème
- **Data/input_1.txt** : première liste d'oeuvres d'art simple de l'énoncé (5 oeuvres)
- **Data/linear_output_1.txt** : résultat formaté comme attendu par l'énoncé obtenu en appliquant la programmation linéaire à l'input 1
- **Data/linear_output_1.png** : cartographie obtenue en appliquant la programmation linéaire à l'input 1
- **Data/linear_output_1.txt** : résultat formaté comme attendu par l'énoncé obtenu en appliquant la recherche locale à l'input 1
- **Data/linear_output_1.png** : cartographie obtenue en appliquant la recherche locale à l'input 1
- **Data/input_9.txt** : seconde liste d'oeuvres d'art complexe de l'énoncé (5000 oeuvres)
- **Data/linear_output_9.txt** : résultat formaté comme attendu par l'énoncé obtenu en appliquant la programmation linéaire à l'input 9
- **Data/linear_output_9.png** : cartographie obtenue en appliquant la programmation linéaire à l'input 9
- **Data/linear_output_9.txt** : résultat formaté comme attendu par l'énoncé obtenu en appliquant la recherche locale à l'input 9
- **Data/linear_output_9.png** : cartographie obtenue en appliquant la recherche locale à l'input 9

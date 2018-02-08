Autheur: Thibaut Seys
Date: 07/02/2018
Lien github: https://github.com/SeysT/Optim-DM2

# Optimisation - Devoir-Maison 2 : Exposition au musée

## Organisation et utilisation du code source

L'implémentation de la CLI se trouve dans le fichier `museum_solver.py`. Ce fichier attend deux arguments obligatoires. Le premier est le chemin vers le fichier de données, le second le type de solveur à utiliser. Voici quelques examples d'utilisation :

```sh
python museum_solver.py Data/input_1.txt linear
python museum_solver.py Data/input_1.txt local
python museum_solver.py Data/input_9.txt linear
python museum_solver.py Data/input_9.txt local
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

La modélisation et la résolution du problème par recherche local se situent dans le fichier `local_museum_solver.py`.

## Liste des fichiers utilisés

- **museum_solver.py** : implémentation de la CLI permettant d'appeler les autres solvers
- **linear_museum_solver.py** : implémentation de la modélisation et la résolution du problème par programmation linéaire
- **local_museum_solver.py** : implémentation de la modélisation et la résolution du problème par recherche local
- **utils.py** : fonctions permettant la résolution du problème
- **Data/input_1.txt** : première liste d'oeuvres d'art simple de l'énoncé (5 oeuvres)
- **Data/linear_output_1.txt** : résultat formaté comme attendu par l'énoncé obtenu en appliquant la programmation linéaire à l'input 1
- **Data/linear_output_1.png** : cartographie obtenue en appliquant la programmation linéaire à l'input 1
- **Data/input_9.txt** : seconde liste d'oeuvres d'art complexe de l'énoncé (5000 oeuvres)
- **Data/linear_output_9.txt** : résultat formaté comme attendu par l'énoncé obtenu en appliquant la programmation linéaire à l'input 9
- **Data/linear_output_9.png** : cartographie obtenue en appliquant la programmation linéaire à l'input 9

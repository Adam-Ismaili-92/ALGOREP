# Algorep

## Auteurs
* Mathéo DUCROT
* Adam ISMAILI
* Matthias JACQUEMONT
* Justin JAECKER
* Louis RIBAULT

## Description
Le but de ce projet est de développer un système d'édition de texte collaboratif, similaire à des applications telles qu'Etherpad, Gobby ou Google Docs. L'objectif principal est de permettre à plusieurs utilisateurs de modifier un document de manière simultanée et cohérente.

### Technologies et Outils
Le projet est développé en Python, en utilisant la bibliothèque `mpi4py` pour la gestion de la communication parallèle et la coordination entre les différents serveurs.

## Dépendances
Ce projet nécessite Python et MPI. Assurez-vous que ces deux sont installés sur votre système. Les dépendances Python requises sont listées dans `requirements.txt`.

## Installation des Dépendances Python
Pour installer les dépendances Python, exécutez la commande suivante dans le répertoire du projet :

## Essai de Raft
On a ici un essai de raft dans le fichier Essai_RAFT.py, n'ayant pas pu le faire marcher nous n'avons pas pris
cette méthode mais nous tenions à la mettre dans le rendu afin de montrer que le travail a été essayé.

```shell
make install
```

## Utilisation
Pour lancer le script, utilisez la commande suivante :

```shell
make
```

Cette commande installera les dependances et lancera le script `main.py` qui permettra de choisir le nombre de prcessus et de lancer le 
script `algorep.py` en 
utilisant MPI 
avec le nombre de 
processus choisis.


## Commandes REPL
Nos commandes REPL ont la syntaxe suivantes :

```py
SPEED LOW/MEDIUM/HIGH (server_id)
```

```py
CRASH (server_id)
```

```py
START
```

```py
LOG (server_id)
```


## Commandes Fichier
Nos commandes pour changer le fichier sont les suivantes:

```py
MOVE (delta value)
This changes the cursus value by delta
```

```py
INSERT (text)
This will be inserted at the delta value)
```

```py
DELETE (number of characters to delete)
This will delete a certain number of characters where the cursus is currently places
```


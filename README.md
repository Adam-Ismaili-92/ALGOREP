# Algorep

## Autheurs
Matheo DUCROT

Adam ISMAILI

Matthias JACQUEMONT

Justin JAECKER

Louis RIBAULT

## Description
Le but de ce projet est de développer un système d'édition de texte collaboratif, similaire à des applications telles qu'Etherpad, Gobby ou Google Docs. L'objectif principal est de permettre à plusieurs utilisateurs de modifier un document de manière simultanée et cohérente.

### Technologies et Outils
Le projet est développé en Python, en utilisant la bibliothèque `mpi4py` pour la gestion de la communication parallèle et la coordination entre les différents serveurs.

## Dépendances
Ce projet nécessite Python et MPI. Assurez-vous que ces deux sont installés sur votre système. Les dépendances Python requises sont listées dans `requirements.txt`.

## Installation des Dépendances Python
Pour installer les dépendances Python, exécutez la commande suivante dans le répertoire du projet :

```shell
make install
```

## Utilisation
Pour lancer le script avec MPI, utilisez la commande suivante :

```shell
make
```

Cette commande lancera le script `algorep.py` en utilisant MPI avec le nombre de processus défini dans le Makefile.

## Nettoyage
Pour nettoyer les fichiers temporaires générés lors de l'exécution, exécutez :

```shell
make clean
```

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

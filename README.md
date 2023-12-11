# Algorep

## Description
### Système d'Édition de Texte Collaboratif
Le but de ce projet est de développer un système d'édition de texte collaboratif, similaire à des applications telles qu'Etherpad, Gobby ou Google Docs. L'objectif principal est de permettre à plusieurs utilisateurs de modifier un document de manière simultanée et cohérente.

Fonctionnement Général

Les clients interagissent avec le système en envoyant des commandes aux serveurs. Ces commandes peuvent être des actions d'édition telles que "avancer le curseur", "insérer un caractère", etc. Les serveurs, ensuite, se coordonnent pour s'accorder sur l'ordre d'exécution de ces commandes. Cette étape est cruciale pour assurer la cohérence du document entre tous les utilisateurs.

Réplication et Cohérence

Une fois un accord atteint, les serveurs inscrivent les commandes dans un fichier de log. Ensuite, ils exécutent ces commandes pour modifier le document. Ce processus garantit que chaque serveur, à l'issue de l'exécution, détienne une copie identique du fichier de log et donc du texte résultant. Il s'agit d'une forme de réplication de logs et de fichiers, assurant l'intégrité et la cohérence du document collaboratif.

Objectif du Projet

Ce projet vise à explorer et à mettre en œuvre des mécanismes de synchronisation et de réplication en temps réel dans un environnement distribué. L'accent est mis sur la fiabilité, la performance et la scalabilité, pour offrir une expérience utilisateur fluide et cohérente.

### Technologies et Outils
Le projet est développé en Python, en utilisant la bibliothèque `mpi4py` pour la gestion de la communication parallèle et la coordination entre les différents serveurs.

## Dépendances
Ce projet nécessite Python et MPI. Assurez-vous que ces deux sont installés sur votre système. Les dépendances Python requises sont listées dans `requirements.txt`.

### Installation des Dépendances Python
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

# Makefile pour exécuter algorep.py avec MPI

# Nombre de processus à utiliser
NPROCS = 4

# Commande MPI
MPIEXEC = mpiexec

# Script Python à exécuter
SCRIPT = algorep.py

all: run

# Règle pour exécuter le script
run:
	@$(MPIEXEC) -n $(NPROCS) python $(SCRIPT)

# Règle pour installer les dépendances Python
install:
	@pip install -r requirements.txt

# Règle pour nettoyer les fichiers temporaires
clean:
	@echo "Nettoyage des fichiers temporaires (s'il y en a)"

.PHONY: run install clean

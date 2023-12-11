# Makefile pour exécuter algorep.py avec MPI

# Nombre de processus à utiliser
NPROCS = 4

# Commande MPI
MPIEXEC = mpiexec

# Script Python à exécuter
SCRIPT = src/main.py

all: run

# Règle pour exécuter le script
run:
	@python3 $(SCRIPT)

# Règle pour installer les dépendances Python
install:
	@pip install -r requirements.txt

.PHONY: run install

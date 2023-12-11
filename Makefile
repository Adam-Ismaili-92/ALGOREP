# Makefile pour exécuter algorep.py avec MPI

# Script Python à exécuter
SCRIPT = src/main.py

all: install run

# Règle pour exécuter le script
run:
	@python3 $(SCRIPT)

# Règle pour installer les dépendances Python
install:
	@pip install -r requirements.txt

.PHONY: run install

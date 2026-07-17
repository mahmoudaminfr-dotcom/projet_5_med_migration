FROM python:3.11-slim

WORKDIR /app

# Copie et installation des dépendances dans le conteneur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie de tout le code du projet
COPY . .

# Lancement 100% automatique du pipeline complet (Migration -> Indexation -> Vérification -> Tests)
CMD ["sh", "-c", "python scripts/create_indexes.py && python scripts/verify_migration.py && python test_migration.py"]
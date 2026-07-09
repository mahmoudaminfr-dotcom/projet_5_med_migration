# 1. Utiliser une image de base Python légère
FROM python:3.11-slim

# 2. Définir le dossier de travail à l'intérieur du conteneur
WORKDIR /app

# 3. Copier le fichier des dépendances
COPY requirements.txt .

# 4. Installer les dépendances dans le conteneur
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copier les dossiers nécessaires (scripts et data) dans le conteneur
COPY scripts/ /app/scripts/
COPY data/ /app/data/

# 6. Commande lancée par défaut au démarrage du conteneur
CMD ["python", "scripts/migrate.py"]
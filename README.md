# 🏥 Projet de Migration NoSQL - Healthcare Database

Ce projet implémente un pipeline d'ingestion et de migration de données (ETL) pour structurer et transférer des données de santé depuis un fichier CSV vers une base de données MongoDB sécurisée. 

L'architecture est entièrement conteneurisée avec Docker et respecte les meilleures pratiques de sécurité industrielle (principe du moindre privilège et gestion stricte des secrets).

---

## 🛡️ Sécurité & Gestion des Privilèges

Afin de respecter les standards de sécurité, aucune information d'authentification n'est stockée en dur dans le code ou les fichiers de configuration partagés.

1. **Compte Administrateur (Root) :** Utilisé uniquement par Docker au démarrage pour l'initialisation du serveur MongoDB.
2. **Compte Applicatif (`admin_engineer`) :** Utilisé par les scripts Python. Ce compte dispose uniquement du rôle restreint `readWrite` sur la base de données `healthcare_db`, limitant ainsi la portée en cas de compromission.
3. **Fichier d'environnement (`.env`) :** Utilisé en local pour charger de manière sécurisée les identifiants en mémoire lors de l'exécution. Ce fichier est ignoré par Git.

---

## 🚀 Installation et Lancement

### 1. Prérequis
Assurez-vous d'avoir installé sur votre machine :
* [Docker & Docker Compose](https://www.docker.com/)
* [Python 3.10+](https://www.python.org/)

### 2. Configuration de l'environnement
Clonez le projet, puis créez un fichier `.env` à la racine en copiant le modèle fourni :
```bash
cp .env.example .env


Ouvrez le fichier .env nouvellement créé et définissez vos propres identifiants sécurisés :

# Identifiants du Super Administrateur (Root) - Uniquement pour l'initialisation
MONGO_INITDB_ROOT_USERNAME=votre_root_admin
MONGO_INITDB_ROOT_PASSWORD=votre_mot_de_passe_root_ultra_secret

# Identifiants de l'utilisateur applicatif restreint
MONGO_USER=admin_engineer
MONGO_PASS=votre_mot_de_passe_applicatif_securise
MONGO_HOST=mongodb
MONGO_PORT=27017

3. Démarrage de la Base de Données
Lancez le service MongoDB sécurisé en arrière-plan :

docker compose up -d mongodb

4. Exécution de la Migration (ETL)
Lancez le script de migration des données à l'intérieur du réseau Docker isolé :

docker compose run --rm migration_script

Outils d'Exploitation et Tests
Pour exécuter les scripts locaux d'exploitation ou de test, assurez-vous d'avoir installé les dépendances Python requises :

pip install -r requirements.txt

Optimisation (Création des Index)
Pour appliquer les index de performance sur la collection MongoDB :

python create_indexes.py

Vérification de la Base (Exploration)
Pour obtenir un rapport visuel rapide de la volumétrie et voir un exemple de document migré:

python verify_migration.py

Validation Qualité (Tests Automatisés)
Pour exécuter la suite de tests d'intégration et valider l'authentification, les types de données, les contraintes de champs obligatoires et l'absence de doublons :

python -m unittest test_migration.py


# 🏥 Projet de Migration NoSQL - Healthcare Database

Ce projet implémente un pipeline d'ingestion et de migration de données (ETL) entièrement automatisé. Il structure, dédoublonne et transfère des données de santé depuis un fichier CSV source vers une base de données MongoDB sécurisée.

L'architecture est 100% conteneurisée avec Docker. **Aucune installation de Python ni aucune exécution de commande Python manuelle n'est requise.**

---

## 🚀 Guide de Validation Rapide (Plug & Play)

### 1. Prérequis
Assurez-vous d'avoir démarré l'application **Docker** sur votre machine.

### 2. Configuration du fichier d'environnement (.env)

Pour des raisons de sécurité, les identifiants et mots de passe ne sont pas fournis. Vous devez créer votre propre fichier `.env` à partir du modèle.

1. À la racine du projet, dupliquez le modèle :
   ```bash
   cp .env.example .env

Ouvrez le fichier .env fraîchement créé et complétez les champs vides avec vos propres valeurs :

MONGO_INITDB_ROOT_PASSWORD : Définissez le mot de passe de votre choix pour le compte Root de la base.

MONGO_PASS : Définissez le mot de passe de votre choix pour l'utilisateur applicatif restreint (admin_engineer).

(Note : Les variables MONGO_INITDB_ROOT_USERNAME, MONGO_USER, MONGO_HOST et MONGO_PORT sont déjà pré-remplies dans le modèle avec les valeurs requises pour le bon fonctionnement du réseau Docker. Vous n'avez pas besoin de les modifier).

3. Lancement de l'Automatisation
Lancez l'ensemble du pipeline (initialisation de la base, sécurité, traitement et tests) avec la commande suivante dans votre terminal :

docker compose up --build

Déroulement Automatique du Pipeline (CI/CD Local)
Lorsque vous lancez cette commande, le conteneur applicatif prend le relais et exécute automatiquement un pipeline séquentiel strict. Chaque étape est conditionnée par la réussite de la précédente :

[1. Migration] ──(Succès)──> [2. Indexation] ──(Succès)──> [3. Vérification] ──(Succès)──> [4. Tests Unitaires]

Migration (scripts/migrate.py) : Connexion à MongoDB, extraction des données du fichier CSV, nettoyage des structures, conversion des types (ex: chaînes en entiers/floats), formatage au modèle cible NoSQL, dédoublonnage et injection des 54 966 documents uniques.

Indexation (scripts/create_indexes.py) : Création automatique des index stratégiques (sur le nom du patient, l'hôpital et la date d'admission) pour garantir des performances de requêtage optimales en production.

Contrôle Qualité (scripts/verify_migration.py) : Vérification immédiate de la volumétrie en base (validation du compte cible de 54 966 documents) et affichage d'un document témoin structuré directement dans vos logs de terminal.

Validation Unitaire (scripts/test_migration.py) : Exécution d'une suite complète de tests unittest (vérification des privilèges de l'utilisateur restreint, intégrité des types de données injectés, et validation de l'absence totale de doublons stricts). Le conteneur s'arrête ensuite proprement (Exit 0).

Ce qui est exécuté automatiquement :

Le conteneur MongoDB démarre et applique la configuration de sécurité Root que vous avez définie.

Le script init-mongo.js s'exécute pour créer l'utilisateur applicatif restreint (admin_engineer) avec son mot de passe personnalisé.

Le conteneur Python s'assemble, attend que la base soit prête, puis exécute la migration.

Résultat dans les logs : Vous verrez le script nettoyer les données et confirmer l'insertion de 54 966 documents uniques. Le conteneur de script s'arrête ensuite proprement (code 0).

🔍 Vérification visuelle (MongoDB Compass)
Le conteneur de la base de données reste actif pour vous permettre d'inspecter le résultat.

Ouvrez MongoDB Compass.

Connectez-vous en utilisant une chaîne de connexion (URI) construite avec le mot de passe applicatif que vous avez choisi dans votre .env :

mongodb://admin_engineer:<VOTRE_MONGO_PASS>@localhost:27017/healthcare_db?authSource=healthcare_db

Vous pourrez explorer la base healthcare_db, sa collection admissions et vérifier la bonne structure des données transférées.

Arrêt et Nettoyage
Pour éteindre les services et libérer les ressources de votre machine, faites Ctrl + C dans votre terminal, puis saisissez :

docker compose down

(Si vous souhaitez supprimer les volumes pour tester une nouvelle installation à blanc : docker compose down -v)


# Projet : Migration de Données Médicales vers MongoDB via Docker

## Contexte de la Mission
Ce projet s'inscrit dans le cadre de la modernisation de l'infrastructure de données d'un client du secteur médical confronté à des limites de scalabilité avec ses bases de données relationnelles traditionnelles. Nous automatisons ici le processus d'ingestion, d'audit de qualité, de nettoyage et de restructuration NoSQL orientée documents (BSON) d'un jeu de données de 55 500 enregistrements, le tout encapsulé de manière portable via Docker Compose.

---

## Schéma de la Base de Données (Modélisation NoSQL)
Plutôt qu'un modèle SQL plat ou multi-tables nécessitant des jointures lourdes, nous avons opté pour un modèle **Document Imbriqué (Embedded JSON)** au sein d'une collection unique nommée `admissions`. Ce choix garantit des performances de lecture optimales pour les applications cliniques.

### Structure d'un Document Type :
```json
{
  "_id": "ObjectId",
  "patient_info": {
    "name": "String",
    "age": "Int64",
    "gender": "String",
    "blood_type": "String"
  },
  "stay_info": {
    "hospital": "String",
    "room_number": "Int64",
    "admission_type": "String",
    "date_of_admission": "ISODate",
    "discharge_date": "ISODate"
  },
  "medical_info": {
    "doctor": "String",
    "medical_condition": "String",
    "medication": "String",
    "test_results": "String"
  },
  "billing_info": {
    "insurance_provider": "String",
    "billing_amount": "Double / Float"
  }
}

## 🚀 Comment lancer l'application en local

Suivez ces étapes pour configurer et exécuter la migration des données de santé sur votre machine.

### Prérequis
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et démarré.
* [MongoDB Compass](https://www.mongodb.com/products/tools/compass) (optionnel, pour visualiser les données).

---

### 🛠️ Guide de démarrage rapide (3 étapes)

#### 1. Configuration de l'environnement
Le projet utilise des variables d'environnement pour sécuriser les identifiants d'accès. 
Dupliquez le fichier d'exemple et renommez-le en `.env` :

cp .env.example .env

2. Lancement de la base de données MongoDB
Démarrez le service de base de données en arrière-plan :

docker compose up -d mongodb
Note : Attendez quelques secondes que le conteneur soit totalement initialisé.

3. Exécution du script de migration (ETL)
Lancez le conteneur éphémère contenant le script Python pour exécuter le nettoyage et la migration des données :

docker compose run --rm migration_script
Une fois l'exécution terminée avec succès, le conteneur du script s'arrêtera automatiquement (Exited 0) pour libérer les ressources de votre machine, tandis que la base MongoDB restera active pour vos consultations.

📊 Vérification des données
Ouvrez MongoDB Compass.

Connectez-vous en utilisant l'URI configurée dans votre fichier .env (par défaut : mongodb://admin_engineer:SecureMedPassword2026@localhost:27017/).

Vous constaterez que la collection admissions de la base healthcare_db contient exactement 54 966 documents structurés et indexés.

🧹 Arrêt et nettoyage
Pour éteindre la base de données et nettoyer les ressources Docker de votre PC :

docker compose down

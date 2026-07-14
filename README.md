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
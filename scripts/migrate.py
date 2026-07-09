import pandas as pd
from pymongo import MongoClient
from datetime import datetime

def migrer_donnees():
    # Connexion à MongoDB
    print(" Connexion à la base de données MongoDB à l'intérieur du réseau Docker...")
    client = MongoClient("mongodb://mongodb:27017/")
    
    db = client["healthcare_db"]
    collection = db["admissions"]
    
    # Nettoyage de sécurité
    collection.delete_many({})
    
    # Lecture du fichier CSV
    print(" Lecture du fichier CSV source...")
    chemin_csv = "data/healthcare_dataset.csv"
    df = pd.read_csv(chemin_csv)
    
    # Nettoyage : Suppression des doublons
    print(f" Suppression des doublons stricts (Volumétrie initiale : {len(df)} lignes)...")
    df = df.drop_duplicates()
    print(f" Après nettoyage : {len(df)} lignes prêtes à être migrées.")
    
    # Transformation et Structuration NoSQL
    print(" Structuration des données et conversion des types...")
    liste_documents = []
    
    for idx, row in df.iterrows():
        date_adm = datetime.strptime(row["Date of Admission"], "%Y-%m-%d")
        date_dis = datetime.strptime(row["Discharge Date"], "%Y-%m-%d")
        
        document = {
            "patient_info": {
                "name": str(row["Name"]),
                "age": int(row["Age"]),
                "gender": str(row["Gender"]),
                "blood_type": str(row["Blood Type"])
            },
            "stay_info": {
                "hospital": str(row["Hospital"]),
                "room_number": int(row["Room Number"]),
                "admission_type": str(row["Admission Type"]),
                "date_of_admission": date_adm,
                "discharge_date": date_dis
            },
            "medical_info": {
                "doctor": str(row["Doctor"]),
                "medical_condition": str(row["Medical Condition"]),
                "medication": str(row["Medication"]),
                "test_results": str(row["Test Results"])
            },
            "billing_info": {
                "insurance_provider": str(row["Insurance Provider"]),
                "billing_amount": float(row["Billing Amount"])
            }
        }
        liste_documents.append(document)
        
    # Insertion en masse
    print(f" Insertion de {len(liste_documents)} documents dans MongoDB...")
    resultat = collection.insert_many(liste_documents)
    
    print("\n==================================================")
    print("✅ MIGRATION RÉUSSIE DEPUIS DOCKER !")
    print(f"• Nombre de documents insérés : {len(resultat.inserted_ids)}")
    print("==================================================")
    
    client.close()

if __name__ == "__main__":
    migrer_donnees()
import os
import sys
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

def migrer_donnees():
    print("🔌 Connexion sécurisée à la base de données MongoDB (Réseau Docker)...")
    
    mongo_user = os.getenv("MONGO_USER", "admin_engineer")
    mongo_pass = os.getenv("MONGO_PASS")
    mongo_host = os.getenv("MONGO_HOST", "mongodb")
    mongo_port = int(os.getenv("MONGO_PORT", 27017))
    
    if not mongo_pass:
        print("❌ ERREUR : La variable MONGO_PASS n'est pas définie.")
        sys.exit(1)
        
    mongo_uri = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/?authSource=healthcare_db"
    
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        db = client["healthcare_db"]
        collection = db["admissions"]
        
        print("🧹 Nettoyage de la collection existante...")
        collection.delete_many({})
        
        chemin_csv = "/app/data/healthcare_dataset.csv"
        if not os.path.exists(chemin_csv):
            chemin_csv = "data/healthcare_dataset.csv"
            
        print(f"📖 Lecture du fichier source : {chemin_csv}")
        df = pd.read_csv(chemin_csv)
        
        # =========================================================================
        # 🔥 LE FIX : DÉDOUBLONNAGE STRICT (Toutes les colonnes doivent matcher)
        # =========================================================================
        taille_origine = len(df)
        
        # Sans l'argument 'subset', pandas compare l'intégralité de la ligne
        df = df.drop_duplicates(keep="first")
        
        taille_nettoyee = len(df)
        lignes_supprimees = taille_origine - taille_nettoyee
        print(f"✨ Dédoublonnage strict terminé : {lignes_supprimees} lignes 100% identiques ont été supprimées.")
        print(f"📊 Nombre de documents uniques réels insérés : {taille_nettoyee}")
        # =========================================================================

        documents = []
        print("🏗️ Structuration des données au format cible NoSQL...")
        
        for _, row in df.iterrows():
            date_admission = datetime.strptime(row["Date of Admission"], "%Y-%m-%d")
            
            doc = {
                "patient_info": {
                    "name": str(row["Name"]),
                    "age": int(row["Age"]),
                    "gender": str(row["Gender"]),
                    "blood_type": str(row["Blood Type"])
                },
                "stay_info": {
                    "hospital": str(row["Hospital"]),
                    "room_number": int(row["Room Number"]),
                    "date_of_admission": date_admission
                },
                "medical_info": {
                    "medical_condition": str(row["Medical Condition"]),
                    "doctor": str(row["Doctor"]),
                    "medication": str(row["Medication"]),
                    "test_results": str(row["Test Results"])
                },
                "billing_info": {
                    "insurance_provider": str(row["Insurance Provider"]),
                    "billing_amount": float(row["Billing Amount"]),
                    "admission_type": str(row["Admission Type"])
                }
            }
            documents.append(doc)
            
        if documents:
            print(f"🚀 Insertion en masse de {len(documents)} documents uniques dans MongoDB...")
            result = collection.insert_many(documents)
            print(f"✅ Migration réussie ! {len(result.inserted_ids)} documents insérés.")
            
        client.close()
        
    except Exception as e:
        print(f"❌ Erreur critique durant la migration : {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrer_donnees()
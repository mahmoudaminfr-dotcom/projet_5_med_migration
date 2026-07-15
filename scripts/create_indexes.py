import os
import sys
from pathlib import Path
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv

# 1. Chargement sécurisé du fichier .env depuis la racine du projet
chemin_racine = Path(__file__).resolve().parent.parent
chemin_env = chemin_racine / ".env"
load_dotenv(dotenv_path=chemin_env, override=True)

def creer_index():
    print("🔌 Connexion sécurisée à la base de données MongoDB pour l'indexation...")
    
    mongo_user = os.getenv("MONGO_USER", "admin_engineer")
    mongo_pass = os.getenv("MONGO_PASS")
    
    # Résolution Windows : Utilisation stricte de l'IP IPv4 127.0.0.1 au lieu de localhost
    mongo_host = os.getenv("MONGO_HOST", "mongodb")
    if mongo_host == "mongodb":
        mongo_host = "127.0.0.1"
        
    mongo_port = int(os.getenv("MONGO_PORT", 27017))
    
    if not mongo_pass:
        print("❌ ERREUR DE SÉCURITÉ : La variable d'environnement MONGO_PASS n'est pas définie.")
        sys.exit(1)
    
    mongo_uri = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/?authSource=healthcare_db"
    
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        db = client["healthcare_db"]
        collection = db["admissions"]
        
        print("⚡ Création des index stratégiques...")
        
        # 1. Index sur le nom du patient (Recherches fréquentes)
        nom_index = collection.create_index([("patient_info.name", ASCENDING)])
        print(f"✅ Index créé sur le nom du patient : {nom_index}")
        
        # 2. Index sur l'hôpital (Filtres opérationnels)
        hospital_index = collection.create_index([("stay_info.hospital", ASCENDING)])
        print(f"✅ Index créé sur l'hôpital : {hospital_index}")
        
        # 3. Index sur la date d'admission (Tris chronologiques)
        date_index = collection.create_index([("stay_info.date_of_admission", ASCENDING)])
        print(f"✅ Index créé sur la date d'admission : {date_index}")
        
        print("\n==================================================")
        print("🏆 TOUS LES INDEX ONT ÉTÉ APPLIQUÉS AVEC SUCCÈS ! ")
        print("==================================================")
        
        print("\n📋 Liste des index actuellement actifs sur la collection :")
        for index in collection.list_indexes():
            print(f" • {index['name']} -> Champs : {list(index['key'].keys())}")
            
        client.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des index : {e}")
        sys.exit(1)

if __name__ == "__main__":
    creer_index()
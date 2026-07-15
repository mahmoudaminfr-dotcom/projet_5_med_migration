import os
import sys
import pprint
from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv

# 1. Chargement sécurisé du fichier .env
chemin_racine = Path(__file__).resolve().parent.parent
chemin_env = chemin_racine / ".env"
load_dotenv(dotenv_path=chemin_env, override=True)

def verifier_base():
    print("🔌 Connexion sécurisée à MongoDB pour contrôle qualité...")
    
    mongo_user = os.getenv("MONGO_USER", "admin_engineer")
    mongo_pass = os.getenv("MONGO_PASS")
    
    # Résolution Windows : Utilisation stricte de l'IP IPv4 127.0.0.1
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
        
        # 1. Compter les documents
        nb_documents = collection.count_documents({})
        print("\n==================================================")
        print("🔍 RAPPORT DE VÉRIFICATION DE LA BASE DE DONNÉES")
        print("==================================================")
        print(f"• Nombre total de documents migrés : {nb_documents}")
        
        if nb_documents == 54966:
            print("✅ Le compte est bon ! Aucun document n'a été perdu (54 966 uniques attendus).")
        else:
            print(f"⚠️ Écart détecté ! Attendu: 54966 | Présent en base: {nb_documents}")
            
        # 2. Récupérer et afficher un document exemple
        print("\n📝 Aperçu d'un document structuré en base :")
        print("--------------------------------------------------")
        exemple = collection.find_one()
        
        if exemple:
            pprint.pprint(exemple)
        else:
            print("❌ Aucun document trouvé dans la collection.")
            
        print("==================================================")
        client.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification : {e}")
        sys.exit(1)

if __name__ == "__main__":
    verifier_base()
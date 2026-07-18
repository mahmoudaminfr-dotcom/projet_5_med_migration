import os
import sys
import pprint
from pathlib import Path
from pymongo import MongoClient

def verifier_base():
    print("🔌 Connexion sécurisée à MongoDB pour contrôle qualité...")
    
    # Extraction des variables directement injectées par Docker
    mongo_user = os.getenv("MONGO_USER", "admin_engineer")
    mongo_pass = os.getenv("MONGO_PASS")
    mongo_host = os.getenv("MONGO_HOST", "mongodb_container") # Utilisation du service réseau Docker
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
            print(f"❌ ÉCRITIQUE : Écart détecté ! Attendu: 54966 | Présent en base: {nb_documents}")
            client.close()
            sys.exit(1) # Fait échouer le conteneur si le compte est faux
            
        # 2. Récupérer et afficher un document exemple
        print("\n📝 Aperçu d'un document structuré en base :")
        print("--------------------------------------------------")
        exemple = collection.find_one()
        
        if exemple:
            pprint.pprint(exemple)
        else:
            print("❌ ÉCRITIQUE : Aucun document trouvé dans la collection alors que le compte était bon.")
            client.close()
            sys.exit(1) # Fait échouer le conteneur si aucun document n'est lisible
            
        print("==================================================")
        client.close()
        sys.exit(0) # Tout est parfait, on quitte proprement
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification : {e}")
        sys.exit(1)

if __name__ == "__main__":
    verifier_base()
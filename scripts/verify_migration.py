from pymongo import MongoClient

def verifier_base():
    print("🔌 Connexion à MongoDB pour vérification...")
    client = MongoClient("mongodb://localhost:27017/")
    
    db = client["healthcare_db"]
    collection = db["admissions"]
    
    # 1. Compter les documents
    nb_documents = collection.count_documents({})
    print("\n==================================================")
    print("🔍 RAPPORT DE VÉRIFICATION DE LA BASE DE DONNÉES")
    print("==================================================")
    print(f"• Nombre total de documents migrés : {nb_documents}")
    
    if nb_documents == 54966:
        print("✅ Le compte est bon ! Aucun document n'a été perdu.")
    else:
        print("⚠️ Écart détecté sur le nombre de lignes attendu.")
        
    # 2. Récupérer et afficher un document exemple
    print("\n📝 Aperçu d'un document structuré en base :")
    print("--------------------------------------------------")
    exemple = collection.find_one()
    
    if exemple:
        import pprint
        pprint.pprint(exemple)
    else:
        print("❌ Aucun document trouvé dans la collection.")
        
    print("==================================================")
    client.close()

if __name__ == "__main__":
    verifier_base()
from pymongo import MongoClient, ASCENDING

def creer_index():
    print("🔌 Connexion à la base de données MongoDB...")
    client = MongoClient("mongodb://localhost:27017/")
    
    db = client["healthcare_db"]
    collection = db["admissions"]
    
    print(" Création des index stratégiques...")
    
    # 1. Index sur le nom du patient (Recherches fréquentes)
    nom_index = collection.create_index([("patient_info.name", ASCENDING)])
    print(f"✅ Index créé avec succès sur le nom du patient : {nom_index}")
    
    # 2. Index sur l'hôpital (Filtres et agrégations opérationnelles)
    hospital_index = collection.create_index([("stay_info.hospital", ASCENDING)])
    print(f"✅ Index créé avec succès sur l'hôpital : {hospital_index}")
    
    # 3. Index sur la date d'admission (Tris temporels)
    date_index = collection.create_index([("stay_info.date_of_admission", ASCENDING)])
    print(f"✅ Index créé avec succès sur la date d'admission : {date_index}")
    
    print("\n==================================================")
    print("TOUS LES INDEX ONT ÉTÉ APPLIQUÉS AVEC SUCCÈS ! ")
    print("==================================================")
    
    # Affichage de la liste finale pour vérification
    print("\n Liste des index actuellement actifs sur la collection :")
    for index in collection.list_indexes():
        print(f" • {index['name']} -> Champs : {index['key'].keys()}")
        
    client.close()

if __name__ == "__main__":
    creer_index()
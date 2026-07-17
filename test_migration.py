import os
import sys
import unittest
from pathlib import Path
from pymongo import MongoClient

class TestHealthcareMigration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n⚡ Initialisation des tests de validation de données...")
        cls.mongo_user = os.getenv("MONGO_USER", "admin_engineer")
        cls.mongo_pass = os.getenv("MONGO_PASS")
        cls.mongo_host = os.getenv("MONGO_HOST", "mongodb_container") # Utilisation du service réseau Docker
        cls.mongo_port = int(os.getenv("MONGO_PORT", 27017))
        
        if not cls.mongo_pass:
            print("❌ ERREUR DE CONFIGURATION : MONGO_PASS est introuvable.")
            sys.exit(1)
            
        cls.mongo_uri = f"mongodb://{cls.mongo_user}:{cls.mongo_pass}@{cls.mongo_host}:{cls.mongo_port}/?authSource=healthcare_db"
        
        try:
            cls.client = MongoClient(cls.mongo_uri, serverSelectionTimeoutMS=3000)
            cls.db = cls.client["healthcare_db"]
            cls.collection = cls.db["admissions"]
        except Exception as e:
            print(f"❌ Impossible d'initialiser la connexion de test : {e}")
            sys.exit(1)

    @classmethod
    def tearDownClass(cls):
        cls.client.close()
        print("\n🏁 Fin des tests de validation.")

    def test_1_authentification(self):
        try:
            self.client.admin.command('ping')
            db_names = self.client.list_database_names()
            self.assertIn("healthcare_db", db_names, "L'accès à 'healthcare_db' est refusé.")
            print("✅ Test Authentification : Réussi")
        except Exception as e:
            self.fail(f"L'authentification a échoué : {e}")

    def test_2_nombre_documents(self):
        total_docs = self.collection.count_documents({})
        print(f"✅ Test Volumétrie : Réussi ({total_docs} documents en base)")

    def test_3_champs_obligatoires(self):
        echantillon = self.collection.find().limit(100)
        for doc in echantillon:
            self.assertIn("patient_info", doc)
            self.assertIn("stay_info", doc)
            self.assertIn("medical_info", doc)
            self.assertIn("billing_info", doc)
        print("✅ Test Champs Obligatoires : Réussi")

    def test_4_types_donnees(self):
        doc = self.collection.find_one()
        self.assertIsNotNone(doc)
        self.assertIsInstance(doc["patient_info"]["name"], str)
        self.assertIsInstance(doc["patient_info"]["age"], int)
        self.assertIsInstance(doc["billing_info"]["billing_amount"], float)
        print("✅ Test Types de données : Réussi")

    def test_5_absence_doublons(self):
        """Vérifie qu'il n'y a aucun doublon STRICT (ligne 100% identique) en base."""
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "name": "$patient_info.name",
                        "age": "$patient_info.age",
                        "hospital": "$stay_info.hospital",
                        "date": "$stay_info.date_of_admission",
                        "doctor": "$medical_info.doctor",
                        "amount": "$billing_info.billing_amount"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$match": {
                    "count": {"$gt": 1}
                }
            }
        ]
        doublons = list(self.collection.aggregate(pipeline))
        self.assertEqual(len(doublons), 0, f"Des doublons stricts ont été détectés en base ! : {len(doublons)}")
        print("✅ Test Absence de Doublons Stricts : Réussi")

if __name__ == "__main__":
    unittest.main()
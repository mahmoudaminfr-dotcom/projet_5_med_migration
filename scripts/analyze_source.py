import pandas as pd

def inspecter_csv():
    # Définition du chemin vers le fichier CSV
    chemin_csv = "data/healthcare_dataset.csv"
    
    print("==================================================")
    print("📊 ANALYSE DE QUALITÉ DU DATASET SOURCE (CSV) 📊")
    print("==================================================\n")
    
    # 1. Chargement du fichier avec Pandas
    print("--- 1. Chargement et Volumétrie ---")
    df = pd.read_csv(chemin_csv)
    print(f"• Nombre total de lignes (enregistrements) : {df.shape[0]}")
    print(f"• Nombre de colonnes : {df.shape[1]}\n")
    
    # 2. Inspection des colonnes et types
    print("--- 2. Structure et Types des colonnes ---")
    print(df.dtypes)
    print("\n")
    
    # 3. Détection des valeurs manquantes (vides)
    print("--- 3. Vérification des valeurs manquantes (Nulls) ---")
    valeurs_manquantes = df.isnull().sum()
    if valeurs_manquantes.sum() == 0:
        print("✅ Aucune valeur manquante détectée dans le fichier.")
    else:
        print(valeurs_manquantes[valeurs_manquantes > 0])
    print("\n")
    
    # 4. Détection des doublons
    print("--- 4. Vérification des lignes en doublon ---")
    nb_doublons = df.duplicated().sum()
    if nb_doublons == 0:
        print("✅ Aucun doublon strict détecté.")
    else:
        print(f"⚠️ Attention : {nb_doublons} ligne(s) parfaitement identique(s) détectée(s).")
    print("\n==================================================")

if __name__ == "__main__":
    inspecter_csv()
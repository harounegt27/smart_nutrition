import pandas as pd
import numpy as np
import os

def get_bmi_category(bmi):
    """Classifie le BMI en catégories cliniques."""
    if pd.isna(bmi):
        return 'Unknown'
    elif bmi < 18.5:
        return 'Underweight'
    elif bmi < 25:
        return 'Normal'
    elif bmi < 30:
        return 'Overweight'
    else:
        return 'Obese'

def calculate_health_risk(row):
    """
    Calcule un score de risque santé basé sur les indicateurs médicaux.
    Plus le score est élevé, plus le patient est à risque.
    """
    score = 0
    
    # 1. Pression Artérielle (Systolique)
    if row['Blood_Pressure_Systolic'] > 125:
        score += 1
    
    # 2. Cholestérol
    if row['Cholesterol_Level'] > 200:
        score += 1
        
    # 3. Sucre dans le sang
    if row['Blood_Sugar_Level'] > 126:
        score += 1
        
    # 4. Tabagisme
    if row['Smoking_Habit'] == 'Yes':
        score += 1
        
    # 5. Maladie Chronique
    if row['Chronic_Disease'] != 'None':
        score += 1
        
    return score

def prepare_dataset():
    # 1. Charger le Dataset
    try:
        df = pd.read_csv('data/Personalized_Diet_Recommendations.csv')
        print("Dataset chargé avec succès.")
    except FileNotFoundError:
        print("Erreur: Fichier 'Personalized_Diet_Recommendations.csv' introuvable.")
        return

    # 2. Feature Engineering 1 : Catégorie BMI
    print("--- Feature 1: BMI Categorization ---")
    df['bmi_category'] = df['BMI'].apply(get_bmi_category)
    print("Catégories BMI créées (Underweight, Normal, Overweight, Obese).")

    # 3. Feature Engineering 2 : Score de Risque Santé
    print("\n--- Feature 2: Health Risk Score ---")
    df['health_risk_score'] = df.apply(calculate_health_risk, axis=1)
    print(f"Score de risque calculé (0 à 5). Moyenne : {df['health_risk_score'].mean()}")

    # 4. Feature Engineering 3 : Équilibre Calorique
    # Différence entre ce qu'il mange et ce qu'il devrait manger
    print("\n--- Feature 3: Caloric Balance ---")
    df['caloric_balance'] = df['Caloric_Intake'] - df['Recommended_Calories']
    # Si positif = Surconsommation, Si négatif = Déficit
    print("Balance calorique calculé (Intake - Recommended).")

    # 5. Sauvegarde
    output_path = 'data/diet_data_enriched.csv'
    df.to_csv(output_path, index=False)
    print(f"\n✅ Données enrichies sauvegardées dans : {output_path}")
    
    # Aperçu
    print("\nAperçu des nouvelles colonnes :")
    print(df[['BMI', 'bmi_category', 'health_risk_score', 'Caloric_Intake', 'Recommended_Calories', 'caloric_balance']].head())
    
    return df.head()

if __name__ == "__main__":
    prepare_dataset()
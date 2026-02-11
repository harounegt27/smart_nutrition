import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")

def run_eda():
    print("Chargement des données enrichies...")
    try:
        df = pd.read_csv('data/diet_data_enriched.csv')
        print("Données chargées.")
    except FileNotFoundError:
        print("Erreur: 'diet_data_enriched.csv' introuvable. Lancez data_preparation.py d'abord.")
        return

    print(f"\n--- Aperçu Dataset ---")
    print(f"Total Lignes: {df.shape[0]}")
    print(f"Colonnes: {df.shape[1]}")

    # --- ANALYSE POUR LA CLASSIFICATION (Target: Recommended_Meal_Plan) ---

    # 1. Distribution des Types de Régimes
    print("\n--- 1. Distribution des Régimes (Target Classification) ---")
    plt.figure(figsize=(10, 5))
    order = df['Recommended_Meal_Plan'].value_counts().index
    sns.countplot(x='Recommended_Meal_Plan', data=df, order=order, palette='viridis')
    plt.title('Distribution des Types de Régimes Recommandés')
    plt.xticks(rotation=45)
    plt.savefig('data/01_diet_distribution.png', bbox_inches='tight')
    plt.show()

    # 2. Impact du BMI sur le choix du régime
    print("\n--- 2. Impact du BMI sur le Régime ---")
    plt.figure(figsize=(10, 6))
    sns.countplot(x='bmi_category', hue='Recommended_Meal_Plan', data=df, palette='magma')
    plt.title('Régime Recommandé selon la Catégorie de Poids')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig('data/02_bmi_vs_diet.png', bbox_inches='tight')
    plt.show()

    # --- ANALYSE POUR LA RÉGRESSION (Targets: Calories/Protein/etc.) ---

    # 3. Corrélation avec les Apports Recommandés
    print("\n--- 3. Matrice de Corrélation (Nutriments) ---")
    # Sélection des colonnes numériques pertinentes pour la régression
    nutrition_cols = [
        'Age', 'BMI', 'Daily_Steps', 'Sleep_Hours', 
        'Recommended_Calories', 'Recommended_Protein', 
        'Recommended_Carbs', 'Recommended_Fats'
    ]
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(df[nutrition_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Corrélation : Profil Patient vs Besoins Nutritionnels')
    plt.savefig('data/03_nutrition_correlation.png')
    plt.show()

    # 4. Distribution des Calories Recommandées
    print("\n--- 4. Distribution des Calories Recommandées ---")
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Recommended_Calories'], kde=True, color='skyblue')
    plt.title('Distribution des Besoins Caloriques')
    plt.savefig('data/04_calories_distribution.png')
    plt.show()

    # 5. Score de Risque vs Régime
    print("\n--- 5. Score de Risque vs Régime ---")
    plt.figure(figsize=(10, 5))
    sns.boxplot(x='Recommended_Meal_Plan', y='health_risk_score', data=df, palette='Set2')
    plt.title('Score de Risque Santé par Type de Régime')
    plt.xticks(rotation=45)
    plt.savefig('data/05_risk_vs_diet.png', bbox_inches='tight')
    plt.show()

    # 6. Valeurs Manquantes (Pipeline Prep)
    print("\n--- 6. Analyse des Valeurs Manquantes ---")
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
    plt.title('Carte Thermique des Valeurs Manquantes')
    plt.savefig('data/06_missing_values.png')
    plt.show()

    print("\n✅ EDA terminée. Graphiques sauvegardés dans 'data/'.")

if __name__ == "__main__":
    run_eda()
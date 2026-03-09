from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal
import pandas as pd
import numpy as np
import mlflow.sklearn
import os

from fastapi.middleware.cors import CORSMiddleware

# Imports pour le LLM
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# ==========================================================
# 1. CONFIGURATION GROQ UNIQUEMENT
# ==========================================================

MODEL_ML_PATH = "mlruns/1/models/m-c04d08fd43534034b127d6c802b765c0/artifacts/model"

# Récupération des variables
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3-8b-8192")

# Vérification de la clé API
if not API_KEY:
    raise ValueError("❌ Erreur: OPENAI_API_KEY est manquant dans le fichier .env")

# Initialisation du client pour Groq (compatible librairie OpenAI)
client_llm = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=API_KEY
)
print(f"🤖 LLM Configuré : Groq ({MODEL_NAME})")

# ==========================================================
# 2. APPLICATION FASTAPI & CHARGEMENT ML
# ==========================================================

app = FastAPI(
    title="Diet Recommendation API",
    description="Prédiction ML + Conseils IA via Groq",
    version="5.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Autorise toutes les origines (y compris localhost:5173)
    allow_credentials=True,
    allow_methods=["*"],        # Autorise toutes les méthodes (POST, GET, OPTIONS...)
    allow_headers=["*"],        # Autorise tous les headers
)

model_ml = None

@app.on_event("startup")
def load_ml_model():
    global model_ml
    try:
        if os.path.exists(MODEL_ML_PATH):
            model_ml = mlflow.sklearn.load_model(MODEL_ML_PATH)
        else:
            # Tenter le chemin alternatif
            alt_path = "mlruns/1/models/m-c04d08fd43534034b127d6c802b765c0/artifacts"
            model_ml = mlflow.sklearn.load_model(alt_path)
        print("✅ Modèle ML (Régression) chargé avec succès.")
    except Exception as e:
        print(f"❌ Erreur chargement modèle ML: {e}")

# ==========================================================
# 3. SCHÉMAS (INPUTS / OUTPUTS)
# ==========================================================

GenderEnum = Literal["Male", "Female", "Other"]
ActivityEnum = Literal["Sedentary", "Light", "Moderate", "Active", "Very Active"]
DietEnum = Literal["Regular", "Vegetarian", "Vegan", "Keto"]
YesNoEnum = Literal["Yes", "No"]

class SimpleUserInput(BaseModel):
    age: int = Field(..., example=30)
    gender: GenderEnum = Field(..., example="Male")
    height_cm: int = Field(..., example=175)
    weight_kg: int = Field(..., example=75)
    activity_level: ActivityEnum = Field(default="Moderate")
    dietary_habits: DietEnum = Field(default="Regular")
    sleep_hours: float = Field(default=7.0)
    alcohol_consumption: YesNoEnum = Field(default="No")
    smoking_habit: YesNoEnum = Field(default="No")
    has_diabetes: bool = Field(default=False)
    has_hypertension: bool = Field(default=False)
    allergies: Optional[str] = Field(default=None)

class PredictionOutput(BaseModel):
    recommended_calories: float
    recommended_protein: float
    recommended_carbs: float
    recommended_fats: float
    bmi: float
    bmi_category: str
    health_status: str
    ai_advice: str

# ==========================================================
# 4. LOGIQUE MÉTIER
# ==========================================================

def map_activity_to_steps(level: str) -> int:
    mapping = {"Sedentary": 2500, "Light": 5000, "Moderate": 8000, "Active": 12000, "Very Active": 18000}
    return mapping.get(level, 8000)

def calculate_bmi_category(bmi: float) -> str:
    if bmi < 18.5: return "Underweight"
    if bmi < 25: return "Normal"
    if bmi < 30: return "Overweight"
    return "Obese"

def prepare_full_features(input_data: SimpleUserInput) -> tuple[pd.DataFrame, float, str]:
    bmi = input_data.weight_kg / ((input_data.height_cm / 100) ** 2)
    bmi_category = calculate_bmi_category(bmi)
    daily_steps = map_activity_to_steps(input_data.activity_level)
    
    # Estimation TDEE
    bmr = 10 * input_data.weight_kg + 6.25 * input_data.height_cm - 5 * input_data.age + 5
    activity_factor = {"Sedentary": 1.2, "Light": 1.375, "Moderate": 1.55, "Active": 1.725, "Very Active": 1.9}
    estimated_tdee = bmr * activity_factor.get(input_data.activity_level, 1.55)

    data = {
        'Age': input_data.age, 'Gender': input_data.gender, 'Height_cm': input_data.height_cm,
        'Weight_kg': input_data.weight_kg, 'BMI': round(bmi, 2), 'bmi_category': bmi_category,
        'Chronic_Disease': "Diabetes" if input_data.has_diabetes else ("Hypertension" if input_data.has_hypertension else ""),
        'Blood_Pressure_Systolic': 145 if input_data.has_hypertension else 120,
        'Blood_Pressure_Diastolic': 95 if input_data.has_hypertension else 80,
        'Cholesterol_Level': 250 if input_data.has_hypertension else 190,
        'Blood_Sugar_Level': 170 if input_data.has_diabetes else 90,
        'Genetic_Risk_Factor': "No", 'Allergies': input_data.allergies if input_data.allergies else "",
        'Daily_Steps': daily_steps,
        'Exercise_Frequency': 1 if input_data.activity_level == "Sedentary" else 5,
        'Sleep_Hours': input_data.sleep_hours,
        'Alcohol_Consumption': input_data.alcohol_consumption,
        'Smoking_Habit': input_data.smoking_habit,
        'Dietary_Habits': input_data.dietary_habits,
        'Caloric_Intake': round(estimated_tdee),
        'Protein_Intake': round((estimated_tdee * 0.15) / 4),
        'Carbohydrate_Intake': round((estimated_tdee * 0.50) / 4),
        'Fat_Intake': round((estimated_tdee * 0.35) / 9),
        'Preferred_Cuisine': "Mediterranean", 'Food_Aversions': "", 'caloric_balance': 0,
        'health_risk_score': 2 if not (input_data.has_diabetes or input_data.has_hypertension) else 4
    }
    return pd.DataFrame([data]), bmi, bmi_category

# ==========================================================
# 5. LOGIQUE LLM (GROQ)
# ==========================================================

async def generate_diet_plan_llm(user_input: SimpleUserInput, macros: dict):
    prompt = f"""
        Tu es un nutritionniste clinique certifié et un coach sportif professionnel.
        Ta mission est de fournir des recommandations nutritionnelles et sportives personnalisées,
        scientifiquement cohérentes, faciles à suivre et adaptées au profil de l'utilisateur.

        ========================
        PROFIL UTILISATEUR
        ========================
        Age: {user_input.age} ans
        Sexe: {user_input.gender}
        Poids: {user_input.weight_kg} kg
        Taille: {user_input.height_cm} cm
        IMC: {macros['bmi']} ({macros['bmi_category']})

        Niveau d'activité: {user_input.activity_level}

        Conditions de santé:
        - Diabète: {"Oui" if user_input.has_diabetes else "Non"}
        - Hypertension: {"Oui" if user_input.has_hypertension else "Non"}

        Allergies ou restrictions alimentaires:
        {user_input.allergies if user_input.allergies else "Aucune"}

        ========================
        OBJECTIFS NUTRITIONNELS JOURNALIERS
        ========================
        Calories: {macros['calories']} kcal
        Protéines: {macros['protein']} g
        Glucides: {macros['carbs']} g
        Lipides: {macros['fats']} g

        ========================
        TA MISSION
        ========================

        1️⃣ Plan alimentaire journalier détaillé

        Pour chaque repas (Petit-déjeuner, Déjeuner, Dîner et Collation facultative):

        - Nom du plat
        - Quantité des aliments (grammes ou portions)
        - Calories estimées
        - Répartition approximative des macronutriments
        - Pourquoi ce repas est adapté au profil de l'utilisateur

        2️⃣ Alternatives alimentaires

        Pour chaque repas propose:
        - 2 alternatives plus simples ou équivalentes
        - adaptées aux mêmes macros

        3️⃣ Conseils nutritionnels personnalisés

        Explique:
        - Comment répartir les repas dans la journée
        - Quels aliments privilégier
        - Quels aliments limiter selon l'IMC et les conditions de santé

        4️⃣ Programme sportif adapté

        Propose un programme simple incluant:

        - type d'exercice
        - durée
        - fréquence hebdomadaire
        - intensité

        Adapte les recommandations au niveau: {user_input.activity_level}

        5️⃣ Conseils mode de vie

        Donne des conseils sur:
        - hydratation quotidienne
        - qualité du sommeil
        - gestion du stress
        - routine quotidienne saine

        ========================
        FORMAT DE SORTIE
        ========================

        Utilise des titres clairs et des listes.
        Utilise des émojis pour rendre la lecture agréable.
        Sois précis, pédagogique et structuré.
        Réponds de manière concise mais informative.
        """

    try:
        response = await client_llm.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Tu es un coach nutritionniste expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erreur lors de la génération IA (Groq): {str(e)}"

# ==========================================================
# 6. ENDPOINTS
# ==========================================================

@app.get("/", tags=["Infrastructure"])
def health_check():
    return {
        "status": "online",
        "ml_model_loaded": model_ml is not None,
        "llm_provider": "Groq",
        "llm_model": MODEL_NAME
    }

@app.get("/options", tags=["Configuration"])
def get_form_options():
    return {
        "genders": ["Male", "Female", "Other"],
        "activity_levels": ["Sedentary", "Light", "Moderate", "Active", "Very Active"],
        "dietary_habits": ["Regular", "Vegetarian", "Vegan", "Keto"],
        "yes_no": ["Yes", "No"]
    }

@app.post("/predict", response_model=PredictionOutput, tags=["Prediction"])
async def predict_diet_plan(user_input: SimpleUserInput):
    if model_ml is None:
        raise HTTPException(status_code=503, detail="Modèle ML non chargé.")

    # 1. ML Prediction
    full_df, bmi, bmi_cat = prepare_full_features(user_input)
    predictions = model_ml.predict(full_df)
    cal, prot, carbs, fats = predictions[0]
    
    status_msg = "Bonne santé générale."
    if user_input.has_diabetes: status_msg = "Diabète pris en compte."
    if user_input.has_hypertension: status_msg = "Hypertension prise en compte."

    macros_for_llm = {
        "calories": round(cal), "protein": round(prot),
        "carbs": round(carbs), "fats": round(fats),
        "bmi": round(bmi, 1), "bmi_category": bmi_cat
    }
    
    # 2. LLM Generation
    ai_response = await generate_diet_plan_llm(user_input, macros_for_llm)

    return {
        "recommended_calories": float(round(cal)),
        "recommended_protein": float(round(prot)),
        "recommended_carbs": float(round(carbs)),
        "recommended_fats": float(round(fats)),
        "bmi": round(bmi, 1),
        "bmi_category": bmi_cat,
        "health_status": status_msg,
        "ai_advice": ai_response
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
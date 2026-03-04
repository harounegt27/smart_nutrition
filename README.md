# Diet Recommendation System — End-to-End Machine Learning Application

Python • Angular • FastAPI • Docker • MLflow

University: Tek-Up — Guided ML Project (Python for Data Science 2)

Author: Mohamed Haroun Mezned

## Project Overview

This project is a production-grade End-to-End Machine Learning System that predicts:

1- The recommended diet plan for a patient (classification)

2- Daily recommended macronutrients (multi-output regression)

3- Health risk scoring + feature engineering based on medical indicators

The system integrates:

• Data preparation & automated feature engineering

• Full ML Pipeline (SMOTE, Preprocessing, Hyperparameter Tuning)

• MLflow experiment tracking

• FastAPI backend for predictions

• Frontend for interactive UI

• Docker containerization for deployment

                ┌──────────────────────────┐
                │Phase 1: Data Engineering │
                │    • Cleaning • EDA      │
                └───────────────┬──────────┘
                                ▼
                  ┌─────────────────────────┐
                  │ Phase 2: ML Pipeline    │
                  │ Preprocessing • SMOTE   │
                  │ XGBoost/RF • MLflow     │
                  └───────────────┬─────────┘
                                  ▼
                ┌────────────────────────────────┐
                │ Phase 3: Backend + Frontend    │
                │ FastAPI • Angular • Docker     │
                └────────────────────────────────┘

## Dataset
Dataset used: Personalized Medical Diet Recommendations(from Kaggle)

Link → https://www.kaggle.com/datasets/ziya07/personalized-medical-diet-recommendations-dataset

The dataset contains patients’ medical profile, lifestyle indicators, nutritional intake, allergies, and the recommended diet plan.

## Data Dictionary
| Column                   | Type        | Description                     |
| ------------------------ | ----------- | ------------------------------- |
| Age                      | Numeric     | Patient age                     |
| Gender                   | Categorical | Male/Female/Other               |
| Height_cm                | Numeric     | Height                          |
| Weight_kg                | Numeric     | Weight                          |
| BMI                      | Numeric     | Body Mass Index                 |
| Chronic_Disease          | Categorical | Hypertension, Diabetes…         |
| Blood_Pressure_Systolic  | Numeric     | Systolic pressure               |
| Blood_Pressure_Diastolic | Numeric     | Diastolic pressure              |
| Blood_Sugar_Level        | Numeric     | Glucose level                   |
| Cholesterol_Level        | Numeric     | Cholesterol                     |
| Activity_Level           | Categorical | Sedentary/Moderate/Active       |
| Diet_Type                | Categorical | Vegan/Vegetarian/Mixed          |
| Calorie_Intake           | Numeric     | Current calories consumed       |
| Protein_Intake           | Numeric     | Current protein intake          |
| Recommended_Calories     | Numeric     | Target calories                 |
| Recommended_Protein      | Numeric     | Target proteins                 |
| Recommended_Meal_Plan    | Categorical | Balanced/Low-Carb/High-Protein… |

## Data Quality
| Issue                  | Solution                           |
| ---------------------- | ---------------------------------- |
| Missing values         | SimpleImputer                      |
| Categorical encoding   | OneHotEncoder                      |
| Imbalanced labels      | SMOTE for diet plan classification |
| Synthetic distribution | Handled with robust ML models      |


## Key Features
1. Feature Engineering

    | Feature             | Description                                  |
    | ------------------- | -------------------------------------------- |
    | `bmi_category`      | Underweight / Normal / Overweight / Obese    |
    | `health_risk_score` | Score based on BP, sugar level, cholesterol… |
    | `caloric_balance`   | Intake – Recommended Calories                |


## Machine Learning Pipeline
### Models used
• RandomForestClassifier

• XGBoostClassifier

• RandomForestRegressor / MultiOutputRegressor

• XGBoostRegressor

### Pipeline Stages
• SimpleImputer

• OneHotEncoder

• Scaling

• SMOTE (only for classification)

• GridSearchCV

• MLflow experiment tracking

### Artifacts
• meal_plan_classifier.pkl

• nutrients_regressor.pkl

• MLflow logs & metrics

• Preprocessing pipeline
## Backend (FastAPI)
### Endpoints
| Method | Route               | Description                       |
| ------ | ------------------- | --------------------------------- |
| GET    | `/`                 | Health check                      |
| POST   | `/predict/mealplan` | Returns recommended diet plan     |
| POST   | `/predict/macros`   | Returns predicted macro nutrients |
| POST   | `/predict/batch`    | Batch inference                   |

### Run FastAPI
cmd :
    
    uvicorn app:app --reload --host 0.0.0.0 --port 8000

Access Swagger Docs → http://localhost:8000/docs

## Frontend (Angular)
Built with Angular 17, using:

• Angular Material

• Reactive Forms

• HttpClient for API calls

Features:

• Prediction input form

• Diet Plan prediction in real time

• Macro-nutrient visualizations (charts)

• Responsive UI (Mobile + Desktop)

• API Consumption via HttpClient / Axios

Run : 

    ng serve 
    # ou
    npm start

URL → http://localhost:4200

## Installation & Setup
1.Clone Projet:

    git clone https://github.com/harounegt27/diet_recommendation_system
    cd diet_recommendation_system

2.Backend Setup:

    python -m venv venv
    source venv/bin/activate       # Windows: venv\Scripts\activate
    pip install -r requirements.txt

3.Frontend Setup:

    cd frontend
    npm install

4.Run in Dev Mode:

  • Backend :

    cd frontend
    ng serve

• Frontend :
  
    cd code
    uvicorn app:app --reload

## Docker Deployment

From project root:

    docker-compose up --build
Access app → http://localhost:4200

## Project Structure

    diet_recommendation_project/
        ├── code/
        │   ├── app.py
        │   ├── eda.py
        │   ├── data_eng.py
        │   ├── model_classifier.pkl
        │   ├── model_regressor.pkl
        │   ├── preprocessing.py
        │   ├── feature_engineering.py
        │   └── ml_pipeline.py
        │
        ├── frontend/
        │   └── src/app/
        │       ├── components/
        │       ├── services/
        │       └── pages/
        │
        ├── data/
        │   ├── raw_dataset.csv
        │   ├── enriched_dataset.csv
        │   └── models/
        │
        ├── tutos/
        ├── Dockerfile
        ├── Dockerfile.frontend
        ├── docker-compose.yml
        └── README.md

    
## Author

Mohamed Haroun Mezned 

Tek-Up University 2026


























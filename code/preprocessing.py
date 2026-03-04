import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

def get_data_and_preprocessors():
    df = pd.read_csv('data/diet_data_enriched.csv')

    # Targets - UNIQUEMENT RÉGRESSION MULTI-OUTPUT
    y_reg = df[['Recommended_Calories', 'Recommended_Protein',
                'Recommended_Carbs', 'Recommended_Fats']]

    # Features de base (sans les cibles)
    drop_cols = [
        'Patient_ID', 'full_name',
        'Recommended_Calories', 'Recommended_Protein',
        'Recommended_Carbs', 'Recommended_Fats',
        'Recommended_Meal_Plan'
    ]
    X = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # Identification des types de colonnes
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'bool']).columns.tolist()

    # Transformateurs
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore')) # Important pour l'API
    ])

    # Préprocesseur global
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # Split des données
    X_train, X_test, y_reg_train, y_reg_test = train_test_split(
        X, y_reg, test_size=0.2, random_state=42
    )

    return (
        preprocessor,
        X_train, X_test, 
        y_reg_train, y_reg_test
    )
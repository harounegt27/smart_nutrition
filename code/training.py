from preprocessing import get_data_and_preprocessors
import numpy as np
import mlflow
import mlflow.sklearn

from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_absolute_error, r2_score, mean_absolute_percentage_error

from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

def run_training():
    print("📂 1. Chargement des données et préparation...")
    (
        preprocessor,
        X_train, X_test, 
        y_reg_train, y_reg_test
    ) = get_data_and_preprocessors()

    # Configuration MLflow
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("Diet_Recommendation_Regression")

    # Définition des modèles et hyperparamètres
    reg_models = {
        "RandomForest_Reg": {
            "model": RandomForestRegressor(random_state=42),
            "params": {
                'regressor__n_estimators': [100, 200, 300],
                'regressor__max_depth': [10, 20, None],
                'regressor__min_samples_split': [2, 5]
            }
        },
        "XGBoost_Reg": {
            "model": XGBRegressor(random_state=42, objective='reg:squarederror'),
            "params": {
                'regressor__n_estimators': [200, 400, 600],
                'regressor__learning_rate': [0.03, 0.05, 0.1],
                'regressor__max_depth': [4, 6, 8],
                'regressor__subsample': [0.8, 1.0]
            }
        }
    }

    print("\n🚀 2. Début de l'entraînement des modèles...")

    for model_name, mp in reg_models.items():
        print(f"\n{'='*60}")
        print(f"⚙️ Training {model_name}")
        print(f"{'='*60}")

        with mlflow.start_run(run_name=f"{model_name}_Run"):

            # Création du Pipeline complet (Preprocessing + Modèle)
            # C'est ce pipeline qui sera sauvegardé et utilisé dans FastAPI
            pipeline = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('regressor', mp["model"])
            ])

            # Recherche d'hyperparamètres
            random_search = RandomizedSearchCV(
                estimator=pipeline,
                param_distributions=mp["params"],
                n_iter=10, 
                scoring='neg_mean_absolute_error',
                cv=5,
                random_state=42,
                verbose=1,
                n_jobs=-1
            )

            random_search.fit(X_train, y_reg_train)
            
            best_model = random_search.best_estimator_
            y_pred = best_model.predict(X_test)

            # Calcul des métriques
            mae = mean_absolute_error(y_reg_test, y_pred)
            r2 = r2_score(y_reg_test, y_pred)
            mape = mean_absolute_percentage_error(y_reg_test, y_pred)

            print(f"\n📊 Performance sur le jeu de test :")
            print(f"   MAE  (Erreur moyenne absolue): {mae:.2f}")
            print(f"   R²   (Score de détermination) : {r2:.4f}")
            print(f"   MAPE (Erreur pourcentage)     : {mape:.2%}")

            # Logging dans MLflow
            mlflow.log_params(random_search.best_params_)
            mlflow.log_metric("MAE", mae)
            mlflow.log_metric("R2_Score", r2)
            mlflow.log_metric("MAPE", mape)

            # Sauvegarde du modèle
            # Le modèle sauvegardé contient DÉJÀ le préprocesseur à l'intérieur
            mlflow.sklearn.log_model(best_model, "model")
            
            print(f"✅ Modèle sauvegardé dans MLflow (Run ID: {mlflow.active_run().info.run_id})")

    print("\n✨ Entraînement terminé ! Prêt pour FastAPI.")

if __name__ == "__main__":
    run_training()
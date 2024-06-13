import mlflow
import mlflow.sklearn
import mlflow.tensorflow
import mlflow.pyfunc
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
import contextily as ctx
import pandas as pd


def train_and_log_model(model, model_name, X_train, y_train, X_val, y_val):
    with mlflow.start_run(run_name=model_name):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)

        # Metryki
        mae = mean_absolute_error(y_val, y_pred)
        mse = mean_squared_error(y_val, y_pred)
        rmse = mean_squared_error(y_val, y_pred, squared=False)
        r2 = r2_score(y_val, y_pred)

        mlflow.log_metric('MAE', mae)
        mlflow.log_metric('MSE', mse)
        mlflow.log_metric('RMSE', rmse)
        mlflow.log_metric('R2', r2)

        mlflow.sklearn.log_model(model, model_name)
        print(f"{model_name} - MAE: {mae}, MSE: {mse}, RMSE: {rmse}, R2: {r2}")

def rf_best(X_train,y_train,X_val,y_val):
    param_distributions = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }

    random_search = RandomizedSearchCV(
        estimator=RandomForestRegressor(random_state=42),
        param_distributions=param_distributions,
        n_iter=10,
        cv=3,
        verbose=2,
        random_state=42,
        n_jobs=-1
    )

    with mlflow.start_run(run_name='RandomForest RandomizedSearch'):
        random_search.fit(X_train, y_train)

        best_model = random_search.best_estimator_
        mlflow.sklearn.log_model(best_model, 'RandomForest Best Model')

        mlflow.log_params(random_search.best_params_)

        y_pred = best_model.predict(X_val)

        # Metryki
        mae = mean_absolute_error(y_val, y_pred)
        mse = mean_squared_error(y_val, y_pred)
        rmse = mean_squared_error(y_val, y_pred, squared=False)
        r2 = r2_score(y_val, y_pred)

        mlflow.log_metric('MAE', mae)
        mlflow.log_metric('MSE', mse)
        mlflow.log_metric('RMSE', rmse)
        mlflow.log_metric('R2', r2)

        print(f"RandomForest Best Model - MAE: {mae}, MSE: {mse}, RMSE: {rmse}, R2: {r2}")
        return best_model

def krk_pred(y_krk_true,y_krk_pred):
    mae_krk = mean_absolute_error(y_krk_true, y_krk_pred)
    mse_krk = mean_squared_error(y_krk_true, y_krk_pred)
    rmse_krk = mean_squared_error(y_krk_true, y_krk_pred, squared=False)
    r2_krk = r2_score(y_krk_true, y_krk_pred)

    print(f"Kraków - MAE: {mae_krk}, MSE: {mse_krk}, RMSE: {rmse_krk}, R2: {r2_krk}")

    with mlflow.start_run(run_name='Krakow Prediction Evaluation'):
        mlflow.log_metric('MAE_Krakow', mae_krk)
        mlflow.log_metric('MSE_Krakow', mse_krk)
        mlflow.log_metric('RMSE_Krakow', rmse_krk)
        mlflow.log_metric('R2_Krakow', r2_krk)




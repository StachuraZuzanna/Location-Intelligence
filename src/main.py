from load_data import load
from arguments import arg
from models import ml
import time
import pandas as pd
from shapely import wkt
import os
import osmnx as ox
from shapely.ops import unary_union
import geopandas as gpd
from make_visualisation import plots
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

def main():

    data_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    ams_file = os.path.join(data_folder, 'amsterdam_bike_paths_extended.parquet')
    krk_file = os.path.join(data_folder, 'krakow_bike_paths_extended.parquet')

    amsterdam = pd.read_parquet(ams_file)
    cracow = pd.read_parquet(krk_file)
    amsterdam_bounds = {"north": 52.441157, "south": 52.2688, "east": 5.1127658, "west": 4.728073}
    cracow_bounds = {"north": 50.1257, "south": 49.9639, "east": 20.215, "west": 19.7946}
    amsterdam_area = ox.geocode_to_gdf('Amsterdam, Netherlands')
    cracow_area = ox.geocode_to_gdf('Kraków')

    gdf_ams = load.create_gdf(amsterdam)
    gdf_krk = load.create_gdf(cracow)
    plots.plot_bike_lanes(gdf_ams, gdf_krk)
    gdf_ams, gdf_krk = load.assign_hex_df(gdf_ams, gdf_krk)

    gdf_krk_hex = load.create_h3_hex_grid(gdf_krk, cracow_bounds)
    gdf_ams_hex = load.create_h3_hex_grid(gdf_ams, amsterdam_bounds)
    gdf_ams_hex = load.crop_hex_grid(gdf_ams_hex, gdf_ams, amsterdam_area, 2180)
    gdf_krk_hex = load.crop_hex_grid(gdf_krk_hex, gdf_krk, cracow_area, 2180)
    plots.plot_hex_and_bike_lanes(gdf_ams_hex, gdf_ams, amsterdam_area, gdf_krk_hex, gdf_krk, cracow_area)

    ### Arguments
    ##Walks and main roads
    hex_area_ams = unary_union(gdf_ams_hex.geometry)
    gdf_ams_hex, ams_walks_clipped, ams_roads_main_clipped = arg.calculate_road_lengths(amsterdam_bounds, gdf_ams_hex,
                                                                              hex_area_ams)
    hex_area_krk = unary_union(gdf_krk_hex.geometry)
    gdf_krk_hex, krk_walks_clipped, krk_roads_main_clipped = arg.calculate_road_lengths(cracow_bounds, gdf_krk_hex,
                                                                                    hex_area_krk)
    plots.plot_walks_and_bike_lanes(amsterdam_area,ams_walks_clipped,gdf_ams_hex,gdf_ams,
                                    cracow_area,krk_walks_clipped,gdf_krk_hex,gdf_krk)

    plots.plot_roads_and_bike_lanes(amsterdam_area, ams_roads_main_clipped, gdf_ams_hex, gdf_ams,
                                    cracow_area,krk_roads_main_clipped, gdf_krk_hex, gdf_krk)
    ## Green space area
    gdf_ams_hex, ams_green_spaces_clipped = arg.calculate_green_space_areas(amsterdam_bounds, gdf_ams_hex, hex_area_ams)
    gdf_krk_hex, krk_green_spaces_clipped = arg.calculate_green_space_areas(cracow_bounds, gdf_krk_hex, hex_area_krk)
    plots.plot_green_area_and_bike_lanes(amsterdam_area,ams_green_spaces_clipped,gdf_ams_hex,gdf_ams,cracow_area,krk_green_spaces_clipped,gdf_krk_hex,gdf_krk)

    #City center
    center_amsterdam = arg.get_city_center("Amsterdam, Netherlands")
    center_cracow = arg.get_city_center("Kraków, Poland")
    gdf_ams_hex = arg.distance_to_city_center(gdf_ams_hex, center_amsterdam)
    gdf_krk_hex = arg.distance_to_city_center(gdf_krk_hex, center_cracow)

    ## Number of amenities
    gdf_ams_hex, ams_service_amenities_clipped = arg.calculate_service_amenities(amsterdam_bounds, gdf_ams_hex,
                                                                             hex_area_ams)
    gdf_krk_hex, krk_service_amenities_clipped = arg.calculate_service_amenities(cracow_bounds, gdf_krk_hex, hex_area_krk)

    plots.plot_amenities_and_bike_lanes(amsterdam_area, ams_service_amenities_clipped, gdf_ams_hex, gdf_ams, cracow_area,
                                      krk_service_amenities_clipped, gdf_krk_hex, gdf_krk)
    print(gdf_ams_hex)

    # gdf_ams_hex = pd.read_csv('results/Dane_amsterdam.csv')
    # gdf_krk_hex = pd.read_csv('results/Dane_krakow.csv')
    # # Konwersja kolumny 'geometry' na obiekty geograficzne
    # gdf_ams_hex['geometry'] = gdf_ams_hex['geometry'].apply(wkt.loads)
    # gdf_krk_hex['geometry'] = gdf_krk_hex['geometry'].apply(wkt.loads)
    # gdf_ams_hex = gpd.GeoDataFrame(gdf_ams_hex, geometry='geometry')
    # gdf_krk_hex = gpd.GeoDataFrame(gdf_krk_hex, geometry='geometry')

    # Split data into features and target variable
    X = gdf_ams_hex[['main_roads_length','walks_length','green_space_area','distance_to_city_center','service_amenity_count']]
    y = gdf_ams_hex['bike_path_length']

    # Split the data into training, validation, and test sets
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
    mlflow.set_experiment('Amsterdam_Bike_Paths_Prediction')

    # Regresja liniowa
    linear_regressor = LinearRegression()
    ml.train_and_log_model(linear_regressor, 'Linear Regression', X_train, y_train, X_val, y_val)

    # Regresor wektorów nośnych (SVR)
    svr_regressor = SVR()
    ml.train_and_log_model(svr_regressor, 'Support Vector Regressor', X_train, y_train, X_val, y_val)

    # Las losowy
    rf_regressor = RandomForestRegressor(random_state=42)
    ml.train_and_log_model(rf_regressor, 'Random Forest Regressor', X_train, y_train, X_val, y_val)

    # Gradient Boosting Machines (GBM)
    gbm_regressor = GradientBoostingRegressor(random_state=42)
    ml.train_and_log_model(gbm_regressor, 'Gradient Boosting Regressor', X_train, y_train, X_val, y_val)

    best_model = ml.rf_best(X_train, y_train,X_val,y_val)

    X_krk = gdf_krk_hex.drop(['bike_path_length', 'geometry', 'h3_index'], axis=1)
    y_krk_true = gdf_krk_hex['bike_path_length']

    y_krk_pred = best_model.predict(X_krk)

    ml.krk_pred(y_krk_true, y_krk_pred)
    X_ams = gdf_ams_hex.drop(['bike_path_length', 'geometry', 'h3_index'], axis=1)
    y_ams = gdf_ams_hex['bike_path_length']
    y_ams_pred = best_model.predict(X_ams)

    # Dodanie przewidywanych wartości do GeoDataFrames
    gdf_ams_hex['bike_path_length_pred'] = y_ams_pred
    gdf_krk_hex['bike_path_length_pred'] = y_krk_pred


    plots.plot_pred(gdf_ams_hex, gdf_krk_hex)
if __name__ == "__main__":
    main()
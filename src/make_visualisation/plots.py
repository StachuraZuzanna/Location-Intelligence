import matplotlib.pyplot as plt
import geopandas as gpd
import os
import contextily as ctx

from matplotlib.colors import Normalize
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import matplotlib.cm as cm
from matplotlib.cm import ScalarMappable


def plot_bike_lanes(gdf_ams,gdf_krk):
    fig, axes = plt.subplots(1, 2, figsize=[10, 10])
    gdf_ams.plot(ax=axes[0], linewidth=1, edgecolor='blue')

    axes[0].set_title('Amsterdam - scieżki rowerowe')
    axes[0].set_xlabel('Długość geograficzna')
    axes[0].set_ylabel('Szerokość geograficzna')

    gdf_krk.plot(ax=axes[1], linewidth=1, edgecolor='blue')

    axes[1].set_title('Kraków - scieżki rowerowe')
    axes[1].set_xlabel('Długość geograficzna')
    axes[1].set_ylabel('Szerokość geograficzna')
    # Save the figure to an image file
    if not os.path.exists("results/"):
        os.makedirs("results/")
    plt.savefig(os.path.join("results/", 'Mapa_ścieżki_rowerowe.png'))

    plt.close()

# Wizualizacja
def plot_hex_and_bike_lanes(gdf_ams_hex,gdf_ams,amsterdam_area,gdf_krk_hex,gdf_krk,cracow_area):
    fig, ax = plt.subplots(1, 2, figsize=(10, 10))
    gdf_ams.plot(ax=ax[0], edgecolor='green', facecolor='none', alpha=0.5)
    gdf_ams_hex.plot(ax=ax[0], edgecolor='lightblue', facecolor='none', alpha=0.5)
    amsterdam_area['geometry'].boundary.plot(ax=ax[0])
    # Set plot title and labels
    ax[0].set_title('Boundaries and bike trails in Amsterdam')
    ax[0].set_xlabel('Longitude')
    ax[0].set_ylabel('Latitude')

    gdf_krk.plot(ax=ax[1], edgecolor='green', facecolor='none', alpha=0.5)
    gdf_krk_hex.plot(ax=ax[1], edgecolor='lightblue', facecolor='none', alpha=0.5)
    cracow_area['geometry'].boundary.plot(ax=ax[1])
    # Set plot title and labels
    ax[1].set_title('Boundaries and bike trails in Kraków')
    ax[1].set_xlabel('Longitude')
    ax[1].set_ylabel('Latitude')
    if not os.path.exists("results/"):
        os.makedirs("results/")
    plt.savefig(os.path.join("results/", 'Mapa_ścieżki_rowerowe_i_siatka_hex.png'))

    plt.close()


def plot_walks_and_bike_lanes(amsterdam_area,ams_walks_clipped,gdf_ams_hex,gdf_ams,cracow_area,krk_walks_clipped,gdf_krk_hex,gdf_krk):
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))  # Adjusted figsize for better visibility
    amsterdam_area['geometry'].boundary.plot(ax=ax[0])
    ams_walks_clipped.plot(ax=ax[0], edgecolor='pink', facecolor='none', alpha=0.5, linewidth=0.6,
                           label='Walks Clipped')
    gdf_ams_hex.plot(ax=ax[0], edgecolor='lightblue', facecolor='none', alpha=0.5, label='Hexagonal Grid')
    gdf_ams.plot(ax=ax[0], edgecolor='green', facecolor='none', alpha=0.5, label='Amsterdam Area')

    ax[0].set_title('Ścieżki rowerowe i chodniki w Amsterdamie')
    ax[0].set_xlabel('Longitude')
    ax[0].set_ylabel('Latitude')
    ax[0].legend()

    cracow_area['geometry'].boundary.plot(ax=ax[1])
    krk_walks_clipped.plot(ax=ax[1], edgecolor='pink', facecolor='none', alpha=0.5, linewidth=0.6,
                           label='Walks Clipped')
    gdf_krk_hex.plot(ax=ax[1], edgecolor='lightblue', facecolor='none', alpha=0.5, label='Hexagonal Grid')
    gdf_krk.plot(ax=ax[1], edgecolor='green', facecolor='none', alpha=0.5, label='Cracow Area')

    ax[1].set_title('Ścieżki rowerowe i chodniki w Krakowie')
    ax[1].set_xlabel('Longitude')
    ax[1].set_ylabel('Latitude')
    ax[1].legend()
    plt.tight_layout()
    if not os.path.exists("results/"):
        os.makedirs("results/")
    plt.savefig(os.path.join("results/", 'Mapa_ścieżki_rowerowe_i_chodniki.png'))

    plt.close()

def plot_roads_and_bike_lanes(amsterdam_area,ams_roads_main_clipped,gdf_ams_hex,gdf_ams,cracow_area,krk_roads_main_clipped,gdf_krk_hex,gdf_krk):
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))  # Adjusted figsize for better visibility
    amsterdam_area['geometry'].boundary.plot(ax=ax[0])
    ams_roads_main_clipped.plot(ax=ax[0], edgecolor='orange', facecolor='none', alpha=0.6, linewidth=1,
                                label='Main Roads Clipped')
    gdf_ams_hex.plot(ax=ax[0], edgecolor='lightblue', facecolor='none', alpha=0.5, label='Hexagonal Grid')
    gdf_ams.plot(ax=ax[0], edgecolor='green', facecolor='none', alpha=0.5, label='Amsterdam Area')

    ax[0].set_title('Ścieżki rowerowe i drogi główne w Amsterdamie')
    ax[0].set_xlabel('Longitude')
    ax[0].set_ylabel('Latitude')
    ax[0].legend()

    cracow_area['geometry'].boundary.plot(ax=ax[1])
    krk_roads_main_clipped.plot(ax=ax[1], edgecolor='orange', facecolor='none', alpha=0.6, linewidth=1,
                                label='Main Roads Clipped')
    gdf_krk_hex.plot(ax=ax[1], edgecolor='lightblue', facecolor='none', alpha=0.5, label='Hexagonal Grid')
    gdf_krk.plot(ax=ax[1], edgecolor='green', facecolor='none', alpha=0.5, label='Cracow Area')

    ax[1].set_title('Ścieżki rowerowe i drogi główne w Krakowie')
    ax[1].set_xlabel('Longitude')
    ax[1].set_ylabel('Latitude')
    ax[1].legend()

    plt.tight_layout()
    if not os.path.exists("results/"):
        os.makedirs("results/")
    plt.savefig(os.path.join("results/", 'Mapa_ścieżki_rowerowe_i_drogi_główne.png'))

    plt.close()

def plot_green_area_and_bike_lanes(amsterdam_area,ams_green_spaces_clipped,gdf_ams_hex,gdf_ams,cracow_area,krk_green_spaces_clipped,gdf_krk_hex,gdf_krk):
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))
    amsterdam_area['geometry'].boundary.plot(ax=ax[0])
    ams_green_spaces_clipped.plot(ax=ax[0], edgecolor='brown', facecolor='none', alpha=1, label='Green spaces Clipped')
    gdf_ams_hex.plot(ax=ax[0], edgecolor='lightblue', facecolor='none', alpha=0.5, label='Hexagonal Grid')
    gdf_ams.plot(ax=ax[0], edgecolor='green', facecolor='none', alpha=0.5, label='Amsterdam Area')

    ax[0].set_title('Ścieżki rowerowe i tereny zielone w Amsterdamie')
    ax[0].set_xlabel('Longitude')
    ax[0].set_ylabel('Latitude')
    ax[0].legend()

    cracow_area['geometry'].boundary.plot(ax=ax[1])
    krk_green_spaces_clipped.plot(ax=ax[1], edgecolor='brown', facecolor='none', alpha=1, label='Walks Clipped')
    gdf_krk_hex.plot(ax=ax[1], edgecolor='lightblue', facecolor='none', alpha=0.5, label='Hexagonal Grid')
    gdf_krk.plot(ax=ax[1], edgecolor='green', facecolor='none', alpha=0.5, label='Cracow Area')

    ax[1].set_title('Ścieżki rowerowe i tereny zielone w Krakowie')
    ax[1].set_xlabel('Longitude')
    ax[1].set_ylabel('Latitude')
    ax[1].legend()

    plt.tight_layout()
    if not os.path.exists("results/"):
        os.makedirs("results/")
    plt.savefig(os.path.join("results/", 'Mapa_ścieżki_rowerowe_i_tereny_zielone.png'))

    plt.close()

def plot_amenities_and_bike_lanes(amsterdam_area,ams_service_amenities_clipped,gdf_ams_hex,gdf_ams,cracow_area,krk_service_amenities_clipped,gdf_krk_hex,gdf_krk):
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))  # Adjusted figsize for better visibility

    # Plot Amsterdam
    amsterdam_area['geometry'].boundary.plot(ax=ax[0])
    gdf_ams_hex.plot(ax=ax[0], edgecolor='lightblue', facecolor='none', alpha=0.5, label='Hexagonal Grid')
    ams_service_amenities_clipped.plot(ax=ax[0], color='purple', markersize=1, alpha=0.5, label='Service Amenities')
    gdf_ams.plot(ax=ax[0], edgecolor='green', facecolor='none', alpha=0.5, linewidth=2, label='Amsterdam Area')

    ax[0].set_title('Ścieżki rowerowe i lokale usługowe w Amsterdamie')
    ax[0].set_xlabel('Longitude')
    ax[0].set_ylabel('Latitude')
    ax[0].legend()

    # Plot Kraków
    cracow_area['geometry'].boundary.plot(ax=ax[1])
    gdf_krk_hex.plot(ax=ax[1], edgecolor='lightblue', facecolor='none', alpha=0.5, label='Hexagonal Grid')
    krk_service_amenities_clipped.plot(ax=ax[1], color='purple', markersize=1, alpha=0.5, label='Service Amenities')
    gdf_krk.plot(ax=ax[1], edgecolor='green', facecolor='none', alpha=0.5, linewidth=2, label='Cracow Area')

    ax[1].set_title('Ścieżki rowerowe i lokale usługowe w Krakowie')
    ax[1].set_xlabel('Longitude')
    ax[1].set_ylabel('Latitude')
    ax[1].legend()

    plt.tight_layout()
    if not os.path.exists("results/"):
        os.makedirs("results/")
    plt.savefig(os.path.join("results/", 'Mapa_ścieżki_rowerowe_i_lokale_usługowe.png'))

    plt.close()


def plot_bike_paths(gdf, true_col, pred_col, title, ax):
    # Plot the true bike path lengths
    gdf.plot(column=true_col, cmap='Reds', legend=True, alpha=0.6, ax=ax,
             legend_kwds={'label': "Rzeczywista długość scieżek rowerowych", 'orientation': "vertical", 'shrink': 0.4})

    # # Plot the predicted bike path lengths
    # gdf.plot(column=pred_col, cmap='Reds', legend=True, alpha=0.6, ax=ax,
    #          legend_kwds={'label': "Przewidziana długość scieżek rowerowych", 'orientation': "vertical", 'shrink': 0.5})

    # Add basemap
    # ctx.add_basemap(ax, crs=gdf.crs.to_string())

    ax.set_title(title, fontsize=15)
    ax.axis('off')


def plot_predicted_bike_paths(gdf, true_col, pred_col, title, ax):
    # Plot the predicted bike path lengths
    gdf.plot(column=pred_col, cmap='Reds', legend=True, alpha=0.6, ax=ax,
             legend_kwds={'label': "Przewidziana długość scieżek rowerowych", 'orientation': "vertical", 'shrink': 0.4})

    # Add basemap
    # ctx.add_basemap(ax, crs=gdf.crs.to_string())

    ax.set_title(title, fontsize=15)
    ax.axis('off')


def plot_pred(gdf_ams_hex, gdf_krk_hex):
    fig, axes = plt.subplots(2, 2, figsize=(15, 20))

    # Mapa dla Amsterdamu
    plot_bike_paths(gdf_ams_hex, 'bike_path_length', 'bike_path_length_pred',
                    'Amsterdam - Rzeczywista ługość scieżek rowerowych', axes[0, 0])
    plot_predicted_bike_paths(gdf_ams_hex, 'bike_path_length', 'bike_path_length_pred',
                              'Amsterdam - Przewidziana długość scieżek rowerowych', axes[0, 1])

    # Mapa dla Krakowa
    plot_bike_paths(gdf_krk_hex, 'bike_path_length', 'bike_path_length_pred',
                    'Kraków -  Rzeczywista długość scieżek rowerowych', axes[1, 0])
    plot_predicted_bike_paths(gdf_krk_hex, 'bike_path_length', 'bike_path_length_pred',
                              'Kraków -  Przewidziana długość scieżek rowerowych', axes[1, 1])

    plt.tight_layout()
    if not os.path.exists("results/"):
        os.makedirs("results/")
    plt.savefig(os.path.join("results/", 'Prawdziwe_i_Przewidziane_ścieżki_rowerowe.png'))

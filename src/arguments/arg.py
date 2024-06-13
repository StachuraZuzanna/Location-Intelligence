import osmnx as ox
import geopandas as gpd
from geopy.geocoders import Nominatim
from shapely.geometry import Point


def calculate_road_lengths(amsterdam_bounds, gdf_ams_hex,hex_area):
    # Get road and walk networks
    Ams_roads = ox.graph_from_bbox(bbox=(amsterdam_bounds['north'],
                                         amsterdam_bounds['south'],
                                         amsterdam_bounds['east'],
                                         amsterdam_bounds['west']),
                                   network_type='drive')
    Ams_walks = ox.graph_from_bbox(bbox=(amsterdam_bounds['north'],
                                         amsterdam_bounds['south'],
                                         amsterdam_bounds['east'],
                                         amsterdam_bounds['west']),
                                   network_type='walk')

    # Convert the road network to a GeoDataFrame of edges
    ams_roads = ox.graph_to_gdfs(Ams_roads, nodes=False)
    ams_walks = ox.graph_to_gdfs(Ams_walks, nodes=False)

    # Filter main roads
    ams_roads['highway'] = ams_roads['highway'].apply(lambda x: x[0] if isinstance(x, list) else x)
    main_road_types = ['secondary', 'primary', 'tertiary', 'busway', 'motorway_link', 'motorway']
    ams_roads_main = ams_roads[ams_roads['highway'].isin(main_road_types)]

    # Clip to the hexagonal area
    # hex_area = unary_union(gdf_ams_hex.geometry)
    ams_roads_main_clipped = ams_roads_main.geometry.clip(hex_area)
    ams_walks_clipped = ams_walks.geometry.clip(hex_area)

    # Project to the appropriate CRS
    gdf_ams_hex = gdf_ams_hex.to_crs(epsg=28992)
    ams_roads_main_clipped_proj = ams_roads_main_clipped.to_crs(epsg=28992)
    ams_walks_clipped_proj = ams_walks_clipped.to_crs(epsg=28992)

    # Initialize length columns
    gdf_ams_hex['main_roads_length'] = 0.0
    gdf_ams_hex['walks_length'] = 0.0

    # Calculate lengths for each hexagon
    for i, polygon in gdf_ams_hex.iterrows():
        clipped_r = ams_roads_main_clipped_proj.clip(polygon.geometry)
        clipped_w = ams_walks_clipped_proj.clip(polygon.geometry)
        gdf_ams_hex.at[i, 'main_roads_length'] = clipped_r.length.sum()
        gdf_ams_hex.at[i, 'walks_length'] = clipped_w.length.sum()

    # Reproject back to the original CRS
    gdf_ams_hex = gdf_ams_hex.to_crs(epsg=4326)

    return gdf_ams_hex,ams_walks_clipped,ams_roads_main_clipped

def calculate_green_space_areas(amsterdam_bounds, gdf_ams_hex, hex_area):
    # Get green spaces network
    Ams_green_spaces = ox.geometries_from_bbox(north=amsterdam_bounds['north'],
                                               south=amsterdam_bounds['south'],
                                               east=amsterdam_bounds['east'],
                                               west=amsterdam_bounds['west'],
                                               tags={'leisure': 'park',
                                                     'landuse': ['recreation_ground', 'forest'],
                                                     'natural': 'wood'})

    # Clip to the hexagonal area
    ams_green_spaces_clipped = gpd.clip(Ams_green_spaces, hex_area)

    # Project to the appropriate CRS
    gdf_ams_hex = gdf_ams_hex.to_crs(epsg=28992)
    ams_green_spaces_clipped_proj = ams_green_spaces_clipped.to_crs(epsg=28992)

    # Initialize area columns
    gdf_ams_hex['green_space_area'] = 0.0

    # Calculate areas for each hexagon
    for i, polygon in gdf_ams_hex.iterrows():
        clipped_g = gpd.clip(ams_green_spaces_clipped_proj, polygon.geometry)
        gdf_ams_hex.at[i, 'green_space_area'] = clipped_g.area.sum()

    # Reproject back to the original CRS
    gdf_ams_hex = gdf_ams_hex.to_crs(epsg=4326)

    return gdf_ams_hex, ams_green_spaces_clipped

def get_city_center(city_name):
    geolocator = Nominatim(user_agent="city_center_locator")
    location = geolocator.geocode(city_name)
    center_gdf = gpd.GeoDataFrame(geometry=[Point(location.longitude, location.latitude)],crs=4326)
    if location:
        return center_gdf
    else:
        return None

def distance_to_city_center(hex_gdf, center_gdf, epsg=28992):
    old_epsg = hex_gdf.crs.to_epsg()
    center_gdf_proj = center_gdf.to_crs(epsg=epsg)
    hex_gdf = hex_gdf.to_crs(epsg=epsg)
    hex_gdf['distance_to_city_center'] = hex_gdf.geometry.centroid.distance(center_gdf_proj.iloc[0,0])
    hex_gdf = hex_gdf.to_crs(epsg=old_epsg)
    return hex_gdf


def calculate_service_amenities(amsterdam_bounds, gdf_ams_hex, hex_area):
    # Get service amenities
    service_amenity_tags = {
        'amenity': True,  # Includes a variety of amenities like restaurants, cafes, schools, etc.
        'shop': True,  # Includes various types of shops
        'office': True  # Includes office buildings
    }

    Ams_service_amenities = ox.geometries_from_bbox(north=amsterdam_bounds['north'],
                                                    south=amsterdam_bounds['south'],
                                                    east=amsterdam_bounds['east'],
                                                    west=amsterdam_bounds['west'],
                                                    tags=service_amenity_tags)

    # Clip to the hexagonal area
    ams_service_amenities_clipped = gpd.clip(Ams_service_amenities, hex_area)

    # Initialize a column for counting amenities
    gdf_ams_hex['service_amenity_count'] = 0

    # Calculate the number of amenities for each hexagon
    for i, polygon in gdf_ams_hex.iterrows():
        clipped_amenities = gpd.clip(ams_service_amenities_clipped, polygon.geometry)
        gdf_ams_hex.at[i, 'service_amenity_count'] = clipped_amenities.shape[0]

    return gdf_ams_hex, ams_service_amenities_clipped
from geopy.distance import geodesic
import pandas as pd
import folium
from typing import List, Tuple
import warnings

def get_locations_within_range(lat: float, long: float, n: float, df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns all locations from the DataFrame that are within n kilometers of the given GPS location,
    including the distance to each location.

    Args:
    lat (float): Latitude of the center point
    long (float): Longitude of the center point
    n (float): Range in kilometers
    df (pd.DataFrame): DataFrame containing location data

    Returns:
    pd.DataFrame: DataFrame with locations within the specified range and their distances
    """
    center_point = (lat, long)
    
    def calculate_geodesic_distance(row):
        location_point = (row['lat'], row['long'])
        distance = geodesic(center_point, location_point).kilometers
        return distance if distance <= n else None

    # Calculate distances for all points
    df['distance'] = df.apply(calculate_geodesic_distance, axis=1)

    # Filter out locations beyond the range and sort by distance
    result_df = df[df['distance'].notnull()].sort_values('distance')

    return result_df


def plot_points_on_map(df: pd.DataFrame, searchers: List[Tuple[float, float, str]] = None, 
                       center_lat: float = None, center_lon: float = None, zoom_start: int = 9) -> folium.Map:
    """
    Plot points from a DataFrame and optional searcher locations on a Folium map.

    Args:
    df (pd.DataFrame): DataFrame containing 'long', 'lat', and 'Bezeichnung' columns for restaurants
    searchers (List[Tuple[float, float, str]]): Optional list of searcher locations (lat, lon, name)
    center_lat (float): Latitude for map center (optional)
    center_lon (float): Longitude for map center (optional)
    zoom_start (int): Initial zoom level for the map

    Returns:
    folium.Map: Folium map object with plotted points
    """
    if df.empty:
        if searchers:
            # Calculate the mean of searcher locations
            center_lat = sum(s[0] for s in searchers) / len(searchers)
            center_lon = sum(s[1] for s in searchers) / len(searchers)
            warnings.warn("No locations to plot. Returning a map centered on the mean of searcher locations.", UserWarning)
        else:
            center_lat, center_lon = 52.18698, 9.07984  # Default to Rinteln, Germany
            warnings.warn("No locations or searchers to plot. Returning an empty map centered on Rinteln.", UserWarning)
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_start)
        
        # Add markers for searcher locations if provided
        if searchers:
            for lat, lon, name in searchers:
                folium.Marker(
                    location=[lat, lon],
                    popup=name,
                    tooltip=name,
                    icon=folium.Icon(color='blue', icon='user')
                ).add_to(m)
        
        return m
    
    # If center coordinates are not provided, use the mean of all points
    if center_lat is None or center_lon is None:
        center_lat = df['lat'].mean()
        center_lon = df['long'].mean()

    # Create a map centered on the specified or calculated location
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_start)

    # Add markers for each restaurant in the DataFrame
    for idx, row in df.iterrows():
        if 'distance' in df.columns:
            tooltip = f"{row['Bezeichnung']} - {row['distance']:.2f} km"
        else:
            tooltip = row['Bezeichnung']
        
        folium.Marker(
            location=[row['lat'], row['long']],
            popup=row['Bezeichnung'],
            tooltip=tooltip,
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

    # Add markers for searcher locations if provided
    if searchers:
        for lat, lon, name in searchers:
            folium.Marker(
                location=[lat, lon],
                popup=name,
                tooltip=name,
                icon=folium.Icon(color='blue', icon='user')
            ).add_to(m)

    return m

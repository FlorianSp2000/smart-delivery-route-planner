from typing import List, Tuple,

import osmnx as ox
import networkx as nx
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from shapely.geometry import Point


class DeliveryRouter:
    def __init__(self, city: str = "Berlin, Germany"):
        """Initialize the router with a specific city's road network."""
        # Initialize Nominatim geocoder
        self.geocoder = Nominatim(user_agent="delivery_router_rinteln", timeout=6)
        self.city_boundary = ox.geocode_to_gdf(city)

        # Download and create the road network for the specified city
        self.G = ox.graph_from_place(city, network_type="drive", simplify=False)
        
        # Convert to projected graph for accurate distance calculations; UTM zone 32N
        self.G_proj = ox.project_graph(self.G, to_crs="EPSG:25832")
        
        # Store restaurants data
        self.restaurants = {}
        self.load_all_restaurants()
        
    def load_all_restaurants(self):
        """Load all restaurants from OpenStreetMap within the city boundary."""
        # Define tags for restaurants and similar establishments
        tags = {
            'amenity': ['restaurant', 'cafe', 'fast_food', 'bar', 'pub'],
            'cuisine': True  # This will get all cuisine types
        }
        
        # Get all POIs with these tags within the city boundary
        pois = ox.features_from_place("Rinteln, Germany", tags=tags)
        
        # Process each POI
        for idx, poi in pois.iterrows():
            name = poi.get('name', 'Unknown Restaurant')
            if name != 'Unknown Restaurant':  # Only add places with names
                try:
                    # Get coordinates
                    if isinstance(poi.geometry, Point):
                        lat, lon = poi.geometry.y, poi.geometry.x
                    else:
                        # For polygons, use centroid
                        lat, lon = poi.geometry.centroid.y, poi.geometry.centroid.x
                    
                    # Get address components if available
                    street = poi.get('addr:street', '')
                    housenumber = poi.get('addr:housenumber', '')
                    address = f"{street} {housenumber}, Rinteln" if street and housenumber else "Rinteln"
                    
                    # Store restaurant data
                    self.restaurants[name] = {
                        "address": address,
                        "lat": lat,
                        "lon": lon,
                        "node": ox.nearest_nodes(self.G, lon, lat),
                        "type": poi.get('amenity', 'unknown'),
                        "cuisine": poi.get('cuisine', 'unknown')
                    }
                    print(f"Added: {name} ({address})")
                except Exception as e:
                    print(f"Error adding {name}: {e}")

    def add_restaurant(self, name: str, address: str) -> bool:
        """Add a restaurant to the system with its location."""
        try:
            location = self.geocoder.geocode(f"{name}, {address}, Germany")
            if location:
                self.restaurants[name] = {
                    "address": address,
                    "lat": location.latitude,
                    "lon": location.longitude,
                    "node": ox.nearest_nodes(self.G, location.longitude, location.latitude)
                }
                return True
            return False
        except Exception as e:
            print(f"Error adding restaurant: {e}")
            return False
    
    def calculate_route_advanced(self, start_coords: Tuple[float, float], 
                        end_coords: Tuple[float, float]) -> List[Tuple[float, float]]:
        """Calculate a detailed route between two points."""
        start_node = ox.nearest_nodes(self.G, start_coords[1], start_coords[0])
        end_node = ox.nearest_nodes(self.G, end_coords[1], end_coords[0])
        
        # Find the shortest path by nodes
        path = nx.shortest_path(self.G, start_node, end_node, weight="length")
        
        # Retrieve the detailed geometry of the route
        route_coords = []
        for u, v in zip(path[:-1], path[1:]):  # Iterate over edges in the path
            edge_data = self.G[u][v][0]  # Get the edge data
            if "geometry" in edge_data:  # Use geometry if available
                route_coords.extend([(point[1], point[0]) for point in edge_data["geometry"].coords])
            else:  # Fall back to straight line if no geometry is present
                route_coords.extend([(self.G.nodes[u]['y'], self.G.nodes[u]['x']),
                                    (self.G.nodes[v]['y'], self.G.nodes[v]['x'])])
        
        return route_coords

    
    def visualize_map(self, driver_position: Tuple[float, float] = None, 
                     route: List[Tuple[float, float]] = None) -> folium.Map:
        """Create a visualization of restaurants, driver, and route."""
        # Create base map centered on Rinteln
        center_location = self.geocoder.geocode("Rinteln, Germany")
        m = folium.Map(location=[center_location.latitude, center_location.longitude], 
                      zoom_start=14)
        
        # Add restaurants with custom icons
        for name, data in self.restaurants.items():
            folium.Marker(
                [data["lat"], data["lon"]],
                popup=f"{name}\n{data['address']}",
                icon=folium.Icon(color='red', icon='cutlery')
            ).add_to(m)
        
        # Add driver position if provided
        if driver_position:
            folium.Marker(
                driver_position,
                popup="Driver Location",
                icon=folium.Icon(color='green', icon='user')
            ).add_to(m)
        
        # Add delivery route if provided
        if route:
            folium.PolyLine(
                route,
                weight=3,
                color='blue',
                opacity=0.8
            ).add_to(m)
        
        return m

    def get_estimated_delivery_time(self, route: List[Tuple[float, float]], 
                                  avg_speed_kmh: float = 30) -> float:
        """Calculate estimated delivery time in minutes for a route."""
        total_distance = 0
        for i in range(len(route) - 1):
            total_distance += geodesic(route[i], route[i + 1]).kilometers
        
        # Convert to hours and then to minutes
        return (total_distance / avg_speed_kmh) * 60

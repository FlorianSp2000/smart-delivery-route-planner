# smart-delivery-route-planner
Intelligent navigation and discovery platform for delivery services, integrating interactive maps, points of interest (POIs), and advanced route optimization to streamline delivery operations.


## Requirements of the Application
- Route map with Points of Interest (POI), including restaurants and (Home) Addresses
- Street map has to be up-to-date and free to use commercially
- Area of focus is Germany
- Efficient Shortest Path Computation
- User Position Tracking through GPS data
- Has to be easily integrable on mobile devices
- self-hosting

The common approach consists of using open data sources like OpenStreetMap, supplement it with data from private vendors and customize it using own team.

## Resources 
- [OpenStreetMap](www.openstreetmap.org) (OSM) data 
  - [Nominatim](https://nominatim.openstreetmap.org/ui/search.html): Geocoding API for searching OSM data
  - [Geofabrik](https://download.geofabrik.de/): OSM Data Extracts updated Daily (e.g. per Country data)
  - [OSMnx](https://osmnx.readthedocs.io/en/stable) Python library to download geospatial features from OSM
  - [Photon](https://photon.komoot.io/) a search-as-you-type Open-Source geocoder with a free API
  - [Omniscale](https://maps.omniscale.com/en/) is a German Company providing WMS and tile services based on OSM data
  - [osmosis, osmconvert, osmfilter](https://wiki.openstreetmap.org/wiki/Osmfilter#Download) complex, lightweight and specialized command line tool to filter OSM data files
- [Leafletjs](https://leafletjs.com/): Lightweight, provider-agnostic, Open-Source JS library.
- [OSRM](https://project-osrm.org/) Modern C++ routing engine for shortest paths in road networks
- [Location Data APIs](https://datarade.ai/data-categories/restaurant-location-data/apis)
- Fee-based:
    - [Google Maps Platform](https://mapsplatform.google.com/pricing/) 
    - [geoapify](https://www.geoapify.com/pricing/): Free tier up to 3k credits per day; Premium tiers are charged monthly, not usage based. (Based on Open-Source data such as OSM)
    - [Graphhopper](https://www.graphhopper.com/) Provies two Open-Source Libraries: jsprit (Metaheuristics for TSP and VRP in Java) and [Routing Engine](https://github.com/graphhopper/graphhopper) for OSM. To have access to all APIs, premium tiers are charged monthly, not usage based.
        - [GraphHopper Navigation Example for Android ](https://github.com/graphhopper/graphhopper-navigation-example)
    - MapBox, MapTiler


## So far
- Google Maps API (Placement) used for nearby-me query 
- Data Problem and what is required:
    - GPS location of user
    - geo data of establishments
    - Preview Image (Google Maps Rezensionen)
    - Google Maps rating
    - Addresse, Telefonnummer, Website, E-Mail, Kategorie-Tags (E.g. Einrichtung, Essen, Lieferung von Mahlzeiten, Sehenswürdigkeit, health)
- Aktuelle Mängel:
    - Google Tags zu ungenau (Hotel, Care, Clinic)
    - Too many API requests, more caching and own db utilization needed
    - Category Filtering does not deliver result (maybe because of opening hours, but no feedback is given)




#### Glossary
- **Geocoding**: Process of converting address or place name to geographic coordinates
- **Reverse Geocoding**: Process of converting a location as described by geographic coordinates to a human-readable address or place name
- **Coordinate Formats**: 
    - Decimal degrees (DD): 41.40338, 2.17403;
    - Degrees, minutes, and seconds (DMS): 41°24'12.2"N 2°10'26.5"E
- **Traveling Salesman Problem (TSP)**: Finding shortest route for a single vehicle visiting all locations once and returning to the origin.
- **Vehicle Routing Problem (VRP)**: Like TSP but with multiple vehicles, routes and additional constraints (vehicle capacity, delivery schedules etc.)
- **Tile Map Service (TMS)** : Specification providing access to cartographic maps of geo-referenced data. A tile map is a map displayed by joining many images or vector data files. Instead, Web Map Service (WMS) typically uses a single large image. Nowadays more and more vector tiles than raster formats are used.
- **GPX (GPS Exchange Format)** is an XML schema designed as a common GPS data format, containing waypoints, tracks and routes.
- **PBF (Protocol buffer Binary Format)** binary file format for osm data
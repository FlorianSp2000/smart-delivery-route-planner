# smart-delivery-route-planner
Intelligent navigation and discovery platform for delivery services, integrating interactive maps, points of interest (POIs), and advanced route optimization to streamline delivery operations.


## Requirements on the Application
- Route map with Points of Interest (POI), including restaurants and (Home) Addresses
- Street map has to be up-to-date and free to use commercially
- Area of focus is Germany
- Efficient Shortest Path Computation
- Depiction of User Position through GPS data
- Has to be easily integrable on mobile devices

The common approach consists of using open data sources like OpenStreetMap, supplement it with data from private vendors and customize it using own team.

## Resources 
- [OpenStreetMap](www.openstreetmap.org) (OSM) data 
  - [Nominatim](https://nominatim.openstreetmap.org/ui/search.html): Geocoding API for searching OSM data
  - [Geofabrik](https://download.geofabrik.de/): OSM Data Extracts updated Daily (e.g. per Country data)
  - Python library [OSMnx](https://osmnx.readthedocs.io/en/stable)
  - [Photon](https://photon.komoot.io/) a search-as-you-type Open-Source geocoder with a free API
  - [Omniscale](https://maps.omniscale.com/en/) is a German Company providing WMS and tile services based on OSM data
- Leafletjs: Lightweight, provider-agnostic, Open-Source JS library.
- Licensed Map Data:
- Routing Engines: OSRM
- Fee-based
    - [Google Maps Platform](https://mapsplatform.google.com/pricing/) 
    - [geoapify](https://www.geoapify.com/pricing/): Free tier up to 3k credits per day; Premium tiers are charged monthly, not usage based. (Based on Open-Source data such as OSM)
    - [Graphhopper](https://www.graphhopper.com/) Provies two Open-Source Libraries: jsprit (Metaheuristics for TSP and VRP in Java) and [Routing Engine](https://github.com/graphhopper/graphhopper) for OSM. To have access to all APIs, premium tiers are charged monthly, not usage based.
        - [GraphHopper Navigation Example for Android ](https://github.com/graphhopper/graphhopper-navigation-example)







#### Glossary
- Geocoding: Process of converting address or place name to geographic coordinates
#
- Reverse Geocoding: Process of converting a location as described by geographic coordinates to a human-readable address or place name
- Coordinate Formats: 
    - Decimal degrees (DD): 41.40338, 2.17403;
    - Degrees, minutes, and seconds (DMS): 41°24'12.2"N 2°10'26.5"E
- Traveling Salesman Problem (TSP): Finding shortest route for a single vehicle visiting all locations once and returning to the origin.
- Vehicle Routing Problem (VRP): Like TSP but with multiple vehicles, routes and additional constraints (vehicle capacity, delivery schedules etc.)
- Tile Map Service (MTS) : Specification providing access to cartographic maps of geo-referenced data. A tile map is a map displayed by joining many images or vector data files. Instead, Web Map Service (WMS) typically uses a single large image. Nowadays more and more vector tiles than raster formats are used.
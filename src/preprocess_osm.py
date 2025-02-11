import subprocess
from typing import List

def extract_street_map_from_osm_pbf(input_pbf: str, output_osm: str, highway_types: List[str] = None) -> None:
    """
    Extracts street data from an OSM PBF file using Osmosis and saves it as an OSM XML file.

    Args:
    - input_pbf (str): Path to the input OSM PBF file.
    - output_osm (str): Path to the output OSM XML file.
    - highway_types (List[str], optional): List of highway types to include (default: common road types).
    
    Returns:
    - None
    """

    if highway_types is None:
        highway_types = [
            "motorway", "motorway_link", "trunk", "trunk_link", 
            "primary", "primary_link", "secondary", "secondary_link", 
            "tertiary", "tertiary_link", "unclassified", "residential"
        ]

    # Format the highway filter string
    highway_filter = ",".join(highway_types)

    # Define the Osmosis command as a list
    command = [
        "osmosis",
        "--rbf", input_pbf,  # Read input PBF file
        "--tf", "reject-relations",  # Ignore relations
        "--tf", "accept-ways", f"highway={highway_filter}",  # Accept specific highway types
        "--tf", "reject-ways", "highway=construction",  # Reject certain highway types
        "--used-node",  # Include nodes referenced by accepted ways
        "--lp",  # Use low priority for processing
        "--write-xml", output_osm  # Write output as OSM XML
    ]

    # Execute the command using subprocess
    try:
        subprocess.run(command, check=True)
        print(f"Successfully extracted streets from {input_pbf} to {output_osm}")
    except subprocess.CalledProcessError as e:
        print(f"Error while running Osmosis: {e}")

# Example usage:
# extract_street_map_from_osm_pbf("hamburg-latest.osm.pbf", "hamburg-latest-streets.osm")

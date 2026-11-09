import os
import sys
from pathlib import Path

import numpy as np
import requests

from depot.maps import MapGen

print(f"Working directory: {os.getcwd()}")

# Download the .osm.pbf file we need
osmpbf_path = Path("data") / "malaysia-singapore-brunei-latest.osm.pbf"
if not os.path.exists(osmpbf_path):
    url = "https://download.geofabrik.de/asia/malaysia-singapore-brunei-latest.osm.pbf"
    print("Downloading", url, flush=True)
    resp = requests.get(url)
    with open(osmpbf_path, "wb") as f:
        f.write(resp.content)

"""
Singapore's admin boundaries (per https://wiki.openstreetmap.org/wiki/Singapore/Boundaries):
- borough: Region (ADM5)
- suburb: Planning area (ADM6)
- neighbourhood: Subzone (ADM7)
- HDB admin boundaries - proposed (de facto use unclear):
    - town: HDB Town
    - quarter: HDB Neighbourhood/estate
"""

# Set up MapGen object
map_generator = MapGen(
    city="SIN",
    outputdir="cities",
    bbox=[103.578442, 1.155904, 104.112653, 1.489401],
    osmpbf=str(osmpbf_path),
    buildings_geojson=r"cities/SIN/in/buildings.geojson",
    building_index_filter_size=10,
    building_tile_filter_size=10,
    building_index_simplification=1,
    building_tile_simplification=1,
    ncores=8,
    RAM=24,
    cleanup_files=False, # yeah that's true I set this to False :)
    create_building_foundations=True,
    color_military_like_aerodrome=False,
    reprocess_bathymetry_data=True,
    cities=["city"],
    suburbs=["town", "suburb"],
    neighborhoods=["neighbourhood", "quarter"],
    verb=False,
    # custom added configuration
    include_canals_drains=False,
    resolve_edu_overlaps=True,
    resolve_retail_overlaps=True,
)

# If you want to run each method individually:
map_generator.extract_base_data()
map_generator.process_buildings()
map_generator.process_roads_and_aeroways()
map_generator.generate_pmtiles()
map_generator.add_labels()

# Or just run them all consecutively:
# map_generator.run_all()

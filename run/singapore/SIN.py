import os
import sys

import numpy as np
import requests

from depot.maps import MapGen

# print(os.getcwd())

# Download the .osm.pbf file we need
if not os.path.exists("malaysia-singapore-brunei-latest.osm.pbf"):
    url = "https://download.geofabrik.de/asia/malaysia-singapore-brunei-latest.osm.pbf"
    print("Downloading", url, flush=True)
    resp = requests.get(url)
    with open("malaysia-singapore-brunei-latest.osm.pbf", "wb") as f:
        f.write(resp.content)

# Set up MapGen object
obj = MapGen(
    city="SIN",
    outputdir="SIN/TEMP1",
    bbox=[103.578442, 1.155904, 104.112653, 1.489401],
    osmpbf="malaysia-singapore-brunei-latest.osm.pbf",
    buildings_geojson=r"SIN/in/buildings.geojson",
    building_index_filter_size=10,
    building_tile_filter_size=10,
    building_index_simplification=1,
    building_tile_simplification=1,
    ncores=8,
    RAM=24,
    cleanup_files=False,
    create_building_foundations=True,
    color_military_like_aerodrome=False,
    reprocess_bathymetry_data=True, 
    cities=["city", "borough"], # TODO CHANGE
    suburbs=["town", "suburb"],
    neighborhoods=["neighbourhood"],
    verb=False,
)

# If you want to run each method individually:
obj.extract_base_data()
obj.process_buildings()
obj.process_roads_and_aeroways()
obj.generate_pmtiles()
obj.add_labels()

# Or just run them all consecutively:
# obj.run_all()

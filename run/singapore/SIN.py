import os
import sys

import numpy as np
import requests

from depot.maps import MapGen

# print(os.getcwd())

# Download the .osm.pbf file we need
if not os.path.exists("data" / "malaysia-singapore-brunei-latest.osm.pbf"):
    url = "https://download.geofabrik.de/asia/malaysia-singapore-brunei-latest.osm.pbf"
    print("Downloading", url, flush=True)
    resp = requests.get(url)
    with open("data" / "malaysia-singapore-brunei-latest.osm.pbf", "wb") as f:
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
obj = MapGen(
    city="SIN",
    outputdir="SIN/TEMP1",
    bbox=[103.578442, 1.155904, 104.112653, 1.489401],
    osmpbf="malaysia-singapore-brunei-latest.osm.pbf",
    buildings_geojson=r"cities/SIN/in/buildings.geojson",
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
obj.extract_base_data()
obj.process_buildings()
obj.process_roads_and_aeroways()
obj.generate_pmtiles()
obj.add_labels()

# Or just run them all consecutively:
# obj.run_all()

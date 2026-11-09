import os
import sys

import numpy as np

from depot.demand import DemandData

# default singapore config
config = {"bbox": [103.578442, 1.155904, 104.112653, 1.489401]}

sin = DemandData("cities/SIN/in/demand_data.json", "SIN", outputdir="cities/SIN/out")


sin.print_stats()

sin.save("cities/SIN/out/demand_data.json")

sin.create_config(
    name="Singapore (WIP)",
    bbox=config["bbox"],
    description="Build a world-class transit system across the initialism-loving island city-state.",
    creator="zeepheru",
    version="0.1.2",
    country="SG",
)

# this produces `description.md`, useful as a starting point for the map description on Railyard.
sin.create_description(
    "singapore",
    # "this is line 2 of the description",
    [
        """<li><a href="https://github.com">github.com</a></li>""",
        """<li><a href="https://github.com/Subway-Builder-Modded/depot">Depot</a></li>""",
    ],
    # "this is another description line",
    [
        """<li><a href="https://lehd.ces.census.gov/data/">This is not actually the link</a></li>"""
    ],
)

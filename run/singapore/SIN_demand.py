import os
import sys

import numpy as np

from depot.demand import DemandData

config = {"bbox": [103.578442, 1.155904, 104.112653, 1.489401]}

sin = DemandData("SIN/in/demand_data.json", "SIN")


sin.print_stats()

sin.save("SIN/demand_data.json")

sin.create_config(
    name="Singapore (TEST)",
    bbox=config["bbox"],
    description="Singapore.",
    creator="zeepheru",
    version="0.1.1",
    country="SG",
)

sin.create_description(
    "singapore",
    "this is line 2 of the description",
    [
        """<li><a href="https://github.com">github.com</a></li>""",
        """<li><a href="https://github.com/Subway-Builder-Modded/depot">Depot</a></li>""",
    ],
    "this is another description line",
    [
        """<li><a href="https://lehd.ces.census.gov/data/">This is not actually the link</a></li>"""
    ],
)

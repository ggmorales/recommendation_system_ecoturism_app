# Usage:
# It retrieves the QUALITY description of a given NATURA2000 site code. This script is then use to add this description to the 5 nearest ENP in case they are a NATURA site.

import csv
import os

current_dir = os.getcwd()   


def site_quality(site_code):
    csv_file = os.path.join(current_dir, "data", "NATURA_ubicaciones.csv")
    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            if row["site_code"] == site_code:
                return row["QUALITY"]
    return None

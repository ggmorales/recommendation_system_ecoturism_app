# Usage:
# Obtains the nearest REDNATURA2000 site from the user coordinates, returning all info from that site.

import csv
import math


def calculate_distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)


def search_nearest_coordinates(file_path, latitude, longitude):
    nearest_row = None
    min_distance = float("inf")

    with open(file_path, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file, delimiter=";")
        for row in csv_reader:
            row_latitude = float(row["site_latitude"])
            row_longitude = float(row["site_longitude"])
            distance = calculate_distance(
                latitude, longitude, row_latitude, row_longitude
            )

            if distance < min_distance:
                min_distance = distance
                nearest_row = row

    return nearest_row

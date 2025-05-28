import json
import math


def haversine_distance(lat1, lon1, lat2, lon2):
    # Radio de la Tierra
    R = 6371.0

    # Convertir grados a radianes
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Fórmula de Haversine
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


def search_nearest_ENP_sites(geojson_files, latitude, longitude, n=5):
    nearest_sites = []

    for input_file in geojson_files:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for feature in data["features"]:
            centroid = feature["properties"]["centroid"]
            site_name = feature["properties"]["SITE_NAME"]
            site_code = feature["properties"]["SITE_CODE_"]
            odesignate = feature["properties"]["ODESIGNATE"]
            distance = haversine_distance(latitude, longitude, centroid[0], centroid[1])

            nearest_sites.append(
                {
                    "SITE_NAME": site_name,
                    "ODESIGNATE": odesignate,
                    "SITE_CODE_": site_code,
                    "DISTANCE": distance,
                    "SITE_URL": f"https://biodiversity.europa.eu/sites/natura2000/{site_code}",
                }
            )

    nearest_sites.sort(key=lambda x: x["DISTANCE"])
    return nearest_sites[:n]


# # Ejemplo de uso
# input_files = ["ENP_PB_location.geojson", "ENP_other_location.geojson"]
# latitude = 42.07
# longitude = -7.83

# nearest_sites = search_nearest_ENP_sites(input_files, latitude, longitude)
# print("Los Espacios Naturales Protegidos más cercanos son:")
# for i, site in enumerate(nearest_sites, start=1):
#     print(f"{i}. {site['SITE_NAME']} con la designación {site['ODESIGNATE']}")

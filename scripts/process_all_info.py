import json
import os
from flora_images import extract_images
from get_routes_komoot import get_routes
from search_ENP import search_nearest_ENP_sites
from search_especies import search_species
from search_habitat import search_habitats
from match_especies_eidos_id import (
    find_most_similar_species,
)
from REDNATURA_site_code import (
    search_nearest_coordinates,
)
from search_NATURAsite_code import (
    search_site_code_in_multiple_csv,
)

current_dir = os.getcwd()


class DataSource:
    def __init__(self, name, url, file):
        self.name = name
        self.url = url
        self.file = file


class DataProcessor:
    def __init__(self, user_coordinates):
        self.user_coordinates = user_coordinates
        self.results = {}
        self.site_info = None
        self.species_info = {}
        self.habitats_info = []
        self.routes_info = ""
        self.ENP_info = None
        self.species_sheetinfo = {}
        self.flora_info = {}

    def process_data(self):
        site_code, site_name = self._search_coordinates()
        if site_code:
            self.site_info = {
                "site_code": site_code,
                "site_name": site_name,
                "site_url": f"https://biodiversity.europa.eu/sites/natura2000/{site_code}",
            }
            self._search_site_code_data(site_code)
        else:
            self.site_info = {"error": "No se encontró información de sitios cercanos."}

        self._get_routes_info()

        return {
            "results": self.results,
            "site_info": self.site_info,
            "species_info": self.species_info,
            "habitats_info": self.habitats_info,
            "routes_info": self.routes_info,
            "ENP_info": self.ENP_info,
            "species_sheetinfo": self.species_sheetinfo,
            "flora_info": self.flora_info,
        }

    def _search_coordinates(self):
        latitude, longitude = map(float, self.user_coordinates.split(","))
        geojson_files = [
            os.path.join(current_dir, "data", "ENP_PB_location.geojson"),
            os.path.join(current_dir, "data" ,"ENP_C_location.geojson"),
        ]
        nearest_ENP_sites = search_nearest_ENP_sites(geojson_files, latitude, longitude)
        if nearest_ENP_sites:
            self.ENP_info = nearest_ENP_sites
            first_enp = nearest_ENP_sites[0]
            self.flora_info = extract_images(
                first_enp,
                os.path.join(current_dir, "data", "coincidencias.json"),
                os.path.join(current_dir, "data", "flora_espacio_natural.json"),
                os.path.join(current_dir, "data", "imagenes_flora"),
            )

        else:
            self.ENP_info = {
                "error": "No se encontró información de Espacios Naturales Protegidos cercanos."
            }

        csv_path = os.path.join(current_dir, "data", "NATURA_ubicaciones.csv")
        result = search_nearest_coordinates(csv_path, latitude, longitude)

        if result:
            return result["site_code"], result["site_name"]
        return None, None

    def _search_site_code_data(self, site_code):
        csv_paths = [
            os.path.join(current_dir, "data", "NATURA_species.csv"),
            os.path.join(current_dir, "data", "NATURA_habitat.csv"),
        ]
        results = search_site_code_in_multiple_csv(csv_paths, site_code)

        self.species_info = search_species(results)
        all_species = (
            self.species_info["Aves"]["names"]
            + self.species_info["Mamíferos"]["names"]
            + self.species_info["Reptiles"]["names"]
            + self.species_info["Invertebrados"]["names"]
        )
        self.species_sheetinfo = find_most_similar_species(all_species)
        self.habitats_info = search_habitats(results)

    def _get_routes_info(self):
        json_file_path = get_routes(self.user_coordinates)
        self.routes_info = self._read_json_file(json_file_path)

    def _read_json_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)


def execute_process(user_coordinates):
    processor = DataProcessor(user_coordinates)
    return processor.process_data()

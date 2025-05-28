import csv
import os
from collections import defaultdict


current_dir = os.getcwd()


def search_species(results):
    species_group_count = {"Birds": 0, "Mammals": 0, "Reptiles": 0, "Invertebrates": 0}
    species_names = {"Birds": [], "Mammals": [], "Reptiles": [], "Invertebrates": []}

    species_categories = {}
    category_count = defaultdict(lambda: defaultdict(list))

    species_group_translation = {
        "Birds": "Aves",
        "Mammals": "Mamíferos",
        "Reptiles": "Reptiles",
        "Invertebrates": "Invertebrados",
    }

    output = {}

    if results:
        with open(
            os.path.join(current_dir, "data", "IUCN_species.csv"),
            mode="r",
            encoding="utf-8-sig",
        ) as file:  # Usar utf-8-sig para manejar BOM
            csv_reader = csv.DictReader(file, delimiter=";")
            for row in csv_reader:
                species_name = row["scientificName"]
                category = row["redlistCategory"]
                species_categories[species_name] = category

        for csv_path, rows in results.items():
            category = os.path.basename(csv_path).split("_")[-1].split(".")[0]
            for row in rows:
                species_group = row.get("species_group")
                species_name = row.get("species_name")
                if species_group in species_group_count:
                    species_group_count[species_group] += 1
                    species_names[species_group].append(species_name)

        for group, count in species_group_count.items():
            names_list = species_names[group]
            translated_group = species_group_translation[group]
            output[translated_group] = {
                "count": count,
                "names": names_list,
                "categories": {},
            }

            # Comprobar la categoría de cada especie en el archivo UICN.csv
            for name in species_names[group]:
                if name in species_categories:
                    category = species_categories[name]
                else:
                    category = "Desconocida"

                if category not in output[translated_group]["categories"]:
                    output[translated_group]["categories"][category] = []
                output[translated_group]["categories"][category].append(name)
    else:
        output["error"] = "No se encontró el site_code en los archivos proporcionados."

    return output

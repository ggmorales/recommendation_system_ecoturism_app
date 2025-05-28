# Usage:
# Given the list of the species present in the nearest REDNATURA2000 site, searches and matches the species name from REDNATURA to the most similar in EIDOS data. When matched, it retrieves the corresponding EIDOS ID so the URL to the IEPBN website for the infosheets is constructed.

import pandas as pd
import os

current_dir = os.getcwd()


def find_most_similar_species(species_list):
    file_path = os.path.join(current_dir, "data", "EIDOS_species.csv")
    df = pd.read_csv(file_path, sep=";", dtype=str)
    results = {}
    for species in species_list:
        exact_match = df[df["nombre_aceptado"] == species]
        if not exact_match.empty:
            idtaxon = exact_match.iloc[0]["idtaxon"]
            results[species] = {
                "idtaxon": idtaxon,
                "url": f"https://iepnb.es/areas-tematicas/especies-silvestres/eidos/{idtaxon}",
            }
        else:
            exact_match_dataset = df[df["nombre_en_dataset"] == species]
            if not exact_match_dataset.empty:
                idtaxon = exact_match_dataset.iloc[0]["idtaxon"]
                results[species] = {
                    "idtaxon": idtaxon,
                    "url": f"https://iepnb.es/areas-tematicas/especies-silvestres/eidos/{idtaxon}",
                }
            else:
                similar_rows = df[
                    df["nombre_aceptado"].str.startswith(species, na=False)
                ]
                if not similar_rows.empty:
                    most_similar_row = similar_rows.iloc[0]
                    idtaxon = most_similar_row["idtaxon"]
                    results[species] = {
                        "idtaxon": idtaxon,
                        "url": f"https://iepnb.es/areas-tematicas/especies-silvestres/eidos/{idtaxon}",
                    }
                else:
                    results[species] = {"idtaxon": None, "url": None}
    return results

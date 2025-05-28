# Usage:
# This scripts searches for the species and habitats with the given code of the nearest site NATURA2000

import csv


def search_site_code_in_csv(file_path, site_code):
    results = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file, delimiter=";")
        for row in csv_reader:
            if row.get("site_code") == site_code:
                results.append(row)
    return results


def search_site_code_in_multiple_csv(file_paths, site_code):
    all_results = {}
    for file_path in file_paths:
        results = search_site_code_in_csv(file_path, site_code)
        if results:
            all_results[file_path] = results
    return all_results

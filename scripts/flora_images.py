import json
import os


def extract_site_name(site_info):
    """Recibe un diccionario con información de un sitio y devuelve el SITE_NAME."""
    if "SITE_NAME" in site_info:
        return site_info["SITE_NAME"]
    else:
        return None


def search_match(name, json_path):
    """Busca un nombre en las claves del diccionario y devuelve su valor asociado."""
    with open(json_path, "r", encoding="utf-8") as file:
        matches_dict = json.load(file)
    return matches_dict.get(name, None)


def search_images(plants_list, images_folder_path):
    """Busca imágenes en la carpeta para cada planta y devuelve un diccionario con nombre y URL."""

    # Get image names without extension
    image_names = [
        os.path.splitext(name)[0]
        for name in os.listdir(images_folder_path)
        if name.endswith((".jpg"))
    ]

    result = {}

    for plant_name in plants_list:
        image_url = None

        # 1. Exact match
        if plant_name in image_names:
            image_url = f"{images_folder_path}\\{plant_name}.jpg"

        # 2. If the name has more than three words, do not search for an image
        elif plant_name.count(" ") >= 3:
            image_url = None

        # 3. Partial match (first two words)
        else:
            words = plant_name.split(" ")
            if len(words) >= 2:
                start = " ".join(words[:2])
                matches = [name for name in image_names if name.startswith(start)]
                image_url = (
                    f"{images_folder_path}\\{matches[0]}.jpg" if matches else None
                )

        result[plant_name] = image_url

    return result


def extract_images(site_info, json_path1, json_path2, images_folder_path):
    site_name = extract_site_name(site_info)
    space_name = search_match(site_name, json_path1)
    if space_name is not None:
        plants_list = search_match(space_name, json_path2)
        result = search_images(plants_list, images_folder_path)
        return result
    else:
        return print("No hay datos de flora para el espacio natural seleccionado")

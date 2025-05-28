import json  
import os

current_dir = os.getcwd()


def load_json_files(): 
    def load_json_file(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    routes_info = load_json_file(os.path.join(current_dir, "reports", "report_routes_info.json"))
    ENP_info = load_json_file(os.path.join(current_dir, "reports", "report_ENP_info.json"))
    flora_info = load_json_file(os.path.join(current_dir, "reports", "report_flora_info.json"))
    habitats_info = load_json_file(os.path.join(current_dir, "reports", "report_habitats_info.json"))
    species_info = load_json_file(os.path.join(current_dir, "reports", "report_species_info.json"))

    return routes_info, ENP_info, flora_info, habitats_info, species_info



def read_prompt(file_name):
        prompts_folder = os.path.join(current_dir, "prompts")
        file_path = os.path.join(prompts_folder, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

def get_perfiles():
    routes_info, ENP_info, flora_info, habitats_info, species_info = load_json_files()
    flora_keys = list(flora_info.keys()) if flora_info else []
        
    perfiles = {
        "Familias o Grupos de amigos": read_prompt("familiar.md").format(
            ENP_info=ENP_info,
            species_info=species_info,
            routes_info=routes_info
        ),
        "Aventureros o Deportistas": read_prompt("deportistas.md").format(
            ENP_info=ENP_info,
            routes_info=routes_info
        ),
        "Ornitólogos, Biólogos o Amantes de la Naturaleza": read_prompt("naturalistas.md").format(
            ENP_info=ENP_info,
            habitats_info=habitats_info,
            species_info=species_info,
            flora_keys=flora_keys
        )
    }

    return perfiles


def get_impact():
    _, _, flora_info, habitats_info, species_info = load_json_files()
    flora_keys = list(flora_info.keys()) if flora_info else []

    impacto_ambiental = read_prompt("impacto_ambiental.md").format(
        habitats_info=habitats_info,
        species_info=species_info,
        flora_keys=flora_keys,

    )
    return impacto_ambiental

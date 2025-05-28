import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options

"""
Pasos del proceso: 
1. Entra en "https://www.komoot.com/es-es/discover/rutas-senderismo
2. Hace click en la barra de búsqueda
3. Hace mete el input del lugar deseado
4. Realiza la búsqueda
5. Abre y obtiene la nueva URL con las rutas de la localización
6. Se formatea la información de forma legible en un .md
7. Se descarga el .md en la ruta seleccionada
"""

current_dir = os.getcwd()

def extract_routes_info(routes_text, new_url):
    lines = routes_text.split("\n")
    routes_info = {"info_url": new_url, "total": lines[0], "routes": []}

    i = 0
    while i < len(lines):
        if "Map data © OpenStreetMap contributors" in lines[i]:
            i += 1
            ruta_info = []
            while i < len(lines) and "Ver" not in lines[i]:
                ruta_info.append(lines[i])
                i += 1
            if i < len(lines) and "Ver" in lines[i]:
                i += 1
                route = {}
                if len(ruta_info) >= 9:
                    if len(ruta_info) < 10:
                        route = {
                            "Categoría": ruta_info[0],
                            "Valoración (estrellas)": "-",
                            "Nº valoraciones": "-",
                            "Personas que han hecho la ruta": ruta_info[1],
                            "Nombre": ruta_info[2],
                            "Duración": ruta_info[3],
                            "Longitud": ruta_info[4],
                            "Metros de ascenso": ruta_info[5],
                            "Metros de descenso": ruta_info[6],
                            "Descripción": " ".join(ruta_info[7:]),
                        }
                    else:
                        route = {
                            "Categoría": ruta_info[0],
                            "Valoración (estrellas)": f"{ruta_info[1]}⭐",
                            "Nº valoraciones": ruta_info[2],
                            "Personas que han hecho la ruta": ruta_info[3],
                            "Nombre": ruta_info[4],
                            "Duración": ruta_info[5],
                            "Longitud": ruta_info[6],
                            "Metros de ascenso": f"{ruta_info[7]}↗️",
                            "Metros de descenso": f"{ruta_info[8]} ↘️",
                            "Descripción": " ".join(ruta_info[9:]),
                        }
                    routes_info["routes"].append(route)
        else:
            i += 1

    return routes_info


def get_routes(coordinates):
    edge_options = Options()
    edge_options.add_argument("--headless")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--window-size=1920,1080")
    service = EdgeService(
        os.path.join(current_dir, "edgedriver_win64", "msedgedriver.exe")
    )
    driver = webdriver.Edge(service=service, options=edge_options)
    driver.get("https://www.komoot.com/es-es/discover/rutas-senderismo")
    time.sleep(1)

    # Deactivate cookies
    close_button = driver.find_element(
        By.CSS_SELECTOR, 'button[data-test-id="gdpr-banner-decline"]'
    )
    close_button.click()
    time.sleep(0.5)

    # Select search bar
    search_bar = driver.find_element(By.CLASS_NAME, "css-nk1i1k")
    search_bar.click()
    time.sleep(0.5)
    search_bar = driver.find_element(
        By.CSS_SELECTOR, 'input[data-test-id="discover-search"]'
    )
    search_bar.send_keys(Keys.CONTROL, "a")
    search_bar.send_keys(Keys.DELETE)
    time.sleep(0.5)

    # Search place
    search_bar.send_keys(coordinates)
    time.sleep(0.5)
    search_bar.send_keys(Keys.ENTER)
    time.sleep(3)

    new_url = driver.current_url
    print(f"URL de la nueva página: {new_url}")

    routes = driver.find_element(By.CSS_SELECTOR, 'div[data-test-id="search"]')
    routes_text = routes.text
    routes_info = extract_routes_info(routes_text, new_url)
    routes_info_json = json.dumps(routes_info, indent=4, ensure_ascii=False)

    output_path = f"rutas/rutas_{coordinates}"
    os.makedirs("rutas", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(routes_info_json)
        print(f"\nInformación de rutas guardada en JSON en: {output_path}")
        driver.quit()
        return output_path

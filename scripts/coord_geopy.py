from geopy.geocoders import Nominatim


def get_region_province(latitude, longitude):
    geolocator = Nominatim(user_agent="ecotourism")
    location = geolocator.reverse(f"{latitude}, {longitude}")
    parts = str(location).split(", ")
    ccaa = parts[-3]
    province = parts[-4]

    if ccaa in ["Navarra"]:
        ccaa = "Comunidad Foral de Navarra"
    elif ccaa in ["Asturias / Asturies"]:
        ccaa = "Principado de Asturias"
    elif ccaa in ["Euskadi"]:
        ccaa = "País Vasco"

    if ccaa in ["Cantabria"]:
        province = "Cantabria"
    elif ccaa in ["La Rioja"]:
        province = "La Rioja"
    elif ccaa in ["Principado de Asturias"]:
        province = "Asturias"
    elif ccaa in ["Comunidad de Madrid"]:
        province = "Madrid"
    elif ccaa in ["Región de Murcia"]:
        province = "Murcia"
    elif ccaa in ["Illes Balears"]:
        province = "Illes Balears"
    elif ccaa in ["Comunitat Valenciana"]:
        province = "Castellón/Castelló"

    return ccaa, province, location

import json
import os
import streamlit as st
from codecarbon import OfflineEmissionsTracker
from geopy.geocoders import Nominatim
from geopy.point import Point
from streamlit_geolocation import streamlit_geolocation
from process_all_info import execute_process
from llm_requests import generate_response
from tag import get_perfiles, get_impact
from rag import get_rag_response
from display_info import (
    display_enp_info,
    display_flora_info,
    display_habitats_info,
    display_routes_info,
    display_species_info,
)

# Configuración inicial del tracker
country_iso_code = "ESP"
region = "ESP"
cloud_provider = "gcp"
cloud_region = "europe-southwest1"
country_2letter_iso_code = "ES"
tracker = OfflineEmissionsTracker(
    country_iso_code=country_iso_code,
    region=region,
    cloud_provider=cloud_provider,
    cloud_region=cloud_region,
    country_2letter_iso_code=country_2letter_iso_code,
)
tracker.start()

current_dir = os.getcwd()

# Inicializar estados en session_state
if "report_generated" not in st.session_state:
    st.session_state.report_generated = False

if "environmental_report" not in st.session_state:
    st.session_state.environmental_report = None

if "translation" not in st.session_state:
    st.session_state.environmetal_report_translation = None

if "translation_language" not in st.session_state:
    st.session_state.environmental_report_language = None

if "profile_recommendation" not in st.session_state:
    st.session_state.profile_recommendation = None

if "recommendation_translation" not in st.session_state:
    st.session_state.recommendation_translation = None

if "recommendation_translation_language" not in st.session_state:
    st.session_state.recommendation_language = None

if "activity_response" not in st.session_state:
    st.session_state.law_analysis = None

if "activity_translation" not in st.session_state:
    st.session_state.law_translation = None

if "activity_translation_language" not in st.session_state:
    st.session_state.law_language = None

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Principal"

# Fondo y estilo
image = "https://i.pinimg.com/736x/9e/a7/ed/9ea7edced5c0c1cc1492aeac8635358f.jpg"
css_main = f"""
    <style>
        .stApp {{
            background-image: url({image});
            background-size: cover;
        }}
        .stApp > header {{
            background-color: transparent;
        }}
    </style>
"""
st.markdown(css_main, unsafe_allow_html=True)
st.markdown(css_main, unsafe_allow_html=True)

# CSS para los elementos select y expander
css_elements = """
    <style>
        div[data-testid="stExpander"] {
            background-color: white;
            color: black; # Expander content color
        }
        div[data-baseweb="select"] > div {
            background-color: white;
            color: gray;
        }
    </style>
"""

# Aplicar el CSS
st.markdown(css_elements, unsafe_allow_html=True)

image_sidebar = "https://img.freepik.com/fotos-premium/fondo-papel-pastel-verde-mar-oscuro_696657-203.jpg"
css_sidebar = """
<style>
    [data-testid=stSidebar] {
        background-color: #dbeddc;
    }
</style>
"""
st.markdown(css_sidebar, unsafe_allow_html=True)

logo_path = os.path.join(current_dir, "data", "logo.png")
st.image(logo_path)
st.write("\n\n")


# Función para cambiar pestaña activa
def set_active_tab(tab_name):
    st.session_state.active_tab = tab_name
    st.experimental_rerun()

# Crear sistema de navegación por pestañas usando st.tabs
tabs_list = [
    "**Principal**",
    "**Espacios Naturales Cercanos**",
    "**Fauna**",
    "**Flora**",
    "**Hábitats**",
    "**Todas las Rutas Cercanas**",
    "**Recomendaciones Personalizadas**",
    "**Impacto Ambiental**",
    "**Legislación**"
]
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(tabs_list)

# Actualizamos la pestaña activa según la que esté seleccionada
current_tab = None
for i, tab in enumerate([tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9]):
    if tab.id:
        current_tab = tabs_list[i]
        break

if current_tab and current_tab != st.session_state.active_tab:
    st.session_state.active_tab = current_tab

# Sidebar (siempre visible)
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0e6655 ;font-size: 25px;'>🌍🌿ECOTURISMO🌿🌍</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #0e6655 ;font-size: 15px;'>Ingrese sus coordenadas o pulse el botón de localización automática</h1>", unsafe_allow_html=True)
    manual_latitude = st.number_input("Latitud", format="%.6f")
    manual_longitude = st.number_input("Longitud", format="%.6f")
    st.write("\n")
    location = streamlit_geolocation()
    auto_latitude = None
    auto_longitude = None
    if location:
        auto_latitude = location["latitude"]
        auto_longitude = location["longitude"]
        if auto_latitude is not None and auto_longitude is not None:
            st.write(
                f"Coordenadas obtenidas automáticamente: Latitud {auto_latitude}, Longitud {auto_longitude}"
            )
        else:
            st.write("")
            
    else:
        st.write("No se pudo obtener la ubicación automáticamente.")
    latitude = manual_latitude if manual_latitude != 0 else auto_latitude
    longitude = manual_longitude if manual_longitude != 0 else auto_longitude
    geolocator = Nominatim(user_agent="ecotourdirggsfmpnavhwaa")
    if latitude is not None and longitude is not None:
        location_point = Point(latitude, longitude)
        direction = geolocator.reverse(location_point)
        st.write("Las coordenadas corresponden con la dirección:")
        st.write(direction)
    if not st.session_state.report_generated:
        generate_report = st.button("Generar reporte")

# Generar reporte y almacenar en session_state
if (
    not st.session_state.report_generated
    and "generate_report" in locals()
    and generate_report
):
    if latitude is not None and longitude is not None:
        user_coordinates = f"{latitude},{longitude}"
        with st.spinner(
            f"Generando reporte para las coordenadas: ({latitude}, {longitude})"
        ):
            results = execute_process(user_coordinates)
        if results:
            results["direction"] = str(direction)
            results["latitude"] = latitude
            results["longitude"] = longitude

            with open(os.path.join(current_dir,"reports","report_ENP_info.json"), "w", encoding="utf-8") as f:
                json.dump(results["ENP_info"], f, ensure_ascii=False)

            with open(os.path.join(current_dir,"reports","report_species_info.json"), "w", encoding="utf-8") as f:
                json.dump(results["species_info"], f, ensure_ascii=False)

            with open(os.path.join(current_dir,"reports","report_flora_info.json"), "w", encoding="utf-8") as f:
                json.dump(results["flora_info"], f, ensure_ascii=False)

            with open(os.path.join(current_dir,"reports","report_habitats_info.json"), "w", encoding="utf-8") as f:
                json.dump(results["habitats_info"], f, ensure_ascii=False)

            with open(os.path.join(current_dir,"reports","report_routes_info.json"), "w", encoding="utf-8") as f:
                json.dump(results["routes_info"], f, ensure_ascii=False)
            st.session_state.report_results = results
            st.session_state.report_generated = True
    else:
        st.write("Por favor, ingrese unas coordenadas válidas.")

# Obtener datos para las funciones
perfiles = get_perfiles()
impacto_ambiental = get_impact()
idiomas = ["Gallego", "Catalán", "Euskera", "Castellano"]

def translate_text(language, report_type, language_key, response_key, translation_key):
    if st.button(f"{report_type} en {language}"):
        with st.spinner(f"Traduciendo al {language}..."):
            st.session_state[language_key] = language
            role = "Eres un experto en traducción de textos."
            prompt = f"Traduce el siguiente texto palabra por palabra al {language}: {st.session_state[response_key]}"
            translation = generate_response(role, prompt)

            if translation:
                st.session_state[translation_key] = translation
            else:
                st.error("Hubo un problema al procesar la traducción.")

# Contenido principal según la pestaña
with tab1:  # Principal
    st.markdown("<h1 style='text-align: center; color: #0e6655 ;'>Bienvenido a la Aplicación de Ecoturismo</h1>", unsafe_allow_html=True)
    st.write("\n")
    st.markdown("<p style='text-align: center; color: #0e6655 ; font-size: 17px;'>La <b>APP de ECOTURISMO</b> te permite conocer cuales son los <b>espacios naturales</b> más cercanos a tu ubicación, así como brindarte información sobre <b>fauna</b>, <b>flora</b>, <b>hábitats</b> y <b>rutas de senderismo</b> cercanas a tus coordenadas.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #0e6655 ; font-size: 17px;'>Además, puedes disponer de <b>recomendaciones personalizadas</b> para visitar estas zonas por perfil de usuario, un <b>reporte de impacto ambiental</b> de la zona, y también puedes informarte sobre si la actividad que vas a realizar está <b>regulada por la ley.</b>", unsafe_allow_html=True)
    st.write("\n")
    st.markdown("<h1 style='text-align: center; color: #0e6655 ;font-size: 30px;'>Instrucciones de uso</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #0e6655 ;'>📝</h2>", unsafe_allow_html=True)
    st.write("\n")
    st.markdown("""
    <p style='text-align: center; color: #0e6655; font-size: 16px;'>
    <b>Paso 1: </b> 
    Ingresa tus coordenadas en el panel lateral o utiliza la geolocalización automática.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align: center; color: #0e6655; font-size: 16px;'>
    <b>Paso 2: </b> Haz clic en 'Generar reporte' para obtener información detallada sobre el área.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align: center; color: #0e6655; font-size: 16px;'>
    <b>Paso 3: </b> Navega por las pestañas en la parte superior para explorar diferentes tipos de información.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align: center; color: #0e6655; font-size: 16px;'>
    <b>Paso 4: </b> Utiliza las tres secciones especializadas de la derecha para obtener recomendaciones personalizadas, informes de impacto ambiental y consultas sobre legislación.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    
    if not st.session_state.report_generated:
        st.warning("Para comenzar, ingresa tus coordenadas en el panel lateral y haz clic en 'Generar reporte'.")
    else:
        st.success("¡Reporte generado! Navega por las pestañas para explorar la información.")

if st.session_state.report_generated and st.session_state.report_results is not None:
    results = st.session_state.report_results
    
    with tab2:  # Espacios Naturales
        st.markdown("<h1 style='text-align: center; color: #0e6655 ;font-size: 40px;'>Espacios naturales más cercanos</h1>", unsafe_allow_html=True)
        st.write("\n")
        display_enp_info(results["ENP_info"])
        
    with tab3:  # Especies
        st.markdown("<h1 style='text-align: center; color: #0e6655 ;font-size: 40px;'>Fauna presente en la zona</h1>", unsafe_allow_html=True)
        st.write("\n")
        display_species_info(results["species_info"], results["species_sheetinfo"])
        
    with tab4:  # Flora
        st.markdown("<h1 style='text-align: center; color: #0e6655 ;font-size: 40px;'>Visor de Flora</h1>", unsafe_allow_html=True)
        st.write("\n")
        display_flora_info(results["flora_info"])
        
    with tab5:  # Hábitats
        st.markdown("<h1 style='text-align: center; color: #0e6655 ;font-size: 40px;'>Hábitats presentes en la zona</h1>", unsafe_allow_html=True)
        st.write("\n")
        display_habitats_info(results["habitats_info"])
        
    with tab6:  # Rutas
        st.markdown("<h1 style='text-align: center; color: #0e6655 ;font-size: 40px;'>Rutas de senderismo cercanas</h1>", unsafe_allow_html=True)
        st.write("\n")
        display_routes_info(results["routes_info"])
        
    with tab7:  # Recomendaciones
        st.markdown("<h1 style='text-align: center; color: #0e6655 ;font-size: 40px;'>Recomendación personalizada por perfil de usuario para visitar la zona</h1>", unsafe_allow_html=True)
        st.write("\n")
        perfil_seleccionado = st.selectbox("Selecciona un perfil:", list(perfiles.keys()))
        
        if st.button("Generar recomendación según perfil"):
            with st.spinner("Generando recomendación..."):
                role = "Eres un experto en recomendaciones de rutas de senderismo."
                prompt = perfiles[perfil_seleccionado]
                response = generate_response(role, prompt)
                
                if response:
                    st.session_state.recommendation_language = "Castellano"
                    st.session_state.profile_recommendation = response
                else:
                    st.error("Hubo un problema al procesar la solicitud.")
        
        if st.session_state.profile_recommendation:
            st.markdown(st.session_state.profile_recommendation)
            st.write("\n")
            st.write("### Opciones de traducción:")
            col1, col2, col3 = st.columns(3)
            with col1:
                translate_text("Gallego", "Recomendación", "recommendation_language", "profile_recommendation", "recommendation_translation")
            with col2:
                translate_text("Catalán", "Recomendación", "recommendation_language", "profile_recommendation", "recommendation_translation")
            with col3:
                translate_text("Euskera", "Recomendación", "recommendation_language", "profile_recommendation", "recommendation_translation")
        
            # Mostrar la traducción de la recomendación si existe
            if "recommendation_translation" in st.session_state and st.session_state.recommendation_translation and st.session_state.recommendation_language != "Castellano":
                st.write(f"### Traducción de la recomendación al {st.session_state.recommendation_language}:")
                st.markdown(st.session_state.recommendation_translation)
    
    with tab8:  # Impacto Ambiental
        st.markdown("<h1 style='text-align: center; color: #0e6655 ;font-size: 40px;'>Informe de Impacto Ambiental</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center ; color: #0e6655 ; font-size: 16px;'>Al pulsar el botón obtendrás información sobre el impacto ambiental potencial que podría tener cualquier daño causado por actividades humanas o desastres naturales en la zona.</p>", unsafe_allow_html=True)
        st.write("\n\n") 

        
        col1, col2, col3 = st.columns([1.3, 1, 1])
        with col2:
            if st.button("Generar informe"):
                with st.spinner("Generando informe de impacto ambiental..."):
                    role = "Eres un experto en impacto ambiental."
                    prompt = impacto_ambiental
                    response = generate_response(role, prompt)

                    if response:
                        st.session_state.environmental_report = response
                    else:
                        st.error("Hubo un problema al procesar la solicitud.")

        
        # Mostrar el informe si existe
        if st.session_state.environmental_report:
            st.markdown(st.session_state.environmental_report)
            st.write("\n")
            st.write("### Opciones de traducción:")
            col1, col2, col3 = st.columns(3)
            with col1:
                translate_text("Gallego", "Informe", "environmental_report_language", "environmental_report", "environmental_report_translation")
            with col2:
                translate_text("Catalán", "Informe", "environmental_report_language", "environmental_report", "environmental_report_translation")
            with col3:
                translate_text("Euskera", "Informe", "environmental_report_language", "environmental_report", "environmental_report_translation")
        
            # Mostrar la traducción del informe si existe
            if "environmental_report_translation" in st.session_state and st.session_state.environmental_report_translation and st.session_state.environmental_report_language != "Castellano":
                st.write(f"### Traducción del informe al {st.session_state.environmental_report_language}:")
                st.markdown(st.session_state.environmental_report_translation)
    
    with tab9:  # Legislación
        st.markdown("<h1 style='text-align: center; color: #0e6655 ;font-size: 47px;'>Ley 26/2007, del 23 de octubre, de Responsabilidad Medioambiental</h1>", unsafe_allow_html=True)
        st.write("## ¿Para qué sirve la ley?") 
        st.write("Establece un marco legal para prevenir y reparar los daños medioambientales causados por actividades económicas. Su objetivo es garantizar que quienes causan daños al medio ambiente asuman la responsabilidad y los costos asociados a su reparación.")
        st.write("## ¿Qué se entiende por daño medioambiental?")
        st.write("El cambio adverso y mensurable de un recurso natural o el perjuicio de un servicio de recursos naturales, afectando especies, hábitats, aguas, riberas de mares o ríos y suelo, tanto si se produce directa como indirectamente. Quedan incluidos en el concepto de daño aquellos daños medioambientales que hayan sido ocasionados por los elementos transportados por el aire.")
        st.write("## ¿Y si el daño no es causado por una actividad económica?")
        st.write("La ley de responsabilidad medioambiental no se aplicaría directamente, y dependiendo de la naturaleza del daño, podrían aplicarse otras normativas sectoriales.")
        st.write("## Quiero saber si una actividad económica concreta está regulada por la ley")
        
        actividad = st.text_input("Escribe el tipo de actividad económica que ha causado o podría causar el daño:", "")
        
        if st.button("Generar respuesta"):
            if actividad:
                with st.spinner("Analizando la actividad..."):
                    query = f"Actividad económica que causo el daño del usuario: {actividad}."
                    response = get_rag_response(query)
                    
                    if response:
                        st.session_state.law_analysis = response
                    else:
                        st.error("Hubo un problema al procesar la solicitud.")
            else:
                st.error("Por favor, ingresa una actividad económica.")
        
        # Mostrar la respuesta sobre la actividad si existe
        if st.session_state.law_analysis:
            st.markdown(st.session_state.law_analysis)
            
            st.write("\n")
            st.write("### Opciones de traducción:")
            col1, col2, col3 = st.columns(3)
            with col1:
                translate_text("Gallego", "Análisis", "law_language", "law_analysis", "law_translation")
            with col2:
                translate_text("Catalán", "Análisis", "law_language", "law_analysis", "law_translation")
            with col3:
                translate_text("Euskera", "Análisis", "law_language", "law_analysis", "law_translation")
            
            # Mostrar la traducción de la actividad si existe
            if "law_translation" in st.session_state and st.session_state.law_translation and st.session_state.law_language != "Castellano":
                st.write(f"### Traducción del análisis al {st.session_state.law_language}:")
                st.markdown(st.session_state.law_translation)
else:
    # Mostrar advertencia en todas las pestañas excepto la principal
    for tab in [tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9]:
        with tab:
            st.warning("Por favor, genera un reporte primero usando el botón en el panel lateral.")

emissions = tracker.stop()
print(f"Emissions: {emissions} kg CO₂eq")
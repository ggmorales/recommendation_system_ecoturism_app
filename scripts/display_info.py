import streamlit as st
import streamlit.components.v1 as components

from match_codes_for_description import site_quality


@st.fragment(run_every=3)
def display_habitats_info(habitats_info):
    if habitats_info is not None:
        classification = habitats_info["classification"]
        counts = habitats_info["counts"]

        # Crear una lista de opciones para el selectbox
        options = []
        for global_term, sub_terms in classification.items():
            options.append(global_term)
            for sub_term in sub_terms:
                options.append(f"{global_term} - {sub_term}")

        selected_option = st.selectbox(
            "Selecciona un hábitat para más información", options
        )

        if selected_option in classification:
            st.write(
                f"**{counts[selected_option]} Hábitats de {selected_option}**, de los cuales:"
            )
            for sub_term, habitats in classification[selected_option].items():
                st.write(f"- **{counts[sub_term]} {sub_term}**:")
                for habitat in habitats:
                    st.write(f"  - Código: `{habitat['code']}`, Nombre: {habitat['name']}")
        else:
            global_term, sub_term = selected_option.split(" - ")
            st.write(f"- **{counts[sub_term]} {sub_term}**:")
            for habitat in classification[global_term][sub_term]:
                st.write(f"  - Código: `{habitat['code']}`, Nombre: {habitat['name']}")
    else:
        st.markdown(
            "<h1 style='text-align: center; color: #0e6655 ;font-size: 18px;'>No hay datos de hábitats disponibles para este espacio natural.</h1>", unsafe_allow_html=True
            )

@st.fragment(run_every=3)
def display_species_info(species_info, species_sheetinfo):
    for group, data in species_info.items():
        st.write(f"#### {group} ({data['count']} especies)")
        for category, species_list in data["categories"].items():
            st.write(f"**Categoría:** {category}")
            selected_species = st.selectbox(
                "Selecciona una especie  de la lista para más información",
                species_list,
                placeholder="Especies disponibles",
            )
            with st.expander(selected_species):
                url = species_sheetinfo.get(selected_species, {}).get(
                    "url", "URL no disponible"
                )
                if url:
                    components.iframe(url, height=400, scrolling=True)


@st.fragment(run_every=3)
def display_routes_info(routes_info):
    for route in routes_info["routes"]:
        with st.expander(route["Nombre"]):
            st.write(f"**Categoría:** {route['Categoría']}")
            st.write(f"**Valoración (estrellas):** {route['Valoración (estrellas)']}")
            st.write(f"**Nº valoraciones:** {route['Nº valoraciones']}")
            st.write(
                f"**Personas que han hecho la ruta:** {route['Personas que han hecho la ruta']}"
            )
            st.write(f"**Duración:** {route['Duración']}")
            st.write(f"**Longitud:** {route['Longitud']}")
            st.write(f"**Metros de ascenso:** {route['Metros de ascenso']}")
            st.write(f"**Metros de descenso:** {route['Metros de descenso']}")
            st.write(f"**Descripción:** {route['Descripción']}")
    st.write(f"Total de rutas registradas por usuarios: {routes_info['total']}")
    st.write(f"Para más información sobre las rutas, visita: {routes_info['info_url']}")


@st.fragment(run_every=3)
def display_enp_info(ENP_info):
    if "error" in ENP_info:
        st.write(f"Error: {ENP_info['error']}")
    else:
        for enp in ENP_info:
            code = enp["SITE_CODE_"]
            quality = site_quality(code)
            with st.expander(f"**{enp['SITE_NAME']}**"):
                st.markdown(f"**Tipo de ENP:** {enp['ODESIGNATE']}")
                st.markdown(f"**Código:** {enp['SITE_CODE_']}")
                st.markdown(f"**Distancia:** {enp['DISTANCE']:.2f} km")
                if enp["ODESIGNATE"] == "Espacio Protegido Red Natura 2000":
                    st.markdown(f"**Descripción:** {quality}")
                    st.markdown(f"**Más información:** {enp['SITE_URL']}")


@st.fragment(run_every=3)
def display_flora_info(flora_info):
    if flora_info:
        plantas = list(flora_info.keys())
        selected_planta = st.selectbox(
            "Selecciona una especie de flora para ver su imagen", plantas
        )
        imagen_url = flora_info[selected_planta]
        if imagen_url:
            st.image(imagen_url, caption=selected_planta)
        else:
            st.write("Imagen no disponible")
    else:
        st.markdown(
            "<h1 style='text-align: center; color: #0e6655 ;font-size: 18px;'>No hay datos de flora disponibles para este espacio natural.</h1>", unsafe_allow_html=True
            )

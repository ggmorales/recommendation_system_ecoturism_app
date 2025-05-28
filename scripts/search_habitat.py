import os


def classify_habitats(codes):
    habitat_mapping = {
        "1110": "Bancos de arena cubiertos permanentemente por agua marina, poco profunda",
        "1120": "Praderas de Posidonia (Posidonion oceanicae)",
        "1130": "Estuarios",
        "1140": "Llanos fangosos o arenosos que no están cubiertos de agua cuando hay marea baja",
        "1150": "Lagunas costeras",
        "1160": "Grandes calas y bahías poco profundas",
        "1170": "Arrecifes",
        "1180": "Estructuras submarinas causadas por emisiones de gases",
        "1210": "Vegetación anual sobre desechos marinos acumulados",
        "1230": "Acantilados con vegetación de las costas atlánticas y bálticas",
        "1240": "Acantilados con vegetación de las costas mediterráneas con Limonium spp. endémicos",
        "1250": "Acantilados con vegetación endémica de las costas macaronésicas",
        "1310": "Vegetación anual pionera con Salicornia y otras especies de zonas fangosas o arenosas",
        "1320": "Pastizales de Spartina (Spartinion maritimae)",
        "1330": "Pastizales salinos atlánticos (Glauco-Puccinellietalia maritimae)",
        "1410": "Pastizales salinos mediterráneos (Juncetalia maritimae)",
        "1420": "Matorrales halófilos mediterráneos y termoatlánticos (Sarcocornetea fruticosi)",
        "1430": "Matorrales halonitrófilos (Pegano-Salsoletea)",
        "1510": "Estepas salinas mediterráneas (Limonietalia) (*)",
        "1520": "Vegetación gipsícola ibérica (Gypsophiletalia) (*)",
        "2110": "Dunas móviles embrionarias",
        "2120": "Dunas móviles de litoral con Ammophila arenaria (dunas blancas)",
        "2130": "Dunas costeras fijas con vegetación herbácea (dunas grises)",
        "2150": "Dunas fijas descalcificadas atlánticas (Calluno-Ulicetea)",
        "2190": "Depresiones intradunales húmedas",
        "2210": "Dunas fijas de litoral del Crucianellion maritimae",
        "2230": "Dunas con céspedes del Malcomietalia",
        "2240": "Dunas con céspedes del Brachypodietalia y de plantas anuales",
        "2250": "Dunas litorales con Juniperus spp.",
        "2260": "Dunas con vegetación esclerófila de Cisto-Lavanduletalia",
        "2270": "Dunas con bosques de Pinus pinea y/o Pinus pinaster",
        "3110": "Aguas oligotróficas con un contenido de minerales muy bajo de las llanuras arenosas (Littorelletalia uniflorae)",
        "3140": "Aguas oligomesotróficas calcáreas con vegetación béntica de Chara spp.",
        "3150": "Lagos eutróficos naturales con vegetación Magnopotamion o Hydrocharition",
        "3160": "Lagos y estanques distróficos naturales",
        "3170": "Estanques temporales mediterráneos",
        "3220": "Ríos alpinos con vegetación herbácea en sus orillas",
        "3230": "Ríos alpinos con vegetación leñosa en sus orillas de Myricaria germanica",
        "3240": "Ríos alpinos con vegetación leñosa en sus orillas de Salix elaeagnos",
        "3250": "Ríos mediterráneos de caudal permanente con Glaucium flavum",
        "3260": "Ríos de pisos de planicie a montano con vegetación de Ranunculion fluitantis y de Callitricho-Batrachion",
        "3270": "Rios de orillas fangosas con vegetación de Chenopodion rubri p.p. y de Bidention p.p.",
        "3280": "Ríos mediterráneos de caudal permanente del Paspalo-Agrostidion con cortinas vegetales ribereñas de Salix y Populus alba",
        "3290": "Ríos mediterráneos de caudal intermitente del Paspalo-Agrostidion",
        "4020": "Brezales húmedos atlánticos de zonas templadas de Erica ciliaris y Erica tetralix",
        "4030": "Brezales secos europeos",
        "4040": "Brezales secos atlánticos costeros de Erica vagans",
        "4050": "Brezales macaronésicos endémicos",
        "4060": "Brezales alpinos y boreales",
        "4090": "Brezales oromediterráneos endémicos con aliaga",
        "5110": "Formaciones estables xerotermófilas de Buxus sempervirens en pendientes rocosas (Berberidion p.p.)",
        "5120": "Formaciones montanas de Cytisus purgans",
        "5130": "Formaciones de Juniperus communis en brezales o pastizales calcáreos",
        "5210": "Matorral arborescente con Juniperus spp.",
        "5220": "Matorrales arborescentes con Ziziphus",
        "5230": "Matorrales arborescentes con Laurus Tobilis",
        "5320": "Formaciones bajas de euphorbia próximas a acantilados",
        "5330": "Matorrales termomediterráneos y pre-estépicos",
        "5410": "Matorrales de tipo frigánico del Mediterráneo occidental de cumbres de acantilado (Astragalo-Plantaginetum subulatae)",
        "5430": "Matorrales espinosos de tipo frigánico endémicos del Euphorbio-Verbascion",
        "6110": "Prados calcáreos o basófilos de Alysso-Sedion albi",
        "6140": "Prados pirenaicos silíceos de Festuca eskia",
        "6160": "Prados ibéricos silíceos de Festuca indigesta",
        "6170": "Prados alpinos y subalpinos calcáreos",
        "6210": "Prados secos seminaturales y facies de matorral sobre sustratos calcáreos (Festuco-Brometalia)",
        "6220": "Zonas subestépicas de gramíneas y anuales de Thero-Brachypodietea",
        "6230": "Formaciones herbosas con Nardus, con numerosas especies, sobre sustratos silíceos de zonas montañosas (y de zonas submontañosas de Europa continental)",
        "6310": "Dehesas perennifolias de Quercus spp.",
        "6410": "Prados con molinias sobre sustratos calcáreos, turbosos o arcillo-limónicos (Molinion caeruleae)",
        "6420": "Prados húmedos mediterráneos de hierbas altas del Molinion-Holoschoenion",
        "6430": "Megaforbios eutrofos higrófilos de las orlas de llanura y de los pisos montano a alpino",
        "6510": "Prados pobres de siega de baja altitud (Alopecurus pratensis, Sanguisorba officinalis)",
        "6520": "Prados de siega de montaña",
        "7110": "Turberas altas activas",
        "7130": "Turberas de cobertura",
        "7140": "'Mires' de transición",
        "7150": "Depresiones sobre sustratos turbosos del Rhynchosporion",
        "7210": "Turberas calcáreas de Cladium mariscus y con especies del Caricion davallianae",
        "7220": "Manantiales petrificantes con formación de tuf (Cratoneurion)",
        "7230": "Turberas bajas alcalinas",
        "7240": "Formaciones pioneras alpinas del Caricion bicoloris-atrofuscae",
        "8130": "Desprendimientos mediterráneos occidentales y termófilos",
        "8210": "Pendientes rocosas calcícolas con vegetación casmofítica",
        "8220": "Pendientes rocosas silíceas con vegetación casmofítica",
        "8230": "Roquedos silíceos con vegetación pionera del Sedo-Scleranthion o del Sedo albi- Veronicion dillenii",
        "8310": "Cuevas no explotadas por el turismo",
        "8320": "Campos de lava y excavaciones naturales",
        "8330": "Cuevas marinas sumergidas o semisumergidas",
        "8340": "Glaciares permanentes",
        "9120": "Hayedos acidófilos atlánticos con sotobosque de Ilex y a veces de Taxus (Quercion robori-petraeae o Ilici-Fagenion)",
        "9130": "Hayedos del Asperulo-Fagetum",
        "9150": "Hayedos calcícolas medioeuropeos del Cephalanthero-Fagion",
        "9160": "Robledales pedunculados o albares subatlánticos y medioeuropeos del Carpinion betuli",
        "9180": "Bosques de laderas, desprendimientos o barrancos del Tilio-Acerion",
        "91B0": "Fresnedas termófilas de Fraxinus angustifolia",
        "91E0": "Bosques aluviales de Alnus glutinosa y Fraxinus excelsior (Alno-Padion, Alnion incanae, Salicion albae)",
        "9230": "Robledales galaico-portugeses con Quercus robur y Quercus pyrenaica",
        "9240": "Robledales ibéricos de Quercus faginea y Quercus canariensis",
        "9260": "Bosques de Castanea sativa",
        "92A0": "Bosques galería de Salix alba y Populus alba",
        "92B0": "Bosques galería de ríos de caudal intermitente mediterráneos con Rhododendron ponticum, Salix y otras",
        "92D0": "Galerías y matorrales ribereños termomediterráneos (Nerio-Tamaricetea y Securinegion tinctoriae)",
        "9320": "Bosques de Olea y Ceratonia",
        "9330": "Alcornocales de Quercus suber",
        "9340": "Bosques de Quercus ilex y Quercus rotundifolia",
        "9360": "Laurisilvas macaronésicas (Laurus, Ocotea)",
        "9370": "Palmerales de Phoenix",
        "9380": "Bosques de Ilex aquifolium",
        "9430": "Bosques montanos y subalpinos de Pinus uncinata (* en sustratos yesosos o calcáreos)",
        "9520": "Abetales de Abies pinsapo",
        "9530": "Pinares (sud-) mediterráneos de pinos negros endémicos",
        "9540": "Pinares mediterráneos de pinos mesogeanos endémicos",
        "9550": "Pinares endémicos canarios",
        "9560": "Bosques endémicos de Juniperus spp.",
        "9570": "Bosques de Tetraclinis articulata",
        "9580": "Bosques mediterráneos de Taxus baccata",
    }
    global_terms = {
        "1": "Hábitat costeros y vegetación halófila",
        "11": "Aguas marinas y medios de marea",
        "12": "Acantilados marítimos y playas de guijarros",
        "13": "Marismas y pastizales salinos atlánticos y continentales",
        "14": "Marismas y pastizales salinos mediterráneos y termoatlánticos",
        "15": "Estepas continentalaes halófilas y gipsófilas",
        "2": "Dunas marítimas y continentales",
        "21": " Dunas marítimas de las costas atlánticas, del mar del Norte y del Báltico",
        "22": "2 Dunas marítimas de las costas mediterráneas",
        "3": "Habitat de agua dulce",
        "31": "Aguas estancadas",
        "32": " Aguas corrientes-tramos de cursos de agua con dinámica natural y seminatural (lechos menores, medios y mayores)- en los que la calidad del agua no presenta alteraciones significativas",
        "4": "Brezales y matorrales de zona templada",
        "5": "Matorrales esclerófilos",
        "51": "Matorrales submediterráneos y de zona templada",
        "52": "Matorrales arborescentes mediterráneos",
        "53": "Matorrales termomediterráneos y preestépicos",
        "54": "Matorrales de tipo frigánico",
        "6": "Formaciones herbosas naturales y seminaturales",
        "61": "Prados naturales",
        "62": "Formaciones herbosas secas seminaturales y facies de matorral",
        "63": "Bosques esclerófilos de pastoreo (dehesas)",
        "64": "Prados húmedos seminaturales de hierbas altas",
        "65": "Prados mesófilos",
        "7": "Turberas altas, turberas bajas (fens y mires) y áreas pantanosas",
        "71": "Turberas ácidas de esfagnos",
        "72": "Áreas pantanosas calcáreas",
        "8": "Hábitats rocosos y cuevas",
        "81": "Desprendimientos rocosos",
        "82": "Pendientes rocosas con vegetación casmofítica",
        "83": "Otros hábitats rocosos",
        "9": "Bosques",
        "91": "Bosques de la Europa templada",
        "92": "Bosques mediterráneos caducifolios",
        "93": "Bosques esclerófilos mediterráneos",
        "94": "Bosques de coníferas de las montañas templadas",
        "95": "Bosques de coníferas de las montañas mediterráneas y macaronésicas",
    }

    classification = {}
    for code in codes:
        global_term = global_terms.get(code[0], "Desconocido")
        sub_term = global_terms.get(code[:2], global_term)
        full_name = habitat_mapping.get(code, "Desconocido")

        if global_term not in classification:
            classification[global_term] = {}

        if sub_term not in classification[global_term]:
            classification[global_term][sub_term] = []

        classification[global_term][sub_term].append({"code": code, "name": full_name})

    return classification


def count_habitats(classification):
    counts = {}
    for global_term, sub_terms in classification.items():
        total_count = sum(len(habitats) for habitats in sub_terms.values())
        counts[global_term] = total_count
        for sub_term, habitats in sub_terms.items():
            counts[sub_term] = len(habitats)
    return counts


def search_habitats(results):
    codes = []
    if results:
        for csv_path, rows in results.items():
            category = os.path.basename(csv_path).split("_")[-1].split(".")[0]
            for row in rows:
                habitat_code = row.get("habitat_code")
                if habitat_code:
                    codes.append(habitat_code)

    classification = classify_habitats(codes)
    counts = count_habitats(classification)

    output = {"classification": classification, "counts": counts}

    if output["classification"] == {}:
        output= None
        return output
    else:
        return output
        


    

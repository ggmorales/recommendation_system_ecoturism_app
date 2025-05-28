# Prompt para Análisis de Impacto Ambiental

## Descripción del objetivo
naliza la información proporcionada en los siguientes datos JSON para medir el **impacto ambiental de cualquier proyecto o acción humana en dicha zona** en una zona específica y genera un **índice de impacto ambiental** basado en los datos disponibles. También puedes mencionar el impacto ambiental que tienen las plantas y animales invasores en esa zona. 

### Información a utilizar
1. **Hábitats Naturales**:  
   - Datos proporcionados: `{habitats_info}`.  
   - **Requisito**:  
     - Identifica los tipos de hábitats presentes y calcula su impacto potencial basado en su cantidad y características.  
     - Explica la importancia ecológica de cada hábitat y señala posibles amenazas (deforestación, cambio climático, urbanización, etc.). 
     - Si no hay información sobre hábitats no muestres datos disponibles, muestra solo la conclusión sobre diversidad de hábitats

2. **Fauna**:  
   - Datos proporcionados: `{species_info}`.  
   - **Requisito**:  
     - Clasifica las especies en categorías de conservación (Least Concern, Vulnerable, Endangered, etc.).  
     - Determina cuáles especies están más amenazadas y explica las implicaciones ecológicas de su desaparición.  
     - Comenta la diversidad de fauna presente, incluyendo todas las aves, mamíferos, reptiles e invertebrados (para los invertebrados menciona que solo estás mencionando los más destacados pero que hay muchos más).  

3. **Flora**:  
   - Datos proporcionados: `{flora_keys}`.  
   - **Requisito**:  
     - Identifica las principales especies vegetales presentes en la zona y su rol en el ecosistema.  
     - Indica si alguna especie está en riesgo según los datos proporcionados.  

---

### Índice de Impacto Ambiental
Genera un índice que evalúe el impacto ambiental de la zona basado en los siguientes criterios:
1. **Diversidad de hábitats**:  
   - Asigna un valor según el número y tipo de hábitats presentes.  
2. **Amenaza a la fauna**:  
   - Calcula el nivel de impacto según el número de especies vulnerables o en peligro de extinción.  
3. **Conservación de flora**:  
   - Evalúa según la cantidad de especies vegetales totales en la zona.  

El índice debe incluir:
1. Una puntuación global del impacto ambiental (escala de 1 a 10, donde 1 es bajo impacto y 10 es alto impacto). 
2. Una explicación de la puntuación del impacto, señalando lo que implica dicha puntuación. 
3. Factores que aumentan o disminuyen el impacto. En esta sección no menciones nada de especies invasoras.  
4. Recomendaciones para mejorar la situación actual.  

---

### Estilo del análisis
- Utiliza un enfoque educativo y científico para el análisis.  
- Genera propuestas que ayuden a mitigar amenazas y promuevan la conservación de la biodiversidad en la zona.  


### Plantilla a utilizar:


Aquí además de explicar el análisis, debes indicar que mide el impacto ambiental potencial que tendría cualquier proyecto o acción humana en dicha zona.

## **Introducción**


## 🏞️ Diversidad de Hábitats 

### Tipos de Hábitats Presentes

#### 1. Tipo de hábitat
- ...
- ...
.
.
.
##### Importancia Ecológica
##### Amenazas

#### 2. Tipo de hábitat
- ...
- ...
.
.
.
##### Importancia Ecológica
##### Amenazas
.
.
.
### Conclusión sobre Diversidad de Hábitats

---

## 🦅 Fauna 

### Clasificación de Especies por Categorías de Conservación
La fauna de la zona incluye x especies distribuidas en aves, mamíferos, reptiles e invertebrados destacados.

#### Aves (nº especies)
Lista por grado de amenaza indicando nombre científico y nombre común.

##### Importancia 
Explica por que contribuyen a mantener la biodiversidad.

#### Mamíferos  (nº especies)
Lista por grado de amenaza indicando nombre científico y nombre común.

##### Importancia
Explica por que contribuyen a mantener la biodiversidad.

#### Reptiles  (nº especies)
Lista por grado de amenaza indicando nombre científico y nombre común.

##### Importancia
Explica por que contribuyen a mantener la biodiversidad.

#### Invertebrados  (nº especies destacadas)
Lista por grado de amenaza indicando nombre científico y nombre común.

##### Importancia
Explica por que contribuyen a mantener la biodiversidad.

### Amenazas y Consecuencias Ecológicas


---

## 🌸 Flora 

### Principales Especies Vegetales y su Rol Ecológico
La zona alberga más de x especies vegetales, entre las que destacan:

#### Tipo
##### Rol Ecológico:

#### Tipo
##### Rol Ecológico:
.
.
.

### Evaluación de Riesgo

---

## 📈 Índice de Impacto Ambiental 

### Puntuación Global
##### Explicación:

### Factores que Aumentan el Impacto


### Factores que Disminuyen el Impacto


---

## ✍🏻 Recomendaciones 


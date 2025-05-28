import re
import os
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import json

current_dir = os.getcwd()

# Cargar el archivo Markdown
with open(os.path.join(current_dir, "boe", "BOE-A-2007-18475-responsabilidad medioambiental.md"), "r", encoding="utf-8") as f:
    markdown_text = f.read()

# Expresión regular para detectar títulos, subtítulos y subapartados
pattern = re.compile(r"^(#{1,3})\s*(.*)", re.MULTILINE)

# Variables para almacenar contexto
chunks = []
current_title = ""
current_subtitle = ""
current_subapartado = ""
current_text = []
current_context = ""

# Procesar línea por línea para construir los chunks
for line in markdown_text.split("\n"):
    match = pattern.match(line)
    if match:
        # Si hay contenido en current_text, procesa el chunk anterior
        if current_text:
            chunk_text = "\n".join(current_text).strip()
            if chunk_text:  # Verifica que el chunk tenga contenido real
                context = " > ".join(filter(None, [current_title, current_subtitle, current_subapartado]))
                chunks.append(Document(page_content=f"{context}\n\n{chunk_text}"))
            current_text = []  # Reiniciar el texto acumulado

        # Identificar el nivel del título
        level = len(match.group(1))  # Número de almohadillas
        title = match.group(2).strip()

        # Asignar correctamente el contexto según el nivel
        if level == 1:
            current_title = title
            current_subtitle = ""
            current_subapartado = ""
        elif level == 2:
            current_subtitle = title
            current_subapartado = ""
        elif level == 3:
            current_subapartado = title

    else:
        current_text.append(line)

# Agregar el último chunk si hay contenido
if current_text:
    chunk_text = "\n".join(current_text).strip()
    if chunk_text:
        context = " > ".join(filter(None, [current_title, current_subtitle, current_subapartado]))
        chunks.append(Document(page_content=f"{context}\n\n{chunk_text}"))


# Chunks generados
print(f"Total de chunks generados: {len(chunks)}\n")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i + 1}:\n{chunk.page_content}\n{'-'*50}")


# Guardar chunks preprocesados
with open("chunks.json", "w", encoding="utf-8") as f:
    json.dump([chunk.page_content for chunk in chunks], f, ensure_ascii=False, indent=4)


# Crear el vectorstore con los chunks usando FAISS
semantic_chunk_vectorstore = FAISS.from_documents(chunks, embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))
semantic_chunk_vectorstore.save_local("faiss_index")








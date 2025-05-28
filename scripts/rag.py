from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from llm_requests import generate_response


# Definir el modelo de embeddings
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Cargar el índice FAISS correctamente
semantic_chunk_vectorstore = FAISS.load_local(
    "vectorial_database",
    embeddings=embedding_model,
    allow_dangerous_deserialization=True  
)
semantic_chunk_retriever = semantic_chunk_vectorstore.as_retriever(search_kwargs={"k": 5})


# Crear la plantilla para el prompt
rag_template = '''\
#Query del usuario:
#{pregunta}

#Contexto:
#{contexto}
'''
rag_prompt = ChatPromptTemplate.from_template(rag_template)

# Convertir la función make_request en un RunnableLambda
def make_request_as_runnable(role):
    return RunnableLambda(lambda rag_prompt: generate_response(role, str(rag_prompt)))

role = '''
Eres un experto en derecho medioambiental.
Debes explicarle al usuario si la actividad económica que ha causado el daño medioambiental está regulada por: Ley 26/2007 de 23 de octubre de Responsabilidad Medioambiental.
Para saber responder, debes tener en cuesta el contexto proporcionado. Debes generar una respuesta lo más informativa posible con toda la información relevante en el contexto.
Lo primero en lo que te debes fijar es si la actividad económica se encuentra en el anexo III de la Ley 26/2007, de 23 de octubre, de Responsabilidad Medioambiental, de ser así,
la ley se aplicará, habrá sanciones y cuales son las consecuencias de que la ley se aplique basandote en el contexto. 
Si la actividad económica no se encuentra en el anexo III, debes racionar que actividades del anexo III podría llegar a realizar la actividad ingresada por el usuario aunque no sea lo más común,
e indicar que si realiza alguna de esas actividades, si que estaría regulada por dicha ley, además, debes responder según el ámbito de aplicación medioambiental del contexto, en que casos se aplicaría la ley cuando no realice ninguna actividad incluida en el anexo III.
El formato de la respuesta debe ser markdown, cuyo titulo debe ser si el daño de la actividad económica ingresada es sancionable o no por la ley mencionada. Los siguientes apartados debes crearlos a partir del contexto.
'''

# Crear el flujo RAG
semantic_rag_chain = (
    {"contexto": semantic_chunk_retriever, "pregunta": RunnablePassthrough()}
    | rag_prompt
    | make_request_as_runnable(role)
    | StrOutputParser()
)

# Invocar el flujo RAG con una consulta específica
def get_rag_response(query):
    response = semantic_rag_chain.invoke(query)
    return response

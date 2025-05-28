import time
from openai import AzureOpenAI
import os
from dotenv import load_dotenv


# Cargar las variables del archivo .env
load_dotenv()

# Obtener las variables de entorno
api_key = os.getenv("API_KEY")
endpoint = os.getenv("ENDPOINT") 


client = AzureOpenAI(api_version="2024-12-01-preview", azure_endpoint=endpoint, api_key=api_key)


def generate_response(role, prompt):
    try:
        messages = [
                    {"role": "system", "content": role},
                    {"role": "user", "content": prompt}
                    ]
 
        # Enviar solicitud al LLM
        chat_completion = client.chat.completions.create(model='gpt-4.1-mini', messages = messages, max_completion_tokens=4000,
                                                temperature=0.7, top_p=0.95, frequency_penalty=0,
                                                presence_penalty=0, stop=None, stream=False)
        
        # Devolver el contenido del mensaje de respuesta
        return chat_completion.choices[0].message.content
    except Exception as e:
        if "429" in str(e):  # Esperar si se excede el límite de llamadas
            print("waiting...")
            print(str(e))
            time.sleep(25)
            return generate_response(role, prompt)
        raise SystemExit(f"Failed to make the request. Error: {e}")





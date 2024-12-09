# Este módulo maneja el chat con el modelo de Ollama.
# Hay 3 usuarios:
# - system: el sistema (nosotras)
# - model: el modelo de Ollama
# - user: el usuario

# Importamos las librerías
from ollama import chat

# Inicializamos una lista para almacenar el historial de mensajes.
historial = []

def iniciar_modelo(base_conocimiento):

    messages = {
        'role': 'system',
        'content': f"""
        You are an assistant that answers questions based solely on the provided knowledge base. 
        You must not provide answers that are not explicitly mentioned in the knowledge base. 
        If the information is not present in the knowledge base, respond with: "I don't know."
        Do not infer, guess, or add any details not present in the knowledge base. "

        Knowledge Base:
        {base_conocimiento}

        ---
        """,
    }
    historial.append(messages)

def consulta(comando):

    messages = {
        'role': 'user',
        'content': comando,
    }
    # Añadimos la consulta del usuario al historial
    historial.append(messages)
    try:
        # Consultamos al modelo
        response = chat('llama3.2:1b', messages=historial)
        # Imprimimos la respuesta
        print(response['message']['content'])
        # Añadimos la respuesta del modelo al historial
        historial.append({
            'role': 'assistant',
            'content': response['message']['content'],
        })
    except Exception as e:
       print(f"Error al consultar el modelo de Ollama:", e)

def consulta_sin_historial(base_conocimiento, pregunta):
    
    messages = [
        {
            'role': 'system',
            'content': f"""
            You are an assistant that answers questions based solely on the provided knowledge base. 
            You must not provide answers that are not explicitly mentioned in the knowledge base. 
            If the information is not present in the knowledge base, respond with: "I don't know."
            Use basic logical reasoning when interpreting the knowledge base.

            Knowledge Base:
            {base_conocimiento}

            ---
            """
        },
        {
            'role': 'user',
            'content': pregunta,
        }
    ]

    try:
        # Consultamos al modelo
        response = chat('llama3.2:1b', messages=messages)
        # Imprimimos la respuesta
        print(response['message']['content'])
    except Exception as e:
        print(f"Error al consultar el modelo de Ollama:", e)
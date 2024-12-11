# Importamos las librerías
from ollama import chat

def consulta_sin_historial(base_conocimiento):

    # You are an assistant that organizes the following knowledge base written in natural language into a structured dictionary format.
    #         The dictionary will have two keys: "persons" and "houses".
    #         Don't add information that is not in the knowledge base to the structured dictionary format but instead it 
    #         must include all the information from the knowledge base.
    
    messages = [
        {
            'role': 'system',
            'content': f"""
            
            You are an assistant that organizes the following knowledge base written in natural language.

            Knowledge Base:
            {base_conocimiento}

            You have to divide the following knowledge base written in natural language into characters and houses.
            You must include all the information from the knowledge base.
            Don't add additional information that is not in the knowledge base.
            Make sure to include a paragraph for each character and houses mentioned in the knowledge base.

            The output must be like this:
            "Character 1": "All text related to Character 1"
            Character 2: All text related to Character 2
            ...
            House 1: All text related to House 1
            ...
            """
        },
    ]

    try:
        # Consultamos al modelo
        response = chat('llama3.2:1b', messages=messages)
        # Imprimimos la respuesta
        print(response['message']['content'])
    except Exception as e:
        print(f"Error al consultar el modelo de Ollama:", e)
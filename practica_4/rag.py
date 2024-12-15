# Importamos las librerías
from ollama import chat

def dividir_base_conocimiento_1(base_conocimiento):
    """NO FUNCIONA"""
    
    messages = [
        {
            'role': 'system',
            'content': f"""
            You are given a knowledge base containing detailed information about characters and families in the world of Game of Thrones.
            Your task is to organize this information by doing the following:

            1. Identify each character and the facts related to them.
            2. For each character, extract all relevant relationships with other characters. For example, if a character is married to another, include this information in both characters' sections.
            3. For each character, group all the relevant facts into one section dedicated to that character.
            4. If any sentence in the base knowledge concerns another character, add it to the other character's section as well.
            5. Output the base knowledge in a structured way, where each character has their own section with all the facts and relationships relevant to them.

            Here's an example of how you should format your output:

            ### Eddard Stark
            Eddard Stark, also known as "Ned", was the head of House Stark.  
            He was married to Catelyn Stark, a member of House Tully.  
            Eddard Stark was 41 years old in Season 1 of Game of Thrones.  
            Catelyn Stark is his wife.

            ### Catelyn Stark
            Catelyn Stark, also known as "Cat", played a critical role in the political alliances of the North.  
            She was married to Eddard Stark, a member of House Stark.  
            Eddard Stark is her husband.

            Please process the following text and format the output in a similar way. Here is the knowledge base you need to process:

            {base_conocimiento}
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

def dividir_base_conocimiento_2(base_conocimiento):
    """Aplica RAG para dividir la base de conocimiento en 3 categorías:
    - personajes
    - casas
    - otro
    Crea un diccionario a partir de la respuesta del modelo.
    """

    dictionary = {"characters": "",
                  "houses": "",
                  "other information not related to characters or houses": ""}
    
    categories = ["characters", "houses", "other information not related to characters or houses"]

    for category in categories:
        messages = [
            {
                'role': 'system',
                'content': f"""
                You are given a knowledge base written in natural lenguage containing information about the world of Game of Thrones.
                Note that the knowledge base is already structured with headers, used them to select information.
                Return a text paragraph with all the text in the knowledge base related to: {category}.
                Use literal text from the knowledge base to write the text paragraph.
                Do not include information in the text paragraph that cannot be inferred from the knowledge base.
                
                Here is the knowledge base:
                {base_conocimiento}
                """
            },
        ]

        try:
            # Consultamos al modelo
            response = chat('llama3.2:1b', messages=messages)
            response_text = response['message']['content']
            # Imprimimos la respuesta
            print(f"\n---{category}---\n")
            print(response_text)
            # Añadimos la respuesta al diccionario
            dictionary[category] = response_text
        except Exception as e:
            print(f"Error al consultar el modelo de Ollama:", e)
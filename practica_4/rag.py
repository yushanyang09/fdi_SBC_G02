# Este módulo incluye la implementación para el RAG
# Las funciones para RAG están comentadas en el main porque no funciona correctamente.

# Importamos las librerías
from ollama import chat

CATEGORIES = [
    "characters",
    "houses",
    "other information not related to characters or houses",
]


def dividir_base_conocimiento_1(base_conocimiento):
    """Intento de aplicar RAG para dividir la base de conocimiento según los diferentes
    personajes y casas de Juego de Tronos."""

    messages = [
        {
            "role": "system",
            "content": f"""
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
            """,
        },
    ]

    try:
        # Consultamos al modelo
        response = chat("llama3.2:1b", messages=messages)
        # Imprimimos la respuesta
        print(response["message"]["content"])
    except Exception as e:
        print(f"Error al consultar el modelo de Ollama:", e)


def dividir_base_conocimiento_2(base_conocimiento, modelo):
    """Aplica RAG para dividir la base de conocimiento en 3 categorías:
    - personajes
    - casas
    - otro
    Crea un diccionario a partir de la respuesta del modelo.
    """

    mapping = {
        "characters": "",
        "houses": "",
        "other information not related to characters or houses": "",
    }

    for category in CATEGORIES:
        messages = [
            {
                "role": "system",
                "content": f"""
                You are given a knowledge base written in natural lenguage containing information about the world of Game of Thrones.
                Note that the knowledge base is already structured with headers, used them to select information.
                Return a text paragraph with all the text in the knowledge base related to: {category}.
                Use literal text from the knowledge base to write the text paragraph.
                Do not include information in the text paragraph that cannot be inferred from the knowledge base.
                
                Here is the knowledge base:
                {base_conocimiento}
                """,
            },
        ]

        try:
            # Consultamos al modelo
            response = chat(modelo, messages=messages)
            response_text = response["message"]["content"]
            # Imprimimos la respuesta
            print(f"\n---{category}---\n")
            print(response_text)
            # Añadimos la respuesta al diccionario
            mapping[category] = response_text
            return mapping
        except Exception as e:
            print(f"Error al consultar el modelo de Ollama:", e)


def rag_consulta(consulta, mapping, modelo):
    """
    Clasifica una consulta del usuario en una o varias categorías, y extrae la información relevante
    del diccionario mapping basado en las categorías seleccionadas.

    Parámetros:
    - consulta: la pregunta del usuario.
    - mapping: un diccionario con las categorías como claves y la información correspondiente como valores.
    - modelo: el modelo de lenguaje a utilizar.

    Devuelve:
    - Un texto que combina la información extraída de las categorías seleccionadas.
    """

    messages = [
        {
            "role": "system",
            "content": f"""
            You are an assistant trained to classify user queries into predefined categories.
            Your task is to determine which of the following categories are relevant to the given user query:
            1. characters
            2. houses
            3. other information not related to characters or houses

            You may select one or more categories, but you must choose only the relevant ones.
            If you are unsure or the query is ambiguous, select all three categories.

            Provide your response as a comma-separated list of categories (e.g., "characters, houses").
            Do not include any explanation or additional text.
            """,
        },
    ]

    try:
        # Consultamos al modelo
        response = chat(modelo, messages=messages)
        response_text = response["message"]["content"]

        # Imprimimos la respuesta
        print(response_text)

        # Procesamos las categorías seleccionadas por el modelo
        selected_categories = [
            cat.strip() for cat in response_text.split(",") if cat.strip() in CATEGORIES
        ]

        # Si no se selecciona ninguna categoría válida, seleccionamos todas
        if not selected_categories:
            selected_categories = CATEGORIES

        # Extraemos la información de las categorías seleccionadas
        extracted_information = "\n".join([mapping[cat] for cat in selected_categories])
        return extracted_information

    except Exception as e:
        print(f"Error al consultar el modelo de Ollama:", e)


def guardar_mapeo(mapping):
    """
    Guarda el contenido de un diccionario mapping en tres archivos de texto distintos.
    Cada archivo corresponde a una categoría o clave del diccionario.

    Parámetro:
    - mapping: diccionario con las claves como categorías y los valores como contenido.
    """
    try:
        # Iteramos sobre las claves y valores del diccionario
        for category, content in mapping.items():
            # Creamos un nombre de archivo basado en la categoría
            filename = f"{category.replace(' ', '_').lower()}.txt"
            # Guardamos el contenido en el archivo correspondiente
            with open(filename, "w", encoding="utf-8") as file:
                file.write(content)
        print("El mapeo se ha guardado correctamente en archivos de texto.")
    except Exception as e:
        print(f"Error al guardar el mapeo: {e}")

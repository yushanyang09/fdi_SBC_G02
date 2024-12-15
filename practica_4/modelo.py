# Este módulo maneja el chat con el modelo de Ollama.
# Utilizamos 2 usuarios:
# - system: el sistema (nosotras)
# - user: el usuario

# Importamos las librerías
from ollama import chat


def consulta(base_conocimiento, pregunta, modelo):
    """Realiza una consulta al modelo e imprime la respuesta. No se utiliza CoT.
    Parámetros:
    - base_conocimiento: texto de la base de conocimiento completa
    - pregunta: pregunta del usuario
    - modelo: modelo de Ollama a utilizar
    """

    messages = [
        {
            "role": "system",
            "content": f"""
            You are an assistant that answers questions based solely on the provided knowledge base. 
            You must not provide answers that are not explicitly mentioned in the knowledge base.
            Do not include information in the answers that cannot be inferred from the knowledge base.
            If the information is not present in the knowledge base, respond with: "I don't know."
            Use basic logical reasoning when interpreting the knowledge base.

            Knowledge Base:
            {base_conocimiento}

            ---
            """,
        },
        {
            "role": "user",
            "content": pregunta,
        },
    ]

    try:
        # Consultamos al modelo
        response = chat(modelo, messages=messages)
        # Imprimimos la respuesta
        print(response["message"]["content"])
    except Exception as e:
        print(f"Error al consultar el modelo de Ollama:", e)


def consulta_chain_of_thought(base_conocimiento, pregunta, modelo):
    """Realiza una consulta al modelo e imprime la respuesta. Para obtener la respuesta final se implementa
    Chain of Thought de la siguiente forma:
    1. Primero se permite al modelo dar una respuesta exploratoria, en la que se trata de simular el razonamiento humano.
    2. A partir de la respuesta exploratoria, el modelo dará una respuesta final dirigida al usuario.
    Parámetros:
    - base_conocimiento: texto de la base de conocimiento completa
    - pregunta: pregunta del usuario
    - modelo: modelo de Ollama a utilizar
    """

    # Respuesta exploratoria
    messages_exploratory = [
        {
            "role": "system",
            "content": f"""
            You are an assistant that answers questions **based exclusively on the provided knowledge base**.
            You are not allowed to use information that is not explicitly stated in the knowledge base.
            For this phase, generate exploratory responses to simulate human reasoning.
            Include uncertainties, logical interpretations, or potential errors.
            Explain how each step in your reasoning is derived from the knowledge base.
            You may not introduce any external information, guesses, or assumptions beyond what the knowledge base provides.
            Use basic logical reasoning when interpreting the provided knowledge base.
            
            Answer the following question while reasoning step by step based exclusively on the knowledge base:
            {base_conocimiento}

            ---
            
            """,
        },
        {
            "role": "user",
            "content": pregunta,
        },
    ]

    try:
        # Consultamos al modelo para la respuesta exploratoria
        response_exploratory = chat(modelo, messages=messages_exploratory)
        exploratory_answer = response_exploratory["message"]["content"]
        print("\n---Exploratory Answer---\n", exploratory_answer)

        # Reflexión y respuesta final
        messages_refined = [
            {
                "role": "system",
                "content": f"""
                You have generated a previous exploratory answer.
                Now, review your previous reasoning and refine your answer.
                Generate a clear and concise response **based exclusively on the provided knowledge base**.
                Correct any uncertainties, logical assumptions, or mistakes from the exploratory phase.
                Remember: You are only allowed to use information explicitly mentioned in the knowledge base.
                Do not include irrelevant details or contradictions.
                If the information is not present in the knowledge base, respond with: "I don't know."
                
                Knowledge Base:
                {base_conocimiento}

                Previous Exploratory Answer:
                {exploratory_answer}

                ---

                """,
            },
            {
                "role": "user",
                "content": pregunta,
            },
        ]

        # Consultamos al modelo para la respuesta refinada
        response_refined = chat(modelo, messages=messages_refined)
        refined_answer = response_refined["message"]["content"]
        print("\n---Final Answer---\n", refined_answer, "\n")

        return refined_answer

    except Exception as e:
        print(f"Error al consultar el modelo de Ollama:", e)

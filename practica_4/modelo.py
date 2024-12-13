# Este módulo maneja el chat con el modelo de Ollama.
# Hay 3 usuarios:
# - system: el sistema (nosotras)
# - model: el modelo de Ollama
# - user: el usuario

# Importamos las librerías
from ollama import chat

def consulta(base_conocimiento, pregunta):
    
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

def consulta_chain_of_thought(base_conocimiento, pregunta):

    # Primera iteración: respuesta exploratoria
    messages_exploratory = [
        {
            'role': 'system',
            'content': f"""
            You are an assistant that answers questions based solely on the provided knowledge base.
            However, for this phase, you are allowed to generate exploratory responses that may include uncertainties, 
            logical assumptions, or even possible mistakes.
            You can only take into account the information explicitly mentioned in the knowledge base
            and use basic logical reasoning when interpreting it.
            After this phase, your reasoning will be re-evaluated to refine the answer.

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
        # Consultamos al modelo para la respuesta exploratoria
        response_exploratory = chat('llama3.2:1b', messages=messages_exploratory)
        exploratory_answer = response_exploratory['message']['content']
        print("\n---Exploratory Answer---\n", exploratory_answer)

        # Segunda iteración: reflexión y respuesta final
        messages_refined = [
            {
                'role': 'system',
                'content': f"""
                You are an assistant that answers questions based solely on the provided knowledge base.
                You have previously generated an exploratory answer. Now, you must evaluate and refine your reasoning to 
                provide the most accurate and concise response, strictly based on the knowledge base. 
                If the information is not present in the knowledge base, respond with: "I don't know."
                Do not include irrelevant details or contradictions.

                Knowledge Base:
                {base_conocimiento}

                Previous Exploratory Answer:
                {exploratory_answer}

                ---
                """
            },
            {
                'role': 'user',
                'content': pregunta,
            }
        ]

        # Consultamos al modelo para la respuesta refinada
        response_refined = chat('llama3.2:1b', messages=messages_refined)
        refined_answer = response_refined['message']['content']
        print("\n---Final Answer---\n", refined_answer)

        return refined_answer

    except Exception as e:
        print(f"Error al consultar el modelo de Ollama:", e)

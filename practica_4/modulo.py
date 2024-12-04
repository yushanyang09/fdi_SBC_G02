from ollama import chat

def iniciar_modelo(base_conocimiento):

    messages = [
        {
            'role': 'system',
            'content': f"""You are an assistant for question-answering tasks. If you don't know the answer, just say that
            you don't know. Use the following document to answer the question: {base_conocimiento}""",
        },
    ]
    response = chat('llama3.2:1b', messages=messages)
    print(response['message']['content'])

def consulta(comando):

    messages = [
        {
            'role': 'user',
            'content': comando,
        },
        
    ]
    response = chat('llama3.2:1b', messages=messages)
    print(response['message']['content'])
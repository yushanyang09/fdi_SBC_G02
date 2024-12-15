# Práctica 4

En esta práctica tratamos de implementar un asistente virtual usando grandes modelos de lenguaje (LLMs). Para ello hemos utilizado el modelo llama3.2:1b de Ollama.

Para ejecutar el programa en tu terminal introduce el siguiente comando:

`uv run practica_4.py <ruta_base_conocimiento>`

Argumentos:

    - ruta_base_conocimiento: nombre del fichero que contiene la base de conocimiento a utilizar

### Interfaz de usuario

El usuario podrá escribir consultas en formato libre (en inglés), y el programa responderá a ellas usando la información de la base de conocimiento.

### Base de conocimiento

La base de conocimiento que hemos construído esta basada en la que usamos para la práctica 3. Se trata de información sobre la serie Juego de Tronos. A diferencia de para la práctica 3, para esta práctica la hemos escrito en lenguaje natural (inglés) y la hemos ampliado parcialmente.

### RAG

Para aplicar RAG en primer lugar intentamos hacerlo de manera que el modelo seleccionara la información correspondiente a cada personaje y casa. Intentamos que, si por ejemplo una frase se refería a dos personajes, esta estuviera presente en la información de ambos personajes. El prompt utilizado se encuentra en la función <code>dividir_base_conocimiento_1</code> del módulo <code>rag.py</code>.

Como el enfoque anterior no parecía funcionar hicimos otra función <code>dividir_base_conocimiento_2</code> que indica al modelo que divida la inforamción en 3 categorías: personajes, casas y otro.

### Chain of Thought

Para la implementación de CoT hemos hecho la función <code>consulta_chain_of_thought</code> que se encuentra en el módulo <code>modelo.py</code>.

Esta función primero genera una respuesta exploratoria simulando razonamiento humano, y luego, a partir de esa respuesta, produce una respuesta final refinada y concisa exclusivamente con información de la base de conocimiento.

Pese a varios intentos con distintos prompts no hemos conseguido que funcione correctamente siempre. Aunque para algunas consultas sí que parece funcionar:

>Introduce un comando: who is the head of House Stark?
>
>---Exploratory Answer---
>
>According to the provided knowledge base:
>
>* Eddard Stark (also known as "Ned") was the head of House Stark.
>* Catelyn Stark, also known as "Cat", played a critical role in the political alliances of the North but does not hold the title of head of House Stark.
>
>---Final Answer---
>
>According to the knowledge base, Eddard Stark (also known as "Ned") was the head of House Stark.`

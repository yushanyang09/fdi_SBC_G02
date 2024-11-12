def leer_consulta(texto_consulta):
    """Parsea el texto de la consulta.
    
    Parámetros:
    - texto_consulta (string): consulta introducida por el usuario

    Devuelve:
    - variables_select (lista): variables que aparecen en el SELECT de la consulta y
    que por tanto deberán ser mostradas en la salida
    - tuplas_where (lista): lista de tuplas de 3 elementos (sujeto, predicado, objeto),
    cada una representa una sentencia del WHERE
    """

    # Dividimos el texto de la consulta usando "where" como separador
    split_where = texto_consulta.split("where")

    # Obtenemos las variables del select
    variables_select = [token.strip(",") for token in split_where[0].split() if token.startswith('?')]

    # Obtenemos las tuplas con las sentencias del where
    sentencias = split_where[1].split('{')[1].split('}')[0]
    sentencias = [s.strip() for s in sentencias.split('.') if s.strip()]
    tuplas_where = [tuple(sentencia.split()) for sentencia in sentencias]

    return variables_select, tuplas_where

def resolver_consulta(afirmaciones, consulta):
    """Resuelve una consulta buscando iterativamente una afirmación de la base de
    conocimiento que coincida con lo que se pregunta en la consulta.

    Parámetros:
    - afirmaciones: lista de afirmaciones (tuplas) de la base de conocimiento
    - consulta: tupla de 3 elementos

    Devuelve:
    Todas las afirmaciones (tuplas) que cumplen la consulta.
    """

    respuestas = []
    tupla_booleana = tuple(elemento.startswith('?') for elemento in consulta)

    for afirmacion in afirmaciones:

        condicion_sujeto = (afirmacion[0] == consulta[0]) | tupla_booleana[0]
        condicion_relacion = (afirmacion[1] == consulta[1]) | tupla_booleana[1]
        condicion_objeto = (afirmacion[2] == consulta[2]) | tupla_booleana[2]

        if (condicion_sujeto & condicion_relacion & condicion_objeto):
            respuestas.append(afirmacion)
    
    return respuestas

def imprimir_respuestas(respuestas, variables_select, indice_a_variable):
    """Provisional: Imprime las respuestas basadas en las variables seleccionadas"""
    for respuesta in respuestas:
        salida = ", ".join(
            f"{variable}: {respuesta[indice_a_variable[variable]]}" 
            for variable in variables_select
            if variable in indice_a_variable
        )
        print(salida)


def procesar_consulta(bc, texto_consulta):
    """Procesa una consulta a la base de conocimiento introducida por el usuario.
    
    Parámetros:
    - bc: lista de afirmaciones (tuplas) de la base de conocimiento
    - texto_consulta (string): consulta introducida por el usuario
    """

    # Parseamos el texto de la consulta
    variables_select, tuplas_where = leer_consulta(texto_consulta)

    # Diccionario para almacenar los valores válidos para cada variable
    variables_usadas = {}

    # Mapeo de las variables a sus posiciones en las tuplas (para imprimir_respuestas)
    indice_a_variable ={var: None for var in variables_select}

     # Lista para almacenar las respuestas que resulten válidas
    respuestas_validas = []

    # Una tupla es una sentencia dentro del where que tiene 3 elementos (sujeto, predicado, objeto)
    for tupla in tuplas_where:

        # Qué elementos de la tupla son variables
        variables_tupla = tuple(elemento.startswith('?') for elemento in tupla)

       # Asocia cada variable a su posición en la tupla
        for j, elemento in enumerate(tupla):
            if variables_tupla[j] and elemento in variables_select:
                indice_a_variable[elemento] = j

        # Resolvemos la sentencia
        respuestas = resolver_consulta(bc, tupla)


        # Se pone a True la primera vez que una variable aparezca en una sentencia del WHERE
        # WHERE { ?personaje t2:pertenece q2:casa_stark . } -> [True, False, False]
        variables_nuevas = [False, False, False]

        for respuesta in respuestas:

            valida = True

            # Si el valor de una variable no es uno de los posibles valores almacenados para 
            # esa variable, la respuesta no es válida
            # Para cada elemento de una sentencia (sujeto, predicado, objeto)
            for j, elemento in enumerate(tupla):
                # Si es una variable
                if variables_tupla[j]:
                    # Si la variable ya fue usada
                    if elemento in variables_usadas and not variables_nuevas[j]:
                        # Si el valor en la respuesta no es uno de los posibles valores
                        # obtenidos de una consulta sobre una sentencia anterior
                        if respuesta[j] not in variables_usadas[elemento]:
                            # La respuesta no es válida
                            valida = False
                    # Si la variable no existe en variables_usada (no ha sido usada por una 
                    # sentencia anterior)
                    else:
                        if not variables_nuevas[j]:
                            # Se inicializa la lista de valores posibles de la variable
                            variables_usadas[elemento] = []
                            variables_usadas[elemento].append(respuesta[j])
                            variables_nuevas[j] = True
                        else:
                            # Se añade el nuevo valor posible de la variable
                            variables_usadas[elemento].append(respuesta[j])

            # Si la respuesta es válida la añadimos a la lista    
            if valida:
                respuestas_validas.append(respuesta)
    print(variables_usadas)

    imprimir_respuestas(respuestas_validas, variables_select, indice_a_variable)

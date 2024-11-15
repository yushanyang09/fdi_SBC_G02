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

def es_variable(elemento):
    """Determina si un elemento de una tupla es una variable."""

    return elemento.startswith('?')

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

    for afirmacion in afirmaciones:

        condicion_sujeto = (afirmacion[0] == consulta[0]) or es_variable(consulta[0])
        condicion_relacion = (afirmacion[1] == consulta[1]) or es_variable(consulta[1])
        condicion_objeto = (afirmacion[2] == consulta[2]) or es_variable(consulta[2])

        if (condicion_sujeto and condicion_relacion and condicion_objeto):
            respuestas.append(afirmacion)
    
    return respuestas

def imprimir_respuestas(variables_usadas, indices_validos, variables_select):
    """Imprime los valores de las variables de las respuestas.
    
    Parámetros:
    - variables_usadas (dict):
    - indices_validos (set):
    - variables_select (lista):
    """

    for indice in indices_validos:
        for variable in variables_select:
            #if (indice in variables_usadas[variable].values()): # creo que no hace falta
                # Nos quedamos con los valores de las variables (las claves del diccionario) que tengan este indice como valor
                respuestas = [clave for clave, val in variables_usadas[variable].items() if val == indice]
                print(respuestas)

def procesar_consulta(bc, texto_consulta):
    """Procesa una consulta a la base de conocimiento introducida por el usuario.
    
    Parámetros:
    - bc: lista de afirmaciones (tuplas) de la base de conocimiento
    - texto_consulta (string): consulta introducida por el usuario
    """

    # Parseamos el texto de la consulta
    variables_select, tuplas_where = leer_consulta(texto_consulta)

    # Diccionario para almacenar los valores posibles de cada variable
    # Las claves son las variables (por ejemplo, "?profesor")
    # El valor es otro diccionario cuyas claves son los posibles valores de esa variable 
    # junto con su índice (por ejemplo, {"alberto":0, "antonio":1})
    variables_usadas = {}

    # Asignamos un índice único a cada valor de una variable
    indice = 0

    # Resolvemos la primera sentencia
    tupla_inicial = tuplas_where[0]
    respuestas_iniciales = resolver_consulta(bc, tupla_inicial)

    for respuesta_inicial in respuestas_iniciales:
            for i, elemento in enumerate(tupla_inicial):
                if es_variable(elemento):
                    if elemento not in variables_usadas:
                        variables_usadas[elemento] = {}
                    variables_usadas[elemento][respuesta_inicial[i]] = indice
            indice += 1

    # Resolvemos las siguientes sentencias si las hay
    for tupla in tuplas_where[1:]:

        nuevas_respuestas = resolver_consulta(bc, tupla)

        respuestas_validas = []

        # Seleccionamos solo las respuestas válidas según las respuestas iniciales
        for nueva_respuesta in nuevas_respuestas:
            for i, elemento in enumerate(tupla):
                if es_variable(elemento):
                    if elemento in variables_usadas:
                        if nueva_respuesta[i] in variables_usadas[elemento]:
                            respuestas_validas.append(nueva_respuesta)
        
        # Conjunto para almacenar los índices de las respuestas válidas
        indices_validos = set()

        # Si una variable no se ha usado antes, se pone su posición a True
        variable_nueva = [False, False, False]

        for respuesta_valida in respuestas_validas:
            for i, elemento in enumerate(tupla):
                if es_variable(elemento):
                    if elemento in variables_usadas:
                        if variable_nueva[i] == False:
                            indice2 = variables_usadas[elemento][respuesta_valida[i]]
                            indices_validos.add(indice2)
                        else:
                            variables_usadas[elemento][respuesta_valida[i]] = indice2
                    else:
                        variables_usadas[elemento] = {}
                        variables_usadas[elemento][respuesta_valida[i]] = indice2
                        variable_nueva[i] = True
        
    imprimir_respuestas(variables_usadas, indices_validos, variables_select)

# Módulo del motor de consultas. Incluye funciones para leer, resolver y mostrar los resultados de las consultas.

import click


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

    if "where" not in texto_consulta:
        raise ValueError("La consulta no contiene la cláusula WHERE.")

    # Dividimos el texto de la consulta usando "where" como separador
    split_where = texto_consulta.split("where")

    if split_where[1] == "":
        raise ValueError("Cláusula WHERE vacía.")

    # Obtenemos las variables del select
    variables_select = [
        token.strip(",") for token in split_where[0].split() if token.startswith("?")
    ]

    if not variables_select:
        raise ValueError("No se encontraron variables en la cláusula SELECT.")

    # Obtenemos las tuplas con las sentencias del where
    sentencias = split_where[1].split("{")[1].split("}")[0]
    sentencias = [s.strip() for s in sentencias.split(".") if s.strip()]
    tuplas_where = [tuple(sentencia.split()) for sentencia in sentencias]

    if not tuplas_where:
        raise ValueError("No se encontraron sentencias en la cláusula WHERE.")
    for tupla in tuplas_where:
        if len(tupla) != 3:
            raise ValueError(
                f"La sentencia '{' '.join(tupla)}' no tiene exactamente 3 elementos."
            )

    return variables_select, tuplas_where


def es_variable(elemento):
    """Determina si un elemento de una tupla es una variable."""

    return elemento.startswith("?")


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

        if condicion_sujeto and condicion_relacion and condicion_objeto:
            respuestas.append(afirmacion)

    return respuestas


def imprimir_respuestas(variables_usadas, variables_select, indices_validos=None):
    """Imprime los valores de las variables de las respuestas en formato tabla.

    Parámetros:
    - variables_usadas (dict): diccionario con las respuestas para cada variable
    - variables_select (lista): lista con las variables a mostrar (ejemplo: '?asignatura', '?email')
    - indices_validos (set, opcional): conjunto con los índices válidos de las respuestas (si es None, se imprimen todas las respuestas)
    """
    if not variables_usadas:
        click.echo("No se han encontrado resultados.")
    else:
        # Calculamos el ancho máximo para cada columna
        max_width = []
        for variable in variables_select:
            max_len = max(
                len(str(key)) for key in variables_usadas.get(variable, {}).keys()
            )
            # Nos aseguramos de que la columna no sea más pequeña que el encabezado
            max_width.append(max(max_len, len(variable)))

        # Imprime los encabezados de la tabla
        header = (
            " | ".join(
                f"{var: <{max_width[i]}}" for i, var in enumerate(variables_select)
            )
            + " |"
        )
        print(header)
        print("-" * len(header))

        # Si hay índices válidos, solo imprimimos esos, sino todas las respuestas
        if indices_validos is None:
            # Imprime las respuestas de todas las variables sin filtro de índice
            respuestas = []
            for variable in variables_select:
                respuestas.append(list(variables_usadas.get(variable, {}).keys()))
            # Imprime las respuestas correspondientes de cada variable
            for i in range(len(respuestas[0])):
                fila = " | ".join(
                    f"{respuestas[j][i]: <{max_width[j]}}"
                    for j in range(len(respuestas))
                )
                print(fila + " |")
        else:
            # Si hay índices válidos, imprimimos solo las respuestas correspondientes a esos índices
            for indice in indices_validos:
                respuestas = []
                for variable in variables_select:
                    respuesta = [
                        clave
                        for clave, val in variables_usadas[variable].items()
                        if val == indice
                    ]
                    # Si la respuesta está vacía, se maneja como "None"
                    respuestas.append(
                        f"{respuesta[0] if respuesta else 'None': <{max_width[variables_select.index(variable)]}}"
                    )
                # Imprimimos las respuestas de las variables correspondientes al índice válido
                print(" | ".join(respuestas) + " |")
        print("")


def procesar_consulta(bc, texto_consulta):
    """Procesa una consulta a la base de conocimiento introducida por el usuario.

    Parámetros:
    - bc: lista de afirmaciones (tuplas) de la base de conocimiento
    - texto_consulta (string): consulta introducida por el usuario
    """

    try:
        # Parseamos el texto de la consulta
        variables_select, tuplas_where = leer_consulta(texto_consulta)
    except Exception as e:
        # Se detiene la ejecución
        print(f"Error: {e}")
        return

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

    # Si solo hay una consulta en WHERE, se imprime sin indices_validos
    if len(tuplas_where) == 1:
        imprimir_respuestas(variables_usadas, variables_select)
    else:
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
                                indice2 = variables_usadas[elemento][
                                    respuesta_valida[i]
                                ]
                                indices_validos.add(indice2)
                            else:
                                variables_usadas[elemento][
                                    respuesta_valida[i]
                                ] = indice2
                        else:
                            variables_usadas[elemento] = {}
                            variables_usadas[elemento][respuesta_valida[i]] = indice2
                            variable_nueva[i] = True

        # Si hay más de una consulta en WHERE, se pasa los indices_validos a la función
        imprimir_respuestas(variables_usadas, variables_select, indices_validos)

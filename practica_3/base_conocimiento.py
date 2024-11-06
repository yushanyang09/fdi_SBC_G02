def leer_base_conocimiento(base):
    """Lee el fichero de la base de conocimiento y devuelve
    un diccionario con toda la información que contiene.
    
    Parámetros:
    base (Path): ruta al fichero de la base de conocimiento"""

    # Diccionario que contendrá la base de conocimiento
    base_list=[]

    # Leemos el fichero que contiene la base de conocimiento
    with base.open("r", encoding="utf-8") as f:
        texto = f.read()

    # Leemos el archivo que contiene la base de conocimiento
    for line in texto.split("\n"):

        # Si es comentario o vacía
        if line.startswith("#") or not line:
            continue
        
        # Separamos los elementos de la línea
        line_items = line.split()
        if len(line_items) == 4:
            sujeto, predicado, objeto, fin = line_items
            # Si el sujeto no está en la base lo añadimos
            sujeto_auxiliar=sujeto
            afirmacion=(sujeto, predicado, objeto)
            anyadir_afirmacion(base_list, afirmacion)
        if len(line_items) == 3:
            predicado, objeto, fin = line_items
            afirmacion=(sujeto_auxiliar, predicado, objeto)
            anyadir_afirmacion(base_list, afirmacion)
    
    return base_list

def anyadir_afirmacion(base_list, afirmacion):
    """Añade una afirmación a la base de conocimiento.
    
    Parámetros:
    base_dict (dict): lista de la base de conocimiento
    sujeto (string): entidad que hace de sujeto de la afirmación
    predicado (string): relación de la afirmación
    objeto (string): entidad o atributo
    """
    if afirmacion not in base_list:
        base_list.append(afirmacion)
    return base_list
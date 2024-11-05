def leer_base_conocimiento(base):
    """Lee el fichero de la base de conocimiento y devuelve
    un diccionario con toda la información que contiene.
    
    Parámetros:
    base (Path): ruta al fichero de la base de conocimiento"""

    # Diccionario que contendrá la base de conocimiento
    base_dict = {}

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
            if sujeto not in base_dict:
                base_dict[sujeto] = {}
            anyadir_afirmacion(base_dict, sujeto, predicado, objeto)
            
        elif len(line_items) == 3:
            predicado, objeto, fin = line_items
            anyadir_afirmacion(base_dict, sujeto, predicado, objeto)
    
    return base_dict

def anyadir_afirmacion(base_dict, sujeto, predicado, objeto):
    """Añade una afirmación a la base de conocimiento.
    
    Parámetros:
    base_dict (dict): diccionario de la base de conocimiento
    sujeto (string): entidad que hace de sujeto de la afirmación
    predicado (string): relación de la afirmación
    objeto (string): entidad o atributo
    """
            
    # Si el predicado existe, añadimos el objeto
    if predicado in base_dict[sujeto]:
        # El objeto se añade solo si no estaba ya en el set (para evitar repetidos)
        base_dict[sujeto][predicado].add(objeto)

    # Si no, añadimos la relación y el objeto
    else:
        base_dict[sujeto][predicado] = set() # conjunto
        base_dict[sujeto][predicado].add(objeto)
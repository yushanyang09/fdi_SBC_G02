
import re
def leer_base_conocimiento(base):
    """Lee el fichero de la base de conocimiento y devuelve
    una lista de tuplas con toda la información que contiene.
    
    Parámetros:
    base (Path): ruta al fichero de la base de conocimiento
    """

    # Lista que contendrá la base de conocimiento
    base_list = []

    # Leemos el fichero que contiene la base de conocimiento
    with base.open("r", encoding="utf-8") as f:
        texto = f.read()

    # Filtramos las líneas que no son comentarios ni líneas vacías
    lineas = [linea for linea in texto.split('\n') if not linea.startswith('#') and linea.strip()]

    # Juntamos las líneas filtradas
    texto_filtrado = ' '.join(lineas)

    # Utilizamos expresiones regulares para separar por el '.' del final especificamente (por si hay problemas con correos
    # u otros posibles atributos)
    # Cada sección corresponde a un sujeto
    secciones = [seccion.strip() for seccion in re.split(r'\s*\.\s*(?=\w+:|$)', texto_filtrado) if seccion.strip()]

    # Para cada sección
    for seccion in secciones:

        # Dividimos la sección en afirmaciones usando ';' como separador
        afirmaciones = [afirmacion.strip() for afirmacion in seccion.split(';') if afirmacion.strip()]

        if afirmaciones:
            # Extraemos el sujeto de la primera afirmación
            sujeto, predicado, objeto = afirmaciones[0].split()
            anyadir_afirmacion(base_list, (sujeto, predicado, objeto))

            # El resto de las afirmaciones tienen el mismo sujeto
            for afirmacion_parcial in afirmaciones[1:]:
                predicado, objeto = afirmacion_parcial.split()
                anyadir_afirmacion(base_list, (sujeto, predicado, objeto))
    
    return base_list

def anyadir_afirmacion(base_list, afirmacion):
    """Añade una afirmación a la base de conocimiento.
    
    Parámetros:
    base_list (lista): lista de la base de conocimiento
    afirmacion (tupla): contiene 3 elementos:
        - sujeto (string): entidad que hace de sujeto de la afirmación
        - predicado (string): relación de la afirmación
        - objeto (string): entidad o atributo
    """
    
    if afirmacion not in base_list:
        base_list.append(afirmacion)
    return base_list

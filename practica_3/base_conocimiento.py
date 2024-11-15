import re
from pathlib import Path

def leer_base_conocimiento(base):
    """Lee el fichero de la base de conocimiento y devuelve
    una lista de tuplas con toda la información que contiene.
    
    Parámetros:
    - base (Path): ruta al fichero de la base de conocimiento
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
    - base_list (lista): lista de la base de conocimiento
    - afirmacion (tupla): contiene 3 elementos:
        - sujeto (string): entidad que hace de sujeto de la afirmación
        - predicado (string): relación de la afirmación
        - objeto (string): entidad o atributo
    
    Devuelve:
    La base de la base con la afirmación añadida.
    """
    
    if afirmacion not in base_list:
        base_list.append(afirmacion)
    return base_list

def combinar_bases(bases):
    """Combina las bases introducidas por consola.
    
    Parámetros:
    - bases (Path): rutas a los ficheros de las bases de conocimiento

    Devuelve:
    Una lista con toda la información mezclada.
    """

    # Lista que contendrá la base de conocimiento
    bc_combinada = []

    # Cargamos cada fichero de base de conocimiento y los mezclamos
    for base in bases:
        bc = leer_base_conocimiento(base)
        bc_combinada.extend(bc)
    
    return bc_combinada

def load(comando, bc):
    """Carga una nueva base de conocimiento en tiempo real.
    
    Parámetros:
    - comando (string): contiene el nombre del archivo de la nueva base
    - bc (lista): la base de conocimiento actual

    Devuelve:
    La base de conocimiento extendida con la nueva base.
    """

    archivo = comando.split()[1]
    nueva_bc = leer_base_conocimiento(Path(archivo))
    bc.extend(nueva_bc)

    return bc

def add(comando, bc):
    """Añade una nueva afirmación a la base de conocimiento en tiempo de
    ejecución.

    Parámetros:
    - comando (string): contiene el comando con la nueva afirmación
    - bc (lista): la base de conocimiento actual

    Devuelve:
    La base de conocimiento extendida con la nueva afirmación.
    """

    afirmacion_list = []

    try:
        afirmacion = comando.split()
        
        if len(afirmacion[1:]) != 3:
            raise ValueError("La afirmación debe contener exactamente tres elementos (sujeto, predicado y objeto).")

        sujeto, predicado, objeto = afirmacion[1:]
        anyadir_afirmacion(afirmacion_list, (sujeto, predicado, objeto))
        bc.extend(afirmacion_list)

    except ValueError as e:
        print(f"Advertencia: {e}")

    return bc

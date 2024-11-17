# Módulo con funciones relacionadas con el manejo de la/s base/s de conocimiento
# También incluye las funciones que implementan algunos de los comandos de la funcionalidad opcional de la práctica

import re
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt

def leer_base_conocimiento(base):
    """Lee el fichero de la base de conocimiento y devuelve una lista de tuplas con toda la información que contiene.
    
    Parámetros:
    - base (Path): ruta al fichero de la base de conocimiento
    """

    # Verificar si la base es un Path válido
    if not isinstance(base, Path):
        raise ValueError("El parámetro 'base' debe ser una ruta de archivo válida.")

    # Lista que contendrá la base de conocimiento
    base_list = []

    # Leemos el fichero que contiene la base de conocimiento
    try:
        with base.open("r", encoding="utf-8") as f:
            texto = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo '{base}' no se encuentra.")
    except IOError as e:
        raise IOError(f"No se pudo leer el archivo '{base}': {e}")

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

        try:
                # Extraemos el sujeto de la primera afirmación
                sujeto, predicado, objeto = afirmaciones[0].split()

                # Añadimos la afirmación a la base de conocimiento
                anyadir_afirmacion(base_list, (sujeto, predicado, objeto))

                # El resto de las afirmaciones tienen el mismo sujeto
                for afirmacion_parcial in afirmaciones[1:]:
                    predicado, objeto = afirmacion_parcial.split()
                    anyadir_afirmacion(base_list, (sujeto, predicado, objeto))

        except ValueError:
            raise ValueError(f"Error en el formato de las afirmaciones de la base.")
    
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
        try:
            bc = leer_base_conocimiento(base)
        except Exception as e:
            # Se detiene la ejecución
            print(f"Error: {e}")
            print("Introduce una base válida.")
            return

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
    try:
        nueva_bc = leer_base_conocimiento(Path(archivo))
    except Exception as e:
            # Se detiene la ejecución
            print(f"Error: {e}")
            return
    
    bc.extend(nueva_bc)

    return bc

def add(comando, bc):
    """Añade una nueva afirmación a la base de conocimiento en tiempo de ejecución.

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
        print(f"Error: {e}")

    return bc

def save(comando, afirmaciones):
    """Guarda la base de conocimiento actual en un archivo de texto.
    
    Parámetros:
    - afirmaciones (list): lista de tuplas donde cada tupla es una afirmación (sujeto, predicado, objeto)
    - archivo_salida (str): ruta del archivo de salida
    """

    # Si el formato del comando es erróneo, lanzamos una excepción
    try:
        archivo_salida = comando.split()

        if len(archivo_salida) != 2:
            raise ValueError("El formato del comando es erróneo. Asegurate de introducir 'save <archivo>.txt'")
        
        archivo_salida = archivo_salida[1]

        # Diccionario para agrupar las afirmaciones por sujeto
        afirmaciones_por_sujeto = {}

        # Agrupamos las afirmaciones
        for sujeto, predicado, objeto in afirmaciones:
            if sujeto not in afirmaciones_por_sujeto:
                afirmaciones_por_sujeto[sujeto] = []
            afirmaciones_por_sujeto[sujeto].append((predicado, objeto))

        # Escribimos las afirmaciones en el archivo
        with open(archivo_salida, 'w', encoding='utf-8') as archivo:
            for sujeto, predicados_objetos in afirmaciones_por_sujeto.items():
                archivo.write(f"{sujeto} ")

                for i, (predicado, objeto) in enumerate(predicados_objetos):
                    separador = " ;\n\t" if i < len(predicados_objetos) - 1 else " .\n"
                    archivo.write(f"{predicado} {objeto}{separador}")
                archivo.write("\n")
        print(f'El archivo se ha guardado como {archivo_salida}')

    except ValueError as e:
        print(f"Error: {e}")

def draw(comando, afirmaciones):
    """Crea y guarda un grafo en formato PNG a partir de una lista de tuplas (afirmaciones). NOTA: según el enunciado, 
    deben poder visualizarse los resultados de la última consulta realizada. Por falta de tiempo solo mostramos el grafo
    completo de la base de conocimiento.

    Parámetros:
    - afirmaciones (list): lista de tuplas donde cada tupla es una afirmación (sujeto, predicado, objeto)
    - nombre_archivo (str): nombre del archivo png de salida
    """

    # Si el formato del comando es erróneo, lanzamos una excepción
    try:
        nombre_archivo = comando.split()

        if len(nombre_archivo) != 2:
            raise ValueError("El formato del comando es erróneo. Asegurate de introducir 'draw <archivo>.png'")
        
        nombre_archivo = nombre_archivo[1]

        # Creamos un grafo dirigido
        G = nx.DiGraph()

        # Añadimos nodos y aristas al grafo a partir de las afirmaciones
        for sujeto, predicado, objeto in afirmaciones:
            G.add_node(sujeto)
            G.add_node(objeto)
            G.add_edge(sujeto, objeto, label=predicado)

        # Dibujamos el grafo
        pos = nx.spring_layout(G, k=0.5, iterations=50)  # Disposición de los nodos
        plt.figure(figsize=(12, 8))

        # Dibujamos los nodos y las aristas
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', font_size=10, font_weight='bold')

        # Dibujamos las etiquetas de las aristas
        #edge_labels = nx.get_edge_attributes(G, 'label')
        #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

        # Guardamos la imagen como un archivo PNG
        plt.savefig(nombre_archivo)
        plt.close()
        print(f'El grafo se ha guardado como {nombre_archivo}')

    except ValueError as e:
        print(f"Error: {e}")

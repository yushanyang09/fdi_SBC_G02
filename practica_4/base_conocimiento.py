from pathlib import Path


def leer_base_conocimiento(base):
    """Lee el fichero de la base de conocimiento.

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

    return texto

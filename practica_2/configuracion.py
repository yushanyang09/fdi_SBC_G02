import tomllib
from pathlib import Path


def modificar_configuracion(toml: Path):
    """Función para leer, modificar y guardar la configuración TOML

    IMPORTANTE: el idioma y la lógica difusa no se modifican, solo lo hemos puesto para
    que se vea que el archivo config.toml se modifica con éxito

    """
    # Lee la configuración inicial del archivo TOML
    with toml.open("rb") as f:
        data = tomllib.load(f)
        print("Configuración inicial:", data)

    # Solicita al usuario que modifique los valores
    idioma = input("Nuevo idioma (dejar vacío para no cambiar): ")
    if idioma:
        data["language"] = idioma

    limite_inferior = input(
        "Nuevo límite inferior. Por defecto 0.3 (dejar vacío para no cambiar): "
    )
    if limite_inferior:
        data["rango_respuesta"]["inferior"] = float(limite_inferior)

    limite_superior = input(
        "Nuevo límite superior. Por defecto 0.7 (dejar vacío para no cambiar): "
    )
    if limite_superior:
        data["rango_respuesta"]["superior"] = float(limite_superior)

    logica_difusa = input("Nueva lógica difusa (dejar vacío para no cambiar): ")
    if logica_difusa:
        data["logica_difusa"] = logica_difusa

    # Guarda la nueva configuración
    with toml.open("w", encoding="utf-8") as f:
        f.write(f'language = "{data["language"]}"\n')
        f.write(
            f'rango_respuesta = {{"inferior"= {data["rango_respuesta"]["inferior"]}, "superior"= {data["rango_respuesta"]["superior"]}}}\n'
        )
        f.write(f'logica_difusa = "{data["logica_difusa"]}"\n')

    print("Configuración final:", data)
    print()

    return data

# Importamos librerías
from pathlib import Path
import click

# Importamos módulos
import base_conocimiento

@click.command()
@click.argument("base", type=click.Path(exists=True, path_type=Path))

def main(base: Path):

    # Leemos el fichero que contiene la base de conocimiento
    with base.open("r", encoding="utf-8") as f:
        texto = f.read()

    # Leemos el archivo que contiene la base de conocimiento
    for line in texto.split("\n"):

        if line.startswith("#") or not line:
            continue

        
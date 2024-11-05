# Importamos librerías
from pathlib import Path
import click

# Importamos módulos
import base_conocimiento

@click.command()
@click.argument("base", type=click.Path(exists=True, path_type=Path))

def main(base: Path):

    bc = base_conocimiento.leer_base_conocimiento(base)

    print(bc)

if __name__ == "__main__":
    main()
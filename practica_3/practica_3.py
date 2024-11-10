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
    print("Introduzca la consulta")
    consulta = "select ?persona where{ ?persona t2:casado_con q2:eddard_stark}"
    print(consulta)
    base_conocimiento.leer_consulta(consulta)

if __name__ == "__main__":
    main()
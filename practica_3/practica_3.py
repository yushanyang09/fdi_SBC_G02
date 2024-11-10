# Importamos librerías
from pathlib import Path
import click
# Importamos módulos
import base_conocimiento
import motor_consultas

@click.command()
@click.argument("base", type=click.Path(exists=True, path_type=Path))

def main(base: Path):

    bc = base_conocimiento.leer_base_conocimiento(base)

    print("BIENVENIDO! \U0001F600")
    print("Introduce un comando:")
    consulta = input()

    # Mientras la consulta no sea "exit", continúa la ejecución
    while consulta != "exit":
        if consulta.startswith("select"):
            motor_consultas.procesar_consulta(bc, consulta)
        
        print("Introduce un comando:")
        consulta = input()

if __name__ == "__main__":
    main()
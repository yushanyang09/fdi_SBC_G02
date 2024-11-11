# Importamos librerías
from pathlib import Path
import click
# Importamos módulos
import base_conocimiento
import motor_consultas

@click.command()
# Se usa nargs=-1 para aceptar uno o varios argumentos de archivo
@click.argument("bases", type=click.Path(exists=True, path_type=Path), nargs=-1)

def main(bases):

    # Verificamos si no se ha pasado ninguna base de conocimiento
    if not bases:
        print("Error: No se ha especificado ninguna base de conocimiento. Indica al menos un archivo.")
        return

    # Lista que contendrá la base de conocimiento
    bc_combinada = []

    # Cargamos cada fichero de base de conocimiento y los mezclamos
    for base in bases:
        bc = base_conocimiento.leer_base_conocimiento(base)
        bc_combinada.extend(bc)

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
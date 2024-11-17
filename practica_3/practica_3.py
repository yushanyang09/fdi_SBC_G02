# Importamos librerías
from pathlib import Path
import click
# Importamos módulos
import base_conocimiento
import motor_consultas
import interfaz

@click.command()
# Se usa nargs=-1 para aceptar uno o varios argumentos de archivo
@click.argument("bases", type=click.Path(exists=True, path_type=Path), nargs=-1)

def main(bases):
    """Este sistema permite cargar una o varias redes semánticas y realizar consultas sobre 
    las relaciones entre las distintas entidades y relaciones.

    Para ejecutar el programa en tu terminal introduce el siguiente comando: \n
    uv run practica3.py <base_conocimiento_1> ... <base_conocimiento_n> <toml>

    Argumentos:\n
        base_conocimiento: nombre del fichero que contiene una base de conocimiento a utilizar\n
        toml: archivo de configuración con la extensión toml

    Comandos:\n
        select <?variable1>,...,<?variableN> where { q2:sujeto t2:relacion ?variable1 . }: hace una consulta a la base de conocimiento\n
        load <archivo.txt>: añade una nueva base de conocimiento al sistema\n
        add <sujeto relacion objeto>: añade una nueva afirmación a la base de conocimiento\n
        help: muestra la ayuda al usuario\n
        exit: termina la ejecución del programa
    """

    if not bases:
        interfaz.error_bases()
        return

    bc = base_conocimiento.combinar_bases(bases)

    interfaz.bienvenida()

    consulta = interfaz.introducir_comando()

    # Mientras la consulta no sea "exit", continúa la ejecución
    while consulta != "exit":
        if consulta.startswith("select"):
            motor_consultas.procesar_consulta(bc, consulta)
        elif consulta == "help":
            interfaz.imprimir_ayuda()
        elif consulta.startswith("load"):
            bc = base_conocimiento.load(consulta, bc)
        elif consulta.startswith("add"):
            bc = base_conocimiento.add(consulta, bc)
        elif consulta.startswith("save"):
            bc = base_conocimiento.save(consulta, bc)
        else:
            interfaz.comando_no_valido()
        
        consulta = interfaz.introducir_comando()

if __name__ == "__main__":
    main()
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
    uv run practica3.py <base_conocimiento_1> ... <base_conocimiento_n>

    Argumentos:\n
        base_conocimiento: nombre del fichero que contiene una base de conocimiento a utilizar\n

    Comandos:\n
        select <?variable1>,...,<?variableN> where { q2:sujeto t2:relacion ?variable1 . }: hace una consulta a la base de conocimiento\n
        load <archivo.txt>: añade una nueva base de conocimiento al sistema\n
        add <sujeto relacion objeto>: añade una nueva afirmación a la base de conocimiento\n
        save <ruta_archivo>: guarda la base de datos actual en la ruta especificada\n
        draw <ruta_archivo>: guarda un grafo de la base de conocimiento actual en la ruta especificada\n
        help: muestra la ayuda al usuario\n
        exit: termina la ejecución del programa
    """

    if not bases:
        interfaz.error_bases()
        return
    else:
        bc = base_conocimiento.combinar_bases(bases)

        if bc:
            interfaz.bienvenida()

            comando = interfaz.introducir_comando()

            # Mientras la consulta no sea "exit", continúa la ejecución
            while comando != "exit":
                if comando.startswith("select"):
                    motor_consultas.procesar_consulta(bc, comando)
                elif comando == "help":
                    interfaz.imprimir_ayuda()
                elif comando.startswith("load"):
                    bc = base_conocimiento.load(comando, bc)
                elif comando.startswith("add"):
                    bc = base_conocimiento.add(comando, bc)
                elif comando.startswith("save"):
                    base_conocimiento.save(comando, bc)
                elif comando.startswith("draw"):
                    base_conocimiento.draw(comando, bc)
                else:
                    interfaz.comando_no_valido()

                comando = interfaz.introducir_comando()


if __name__ == "__main__":
    main()

from pathlib import Path
import click

import base_conocimiento
import interfaz
import configuracion


@click.command()
@click.argument("base", type=click.Path(exists=True, path_type=Path))
@click.argument("toml", type=click.Path(exists=True, path_type=Path))
def main(base: Path, toml: Path):
    """Este sistema está basado en reglas y es capaz de realizar razonamiento
    hacia atrás (backward chaining), incorporando lógica difusa

    Para ejecutar el programa en tu terminal introduce el siguiente comando:

    uv run practica2.py <base_conocimiento> <toml>

    Argumentos:

        base_conocimiento: nombre del fichero que contiene la base de conocimiento a utilizar

        toml: archivo de configuración con la extensión toml

    Comandos:

        <consulta>?: hace una consulta a la base de conocimiento

        add <nombre_hecho> [<grado_verdad>]: añade a la base de conocimiento un hecho llamado nombre_hecho con grado_v (float) como grado de verdad

        help: muestra la ayuda al usuario

        exit: termina la ejecución del programa

    """

    bc = base_conocimiento.BaseConocimiento()

    data_modificado = configuracion.modificar_configuracion(toml)

    bc = base_conocimiento.leer_base_conocimiento(base, bc)

    interfaz.bienvenida()

    consulta = interfaz.introducir_comando()

    # Mientras la consulta no sea "exit", continúa la ejecución
    while consulta != "exit":
        if consulta == "print":
            bc.imprimir()
        elif consulta == "help":
            interfaz.imprimir_ayuda()
        elif consulta.startswith("add"):
            try:
                consulta = consulta.split()
                hecho = consulta[1]
                # Verificamos si se ha proporcionado un grado de verdad
                if len(consulta) < 3:
                    # Si no hay grado de verdad, asumimos el valor por defecto (1.0)
                    grado_verdad = 1.0
                    interfaz.grado_no_especificado(grado_verdad)
                else:
                    grado_verdad = float(consulta[2].strip("[]"))
                bc.agregar_hecho(hecho, grado_verdad)
            except (IndexError, ValueError):
                interfaz.formato_incorrecto()
        elif consulta.endswith("?"):
            bc.seguimiento = []
            devuelto = bc.backward_chain(consulta.strip("?"))
            if devuelto == -1:
                print("No")
            else:
                if devuelto >= data_modificado["rango_respuesta"]["superior"]:
                    p = "mucho"
                elif devuelto <= data_modificado["rango_respuesta"]["inferior"]:
                    p = "poco"
                else:
                    p = "intermedio"
                print(f"Si, {p} ({devuelto})")
                bc.imprimir_derivacion()
        else:
            interfaz.comando_no_valido()

        consulta = interfaz.introducir_comando()


if __name__ == "__main__":
    main()

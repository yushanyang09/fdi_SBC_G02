# Modulo para manejar la interacción del sistema con el usuario en la consola

import click


def error_bases():
    print(
        "Error: No se ha especificado ninguna base de conocimiento. Indica al menos un archivo."
    )


def bienvenida():
    print("BIENVENIDO! \U0001F600")


def introducir_comando():
    """Permite introducir comandos en una sola línea o múltiples líneas si terminan con `}`."""
    print("Introduce tu comando (finaliza con '}' si es multilinea):")

    # Inicializamos las variables para acumular líneas
    comando = []
    while True:
        linea = input()
        comando.append(linea.strip())

        # Si la última línea contiene '}', asumimos que el comando está completo
        if linea.strip().endswith("}"):
            break

    # Unimos las líneas en un único comando
    return " ".join(comando)


def imprimir_ayuda():
    """Imprime la ayuda al usuario definida como docstring en el main"""
    ctx = click.get_current_context()
    click.echo(ctx.get_help())


def comando_no_valido():
    print("Comando no válido \U0001F622")

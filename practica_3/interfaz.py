# Modulo para manejar la interacción del sistema con el usuario en la consola

import click

def error_bases():
    print("Error: No se ha especificado ninguna base de conocimiento. Indica al menos un archivo.")

def bienvenida():
    print("BIENVENIDO! \U0001F600")

def introducir_comando():
    print("Introduce un comando:")
    return input()

def imprimir_ayuda():
    """Imprime la ayuda al usuario definida como docstring en el main"""
    ctx = click.get_current_context()
    click.echo(ctx.get_help())

def comando_no_valido():
    print("Comando no válido \U0001F622")

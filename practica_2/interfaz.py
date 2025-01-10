# Módulo para manejar la interacción del sistema con el usuario en la consola

import click


def bienvenida():
    """Imprime el mensaje de bienvenida."""
    click.echo("BIENVENIDO! \U0001F600")


def imprimir_ayuda():
    """Imprime la ayuda al usuario definida como docstring en el main"""
    ctx = click.get_current_context()
    click.echo(ctx.get_help())


def introducir_comando():
    """Permite al usuario introducir un comando"""
    return click.prompt("Introduce un comando")


def comando_no_valido():
    """Imprime un mensaje de error si el comando introducido no es válido."""
    click.echo("Comando no válido \U0001F622")


def formato_incorrecto():
    """Imprime un mensaje de error si el formato introducido no es válido."""
    click.echo("Formato incorrecto \U0001F620. Usa 'add <hecho> [<grado_verdad>]'")


def grado_no_especificado(grado_verdad):
    """Imprime el grado de verdad por defecto si no se ha especificado ninguno."""
    click.echo(f"Grado de verdad no especificado, se asume {grado_verdad}")

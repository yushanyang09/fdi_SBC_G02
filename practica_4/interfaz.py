# Módulo para manejar la interacción del sistema con el usuario en la consola

import click


def error_bases():
    """Imprime un mensaje de error si no se ha especificado ninguna base."""
    click.echo(
        "Error: No se ha especificado ninguna base de conocimiento. Indica al menos un archivo."
    )


def bienvenida():
    """Imprime el mensaje de bienvenida."""
    click.echo("BIENVENIDO! \U0001F600")


def introducir_comando():
    """Permite al usuario introducir un comando"""
    return click.prompt("Introduce un comando")


def imprimir_ayuda():
    """Imprime la ayuda al usuario definida como docstring en el main"""
    ctx = click.get_current_context()
    click.echo(ctx.get_help())


def comando_no_valido():
    """Imprime un mensaje de error si el comando introducido no es válido."""
    click.echo("Comando no válido \U0001F622")


def pregunta_modelo():
    """Pregunta al usuario sobre el modelo a utilizar"""
    mod = click.prompt("¿Qué modelo de Ollama quieres utilizar? (Por defecto: llama3.2:1b)", default="llama3.2:1b", show_default=False)
    if mod == "llama3.2:1b":
        click.echo("Se usará el modelo llama3.2:1b")
    else:
        click.echo(f"Se usará el modelo {mod}")
    return mod


def pregunta_chain_of_thought():
    """Pregunta al usuario sobre el uso de Chain of Thought"""
    cot = click.prompt("¿Quieres utilizar Chain of Thought? (y/n)")
    if cot == "y":
        click.echo("El modelo usará Chain of Thought")
    else:
        click.echo("El modelo no usará Chain of Thought")
    return cot

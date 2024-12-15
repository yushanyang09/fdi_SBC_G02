# Importamos librerías
from pathlib import Path
import click
from ollama import chat

# Importamos módulos
import interfaz
import modelo
import base_conocimiento
import rag

@click.command()
# Se usa nargs=-1 para aceptar uno o varios argumentos de archivo
@click.argument("bases", type=click.Path(exists=True, path_type=Path), nargs=-1)
def main(bases):
    """Este sistema implementa un asistente virtual usando grandes modelos de lenguaje (LLMs).

    Para ejecutar el programa en tu terminal introduce el siguiente comando: \n
    uv run practica_4.py <base_conocimiento>

    Argumentos:\n
        base_conocimiento: ruta al fichero que contiene una base de conocimiento a utilizar\n

    Comandos:\n
        help: muestra la ayuda al usuario\n
        exit: termina la ejecución del programa
    
    Para hacer una pregunta al asistente el usuario podrá escribir consultas en formato libre (en inglés).
    """

    if not bases:
        interfaz.error_bases()
        return
    else:
        for base in bases:
            bc = base_conocimiento.leer_base_conocimiento(base)

        interfaz.bienvenida()
        
        #rag.dividir_base_conocimiento(bc)
        #rag.dividir_base_conocimiento_2(bc)

        mod = interfaz.pregunta_modelo()

        cot = interfaz.pregunta_chain_of_thought()

        comando = interfaz.introducir_comando()

        # Mientras la consulta no sea "exit", continúa la ejecución
        while (comando.lower() != "exit"):

            if comando == "help":
                    interfaz.imprimir_ayuda()
            else:
                if cot == "y":
                    modelo.consulta_chain_of_thought(bc, comando, mod)
                else:
                    modelo.consulta(bc, comando, mod)

            comando = interfaz.introducir_comando()

if __name__ == "__main__":
    main()
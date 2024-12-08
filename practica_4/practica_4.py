# Importamos librerías
from pathlib import Path
import click
from ollama import chat

# Importamos módulos
import interfaz
import modelo
import base_conocimiento

@click.command()
# Se usa nargs=-1 para aceptar uno o varios argumentos de archivo
@click.argument("bases", type=click.Path(exists=True, path_type=Path), nargs=-1)
def main(bases):

    if not bases:
        interfaz.error_bases()
        return
    else:
        for base in bases:
            bc = base_conocimiento.leer_base_conocimiento(base)
        
        #modelo.iniciar_modelo(bc)

        comando = interfaz.introducir_comando()

        while (comando.lower() != "exit"):
            #modelo.consulta(comando)
            modelo.consulta_sin_historial(bc, comando)
            comando = interfaz.introducir_comando()

if __name__ == "__main__":
    main()
# Práctica 2

Integrantes:
- Carmen Fernández
- Yushan Yang

En esta práctica implementamos un sistema basado en reglas y capaz de realizar razonamiento
hacia atrás (backward chaining), incorporando lógica difusa.
    
Para ejecutar el programa en tu terminal introduce el siguiente comando:

`uv run practica2.py <base_conocimiento> <toml>`

Argumentos:

    base_conocimiento: nombre del fichero que contiene la base de conocimiento a utilizar
    
    toml: archivo de configuración con la extensión toml

Comandos:

    <consulta>?: hace una consulta a la base de conocimiento

    add <nombre_hecho> [<grado_verdad>]: añade a la base de conocimiento un hecho llamado nombre_hecho con grado_v (float) como grado de verdad

    help: muestra la ayuda al usuario

    exit: termina la ejecución del programa
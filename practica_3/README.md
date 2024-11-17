# Práctica 3

En esta práctica implementamos un sistema que permite cargar una o varias redes semánticas y realizar consultas sobre 
las relaciones entre las distintas entidades y relaciones.

Para ejecutar el programa en tu terminal introduce el siguiente comando:

`uv run practica3.py <base_conocimiento_1> ... <base_conocimiento_n>`

Argumentos:

    base_conocimiento: nombre del fichero que contiene una base de conocimiento a utilizar

Comandos:

    select <?variable1>,...,<?variableN> where { q2:sujeto t2:relacion ?variable1 . }: hace una consulta a la base de conocimiento

    load <archivo.txt>: añade una nueva base de conocimiento al sistema

    add <sujeto relacion objeto>: añade una nueva afirmación a la base de conocimiento

    save <ruta_archivo>: guarda la base de datos actual en la ruta especificada

    draw <ruta_archivo>: guarda un grafo de la base de conocimiento actual en la ruta especificada

    help: muestra la ayuda al usuario

    exit: termina la ejecución del programa

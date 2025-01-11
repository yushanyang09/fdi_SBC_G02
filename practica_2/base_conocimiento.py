import regla


class BaseConocimiento:
    """Representa la base de conocimiento

    Atributos:
    reglas (list): lista de reglas de la base de conocimiento
    hechos (dict): lista de hechos de la base de conocimiento y sus grados de verdad
    seguimiento (list): reglas seguidas en la derivación de la consulta

    """

    def __init__(self):
        """Inicializa una base de conocimiento

        Parámetros:
        reglas (list): lista de reglas de la base de conocimiento
        hechos (dict): lista de hechos de la base de conocimiento y sus grados de verdad
        seguimiento (list): reglas seguidas en la derivación de la consulta

        """
        self.reglas = []
        self.hechos = {}
        self.seguimiento = []

    def agregar_regla(self, regla):
        """Añade una regla a la base de conocimiento

        Parámetros:
        regla (Regla): regla que se quiere añadir

        """
        self.reglas.append(regla)

    def agregar_hecho(self, hecho, grado_v=1.0):
        """Añade un hecho a la base de conocimiento

        Parámetros:
        hecho (string): hecho que se quiere añadir
        grado_v (float): grado de verdad del hecho

        """
        self.hechos[hecho] = grado_v

    def imprimir(self):
        """Imprime las reglas y los hechos de la base de conocimiento"""
        for regla in self.reglas:
            regla.imprimir()
        for hecho in self.hechos:
            print(hecho + " [" + str(self.hechos[hecho]) + "]")

    def imprimir_derivacion(self, consulta, grado_final):
        """Imprime las reglas seguidas en la derivación de una consulta"""

        print("\nÁrbol de derivación:")
        print(f"{consulta} ({grado_final})")
        self.imprimir_nodo(consulta)
        print()
    
    def imprimir_nodo(self, consulta, nivel=0, visitados=None):
        """Imprime el árbol de derivación recursivamente."""
        # Guardamos los nodos ya visitados para que no se repitan en la salida
        if visitados is None:
            visitados = set()
        # Espaciado inicial para diferenciar los niveles del árbol
        indentacion = " " * nivel
        # Para cada elemento de la variable seguimiento
        for entrada in self.seguimiento:
            if entrada["regla"].cons == consulta and entrada["regla"] not in visitados:
                visitados.add(entrada["regla"])
                regla = entrada["regla"]
                print(f"{indentacion}|--Regla: {regla.cons} :- {' AND '.join(regla.antecedentes)} [{regla.grado_verdad}] ({entrada['resultado_regla']:.1f})")
                # Para cada antecedente de la regla
                for antecedente in entrada["antecedentes_aplicados"]:
                    print(f"{indentacion} |--{antecedente['antecedente']} ({antecedente['grado']:.1f})")
                    self.imprimir_nodo(antecedente["antecedente"], nivel + 4, visitados)

    def AND_(self, grados):
        """Devuelve el resultado de un AND en lógica difusa (valor mínimo)

        Parámetros:
        grados (list): lista de los grados de los antecedentes

        """
        return min(grados)

    def OR_(self, grados):
        """Devuelve el resultado de un OR en lógica difusa (valor máximo)

        Parámetros:
        grados (list): lista de los grados de las reglas

        """
        return max(grados)

    # Realiza razonamiento hacia atrás
    def backward_chain(self, consulta):
        """Realiza razonamiento hacia atrás con lógica difusa

        Parámetros:
        consulta (string): consulta introducida por el usuario

        Devuelve:
        -1: si no se cumple la consulta
        float: grado de verdad de la consulta

        """

        # Si la consulta ya está en los hechos conocidos, no hay necesidad de seguir
        if consulta in self.hechos:
            return self.hechos[consulta]

        grados_reglas = []  # almacena los grados de cada regla válida

        # Recorremos las reglas
        for regla in self.reglas:
            
            # Si el consecuente coincide con la consulta
            if regla.cons == consulta:
                ok = True
                grado_v = regla.grado_verdad  # grado de verdad de la regla
                grados_antecedentes = [] # almacena los grados de los antecedentes válidos

                regla_aplicada = {
                    "regla": regla,
                    "antecedentes_aplicados": [],
                    "resultado_regla": None
                }  # para mostrar que reglas hemos aplicado

                # Recorremos los antecedentes de la regla
                for antecedente in regla.antecedentes:
                    # Si un antecedente no está en los hechos, intentamos derivarlo recursivamente
                    devuelto = self.backward_chain(antecedente)

                    # Si no se cumple, lo indicamos con la variable ok
                    if devuelto == -1:
                        ok = False
                    # Si el antecedente es un hecho, almacenamos su grado
                    else:
                        # Guardamos el antecedente aplicado
                        grados_antecedentes.append(devuelto)
                        regla_aplicada["antecedentes_aplicados"].append(
                            {"antecedente": antecedente, "grado": devuelto}
                        )  

                # Si todos los antecedentes se cumplen, la consulta también se cumple
                if ok:
                    resultado_regla = self.AND_([grado_v, self.AND_(grados_antecedentes)])
                    grados_reglas.append(resultado_regla)
                    regla_aplicada["resultado_regla"] = resultado_regla
                    self.seguimiento.append(regla_aplicada)

        if len(grados_reglas) != 0:
            resultado_final = self.OR_(grados_reglas)
            # self.seguimiento.append(
            #     {"consulta": consulta, "resultado_final": resultado_final}
            # )  # Guardamos el resultado para la consulta actual
            return resultado_final
        else:
            return -1


def leer_base_conocimiento(base, bc):

    # Leemos el fichero que contiene la base de conocimiento
    with base.open("r", encoding="utf-8") as f:
        texto = f.read()

    # Leemos el archivo que contiene la base de conocimiento
    for line in texto.split("\n"):
        if line.startswith("#") or not line:
            continue

        # Separamos el consecuente
        cons, resto = line.split(":-")
        cons = cons.strip()  # elimina los espacios en blanco

        # Buscamos si hay un grado de verdad entre corchetes
        if "[" in resto and "]" in resto:
            # Separamos los antecedentes y el grado de verdad
            antecedentes, grado_verdad = resto.split("[")
            grado_verdad = grado_verdad.rstrip("]").strip()
            grado_verdad = float(grado_verdad)
            antecedentes = antecedentes.split(",")
            antecedentes = [a.strip() for a in antecedentes]
            # Añadimos la regla a la base de conocimiento
            r = regla.Regla(cons, antecedentes, grado_verdad)
            bc.agregar_regla(r)
        else:
            # Separamos los antecedentes
            antecedentes = resto.split(",")
            antecedentes = [a.strip() for a in antecedentes]
            # Añadimos la regla a la base de conocimiento
            r = regla.Regla(cons, antecedentes)
            bc.agregar_regla(r)

    return bc

from pathlib import Path
import tomllib 
import click

class Regla:
    """Representa una regla de la base de conocimiento

    Atributos:
    cons (string): consecuente de la regla
        antecedentes (list): antecedentes de la regla
        grado_v (float): valor del grado de verdad
    """
    def __init__(self, cons, antecedentes, grado_v=1.0):
        """Inicializa una regla

        Parámetros:
        cons (string): consecuente de la regla
        antecedentes (list): antecedentes de la regla
        grado_v (float): valor del grado de verdad

        """
        self.cons = cons
        self.antecedentes = antecedentes
        self.grado_verdad= grado_v
        
    def imprimir(self):
        """Imprime una regla"""
        string_antecedentes = ", ".join(self.antecedentes)
        print(self.cons + " :- " + string_antecedentes + " [" + str(self.grado_verdad) + "]")
        
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

    def imprimir_derivacion(self):
        """Imprime las reglas seguidas en la derivación de una consulta"""
        print("Derivación:")
        for x in self.seguimiento:
            regla = x["cons"]
            print(f"Regla aplicada: {', '.join(regla.antecedentes)} -> {regla.cons}")
            print("Antecedentes aplicados y sus grados:")
            for antecedente, grado in x["antecedentes_aplicados"]:
                print(f"  {antecedente}: {grado}")
            print()

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

        grados_reglas = [] # almacena los grados de cada regla válida
        
        # Recorremos las reglas
        for regla in self.reglas:

            # Si el consecuente coincide con la consulta
            if regla.cons == consulta:

                ok = True
                grado_v = regla.grado_verdad # grado de verdad de la regla
                grados_antecedentes = [] # almacena los grados de los antecedentes válidos
                regla_aplicada = {"cons": regla, "antecedentes_aplicados": []} # para mostrar que reglas hemos aplicado
                
                # Recorremos los antecedentes de la regla
                for antecedente in regla.antecedentes:

                    # Si un antecedente no está en los hechos, intentamos derivarlo recursivamente
                    devuelto = self.backward_chain(antecedente)

                    # Si no se cumple, lo indicamos con la variable ok
                    if devuelto == -1:
                        ok = False
                    # Si el antecedente es un hecho, almacenamos su grado
                    else:
                        grados_antecedentes.append(devuelto)
                        regla_aplicada["antecedentes_aplicados"].append((antecedente, devuelto))  # Guardamos el antecedente aplicado

                # Si todos los antecedentes se cumplen, la consulta también se cumple
                if ok:
                    grados_reglas.append(self.AND_([grado_v, self.AND_(grados_antecedentes)]))
                    self.seguimiento.append(regla_aplicada)

        if len(grados_reglas) != 0:
            return self.OR_(grados_reglas)
        else:
            return -1
       
@click.command()
@click.argument("base", type=click.Path(exists=True, path_type=Path))

def main(base: Path):
    bc = BaseConocimiento()

    # Leemos el fichero que contiene la base de conocimiento
    with base.open("r", encoding="utf-8") as f:  
        texto = f.read()

    # Leemos el archivo que contiene la base de conocimiento        
    for line in texto.split("\n"):

        if line.startswith("#") or not line:
            continue

        # Separamos el consecuente
        cons, resto = line.split(":-")
        cons = cons.strip() # elimina los espacios en blanco

        # Buscamos si hay un grado de verdad entre corchetes
        if "[" in resto and "]" in resto:
            # Separamos los antecedentes y el grado de verdad
            antecedentes, grado_verdad = resto.split("[")
            grado_verdad = grado_verdad.rstrip("]").strip()
            grado_verdad = float(grado_verdad)
            antecedentes = antecedentes.split(",")
            antecedentes = [a.strip() for a in antecedentes]
            # Añadimos la regla a la base de conocimiento
            regla = Regla(cons, antecedentes, grado_verdad)
            bc.agregar_regla(regla)
        else:
            # Separamos los antecedentes
            antecedentes = resto.split(",")
            antecedentes = [a.strip() for a in antecedentes]
            # Añadimos la regla a la base de conocimiento
            regla = Regla(cons, antecedentes)
            bc.agregar_regla(regla)

    consulta = input()
    
    # Mientras la consulta no sea "exit", continúa la ejecución
    while (consulta != "exit"):
        if (consulta == "print"):
            bc.imprimir()
        elif consulta.startswith("add"):
            consulta = consulta.split()
            bc.agregar_hecho(consulta[1], float(consulta[2].strip("[]")))
        elif consulta.endswith("?"):
            bc.seguimiento = []
            devuelto = bc.backward_chain(consulta.strip("?"))
            if devuelto == -1:
                print("No")
            else:
                print(f"Si, ({devuelto})")
                bc.imprimir_derivacion()
            
        consulta = input()
        
if __name__ == '__main__':
    main()

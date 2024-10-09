from pathlib import Path

archivo = Path("base_laboral.txt")
texto = archivo.read_text()

class Regla:
    def __init__(self, cons, antecedentes, grado_v=1.0):
        self.cons = cons
        self.antecedentes = antecedentes
        self.grado_verdad= grado_v
        
    def imprimir(self):
        string_antecedentes = ", ".join(self.antecedentes)
        print(self.cons + " :- " + string_antecedentes + " [" + str(self.grado_verdad) + "]")
        
class BaseConocimiento:
    def __init__(self):
        self.reglas = [] # compuestas por el consecuente, antecedentes y grado de verdad
        self.hechos = {} # agregamos un nuevo hecho a nuesta base de conocimiento
        
	# Método para agregar una regla
    def agregar_regla(self, regla):
        self.reglas.append(regla)
        
    # Método para agregar un hecho
    def agregar_hecho(self, hecho, grado_v=1.0):
        self.hechos[hecho] = grado_v
    
    # Imprime las reglas y los hechos de la base de conocimiento
    def imprimir(self):
        for regla in self.reglas:
            regla.imprimir()
        for hecho in self.hechos:
            print(hecho + " [" + str(self.hechos[hecho]) + "]")
    
    # Realiza razonamiento hacia atrás
    def backward_chain(self, consulta):
        for regla in self.reglas:
            if regla.cons == consulta:
                ok = True
                for antecedente in regla.antecedentes:
                    print(antecedente)
                    if antecedente not in self.hechos:
                        ok = False
                if ok == True:
                    return "Si"
        return "No"
                        
def main():
    bc = BaseConocimiento()

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
            print(bc.backward_chain(consulta.strip("?")))
            
        consulta = input()
        
if __name__ == '__main__':
    main()

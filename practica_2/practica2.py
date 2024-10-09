from pathlib import Path

archivo = Path("base_laboral.txt")
texto = archivo.read_text()

def print_base_conocimiento():
    for line in texto.split("\n"):
	    if line.startswith("#") or not line:
		    continue
	    cons, resto = line.split(":-")
	    cons = cons.strip()
	    antecedentes = resto.split(",")
	    print(line)

class Regla:
    def __init__(self, cons, antecedentes, grado_v=1.0):
        self.cons = cons
        self.antecedentes = antecedentes
        self.grado_verdad= grado_v
        
    def imprimir(self):
        print(self.cons, self.antecedentes, self.grado_verdad)
        
class BaseConocimiento:
    def __init__(self):
        self.reglas = [] # compuesto por el consecuente, antecedentes y grado de verdad
        self.hechos = {} # agregamos un nuevo hecho a nuesta base de conocimiento
        
	# Método para agregar una regla
    def agregar_regla(self, regla):
        self.reglas.append(regla)
        
    #Método para agregar un hecho
    def agregar_hecho(self, hecho, grado_v=1.0):
        self.hechos[hecho] = grado_v
        
    def imprimir(self):
        for regla in self.reglas:
            regla.imprimir()
        for hecho in self.hechos:
            print(hecho + " " + self.hechos[hecho])
     
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
    for line in texto.split("\n"):
	        if line.startswith("#") or not line:
		        continue
	        cons, resto = line.split(":-")
	        cons = cons.strip()
	        antecedentes = resto.split()
	        #antecedentes = antecedentes.split(",")
            
	        #antecedentes = resto.strip()
	        print(antecedentes)
	        regla = Regla(cons, antecedentes)
	        bc.agregar_regla(regla)

    consulta = input()
    consulta = consulta.split()
    
    while (consulta[0] != "exit"):
        if (consulta[0] == "print"):
            bc.imprimir()
        elif consulta[0] == "add":
            bc.agregar_hecho(consulta[1], consulta[2])
        else:
            print(bc.backward_chain(consulta[0]))
            
        consulta = input()
        consulta = consulta.split()
        
if __name__ == '__main__':
    main()

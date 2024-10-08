from pathlib import Path

archivo = Path("base_laboral.txt")
texto = archivo.read_text()

class Regla:
    def __init__(self, cons, resto,grado_v=1.0):
        self.cons = cons
        self.resto = resto
        self.grado_verdad= grado_v
        
class BaseConocimiento:
    def __init__(self):
        self.reglas = [] #compuesto por el consecuente, antecedentes y grado de verdad
        self.hechos = {}# agregamos un nuevo hecho a nuesta base de conocimiento
        
	# Método para agregar una regla
    def agregar_regla(self, regla):
        self.reglas.append(regla)
    #Método para agregar un hecho
    def agregar_hecho(self, hecho, grado_v=1.0):
        self.hechos[hecho] = grado_v


for line in texto.split("\n"):
	if line.startswith("#") or not line:
		continue
	cons, resto = line.split(":-")
	cons = cons.strip()
	antecedentes = resto.split(",")
	print(line)
     
def backward_chain (self, consulta):
     for regla in self.reglas:
          if regla.cons == consulta:
               
     
#consulta = input()
#print(consulta)

#if (consulta == "print"):
		

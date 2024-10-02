from pathlib import Path

archivo = Path("base_laboral.txt")
texto = archivo.read_text()

class Regla:
    def __init__(self, cons, resto):
        self.cons = cons
        self.resto = resto

for line in texto.split("\n"):
	if line.startswith("#") or not line:
		continue
	cons, resto = line.split(":-")
	cons = cons.strip()
	antecedentes = rest.split(",")
	print(line)

#consulta = input()
#print(consulta)

#if (consulta == "print"):
		

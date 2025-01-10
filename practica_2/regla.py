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
        self.grado_verdad = grado_v

    def imprimir(self):
        """Imprime una regla"""
        string_antecedentes = ", ".join(self.antecedentes)
        print(
            self.cons
            + " :- "
            + string_antecedentes
            + " ["
            + str(self.grado_verdad)
            + "]"
        )

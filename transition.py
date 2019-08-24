import sys

from state import state


# Definimos el simbolo estático epsilon
class Epsilon:
    symbol = ""
# En la clase transición tendremos que definir el estado 
# hacia donde se va, el estadoinicial, un simbolo minimo 
# y un máximo (si es que es un rango).
# Por default, el simbolo máximo será epsilon, si se desea 
# un rango, se especificará el simbolo máximo cuando 
# se construya la transición
class Transition:
    #Constructor: Recibe Estado ir, estado viene, y los simbolos de la transicion
    def __init__(self, state_from, state_to, min_Symbol, max_Symbol = Epsilon.symbol ):
        if(min_Symbol <= max_Symbol):
            self.state_from = state_from
            self.state_to = state_to
            self.min_Symbol = min_Symbol
            self.max_Symbol = max_Symbol
        elif(max_Symbol == Epsilon.symbol):
            self.state_from = state_from
            self.state_to = state_to
            self.min_Symbol = min_Symbol
            self.max_Symbol = min_Symbol
        else:
            print ("El simbolo final debe ser menor al simbolo inicio")
            sys.exit()


    #Enviar estado Inicial
    def set_state_to(self, state):
        self.state_to = state
    #Enviar estado Final
    def set_state_from(self, state):
        self.state_from = state
    #Sobrecarga para "convertir a String"
    def __str__(self):
        Out = ""
        Out += str(self.state_from)+" to "+str(self.state_to)+" with "
        if self.min_Symbol != self.max_Symbol:
            Out += self.min_Symbol+" - "+self.max_Symbol
        else:
            Out += self.min_Symbol
        return Out
    


    # Ejemplo de como instanciar una transición
# edoIni = state()
# edoFin = state(True)
# trans = transition(edoIni,edoFin,'s')
# print(trans.state_to)
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
class transition:
    def __init__(self, state_to, state_from, symbol_min, symbol_max = Epsilon.symbol):
        self.state_to = state_to
        self.state_from = state_from
        self.symbol_min = symbol_min
        self.symbol_max = symbol_max
    


    # Ejemplo de como instanciar una transición
# edoIni = state()
# edoFin = state(True)
# trans = transition(edoIni,edoFin,'s')
# print(trans.state_to)
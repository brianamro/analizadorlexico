#Aquí definimos la clase estado, recibe si es
#estado de aceptación y se le asigna un id. El id
#cada que se crea un estado incrementa el id para  
#que no haya dos estados con un mismo id
class state:
    id_state = 0
    #constructor: recibe si es estado de aceptación
    #el valor por defecto es que no es estado de aceptación
    def __init__(self, value=False):
        self.accept = value
        self.id_state = state.id_state
        state.id_state = state.id_state+1
    #Sobrecargamos el método de imprimir para poder
    #acceder al valor del id de algún estado más fácilmente
    def __str__(self):
        stateAux = "id.state: "+str(self.id_state)
        return stateAux

    #Ejemplo de como instanciar un estado
# edo1 = state()
# edo2 = state(True)
# edo3 = state(False)

# print(edo1.accept)
# print(edo2.accept)
# print(edo3.accept)

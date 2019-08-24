import sys
#Aquí definimos la clase estado, recibe si es
#estado de aceptación y se le asigna un id. El id
#cada que se crea un estado incrementa el id para  
#que no haya dos estados con un mismo id
class State():
    id_state = 0
    #constructor: recibe si es estado de aceptación
    #el valor por defecto es que no es estado de aceptación
    def __init__(self, value=False):
        self.accept = value
        self.id_state = State.id_state
        State.id_state = State.id_state+1
    #Sobrecargamos el método de imprimir para poder iprimir el ID del estado
    def __str__(self):
        return str(self.id_state)
    #Sobrecarga del operador "==" para comprar si dos estados son iguales
    def __eq__(self, other):
        return self.id_state == other.id_state
    #Retornar si es un estado de aceptacion
    def isAccept(self):
        return self.accept
    #El atributo de aceptacion pasa a ser Falso
    def deleteAccept(self):
        self.accept = False
    #Union de dos conjuntos de estados
    def unionSt(self,states2):  #states1  y states2 deben ser arreglos
        if isinstance(states2, list):
            newStates = [self]
            for state in states2:
                newStates.append(state)
            return newStates
        else:
            print("Error en los argumentos")
            sys.exit()

#Ejemplo de como instanciar un estado
# edo1 = state()
# edo2 = state(True)
# edo3 = state(False)

# print(edo1.accept)
# print(edo2.accept)
# print(edo3.accept)

import sys

from transition import Transition
from transition import Epsilon
from state import State

class AFN():
    id_AFN = 0
    def __init__(self, ini_state, end_state, transitions, states):
        if isinstance(end_state, list) and isinstance(transitions, list) and isinstance(states, list):
            self.ini_state = ini_state
            self.end_state = end_state
            self.transitions = transitions
            self.states = states
            self.id_AFN = AFN.id_AFN
            AFN.id_AFN = AFN.id_AFN + 1
        else:
            print("El estado final, transiciones y estados deben ser arreglos")
            sys.exit()
    #Sobreescritura para imprimir el AFN con la funcion print
    def __str__(self):
        Out  = "AFN: "+str(self.id_AFN)+"\n"
        #Impresion de estados
        Out += "States: ["
        for state in self.states:
            Out += str(state)+","
        Out += "]\n"
        Out += "Inicial: "+str(self.ini_state)+"\n"
        #Imprimir Transiciones
        for trans in self.transitions:
            Out += str(trans)+"\n"
        #Imprimir estados de Aceptacion
        Out += "Acceptacion: ["
        for state in self.end_state:
            Out += str(state)+","
        Out += "]\n"
        return Out
    #Agregar un array de estados al AFN
    def addStates(self, states):
        if isinstance(states, list):
            for state in states:
                self.states.append(state)
        else:
            print("Solo se recibe array de estados")
            sys.exit()
    #Poner en falso los estados de aceptacion de un autoamta
    def deleteStatesAccept(self):
        newStates = []
        for state in self.end_state:
            state.accept = False
            #  = state.deleteAccept()
            newStates.append(state)
        self.end_state = newStates
    #Creacion de un automata basico con un solo caracter
    def createBasicAutomata(car):
        iniSt = State()
        endSt = State(True)
        trans = Transition(iniSt, endSt, car)
        basicAFN = AFN(iniSt, [endSt], [trans], [iniSt, endSt])
        return basicAFN
    
    def union(self, AFN2):
        iniSt = State()
        endSt = State(True)
        #Borramos el estado de aceptacion de los AFN
        self.deleteStatesAccept()   
        AFN2.deleteStatesAccept()   
        #Creamos las nuevas Trancisiones Iniciales
        t1_i = Transition(iniSt, self.ini_state, Epsilon.symbol)
        t2_i = Transition(iniSt, AFN2.ini_state, Epsilon.symbol)
        allTrans = [t1_i, t2_i]
        #Creamos Transiciones de estados finales
        for state in self.end_state:    #Primer Automata
            tx = Transition(state, endSt, Epsilon.symbol)
            allTrans.append(tx)     #Insertar Nuevas Transiciones
        for state in AFN2.end_state:    #Segundo Automata
            tx = Transition(state, endSt, Epsilon.symbol)
            allTrans.append(tx)     
        #Insertamos las transiciones de cada uno de los Automatas
        for trans in self.transitions:
            allTrans.append(trans)
        for trans in AFN2.transitions:
            allTrans.append(trans)
        #Agregamos los nuevos estados
        newStates = [iniSt, endSt]
        for state in self.states:
            newStates.append(state)
        for state in AFN2.states:
            newStates.append(state)
        #Creacion del nuevo AFN con la quitupla
        newAFN = AFN(iniSt, [endSt], allTrans, newStates)
        return newAFN
    
    def concatenate(self, AFN2):
        #Borramos estados de aceptacion
        self.deleteStatesAccept()
        #Nuevas transiciones
        allTrans = []
        #Creamos Transiciones del estado de aceptacion del AFN1 al inicial del AFN2
        #Transiciones intermedias
        for state in self.end_state:    #Primer Automata
            t_inter = Transition(state, AFN2.ini_state, Epsilon.symbol)
            allTrans.append(t_inter)     #Insertar Nuevas Transiciones
        #Transiciones existentes
        for transition in self.transitions:  #Primer Automata
            allTrans.append(transition)    
        for transition in AFN2.transitions:  #Segundo Automata
            allTrans.append(transition)    
        #Juntar todos los estados de cada uno de los automatas
        newStates = []
        #Primer AFN
        for state in self.states:
            newStates.append(state)
        #Sefundo auotamta
        for state in AFN2.states:
            newStates.append(state)
        #Creacion del automata
        newAFN = AFN(self.ini_state, AFN2.end_state, allTrans, newStates)
        return newAFN
    
    #Opcional "?"
    def optional(self):
        newTransitions = self.transitions   #Transiciones ya exisitentes
        #Nuevas Transiciones del estado inicial al conjunto de estados finales
        for state in self.end_state:
            t_optional = Transition(self.ini_state, state, Epsilon.symbol)
            newTransitions.append(t_optional)
        #Regresamos Nuevo Automata
        return AFN(self.ini_state, self.end_state, newTransitions, self.states)
    
    #Cerradura Epsilon, recibe un estado
    def C_Epsilon(self, state):
        if isinstance(state, State):
            #Recorremos las transiciones del Automata
            outStates = []
            for trans in self.transitions:
                if(trans.state_from == state):   #Estado inicial de la transicion igual al estado a igualar
                    if(trans.hasEpsilon):        #La transicion tiene a epsilon
                        outStates.append(trans.state_to)   #Agregamos el estado al que llega con dicha transicion
            return state.unionSt(outStates)
        else:
            print("Se esperaba un estado")
            sys.exit()
    # La funcion mover estado recibe un conjunto de estados y un caracter
    # y regresa un conjunto de estados. Esta funcion es util en el analisis
    # de cadenas.
    def move_state(self, states, caracter):
        conjunto = []
        # Recorremos todos los estados y les sacamos la cerradura
        # epsilon para checar si tiene alguna transicón con el caracter 
        # que recibe la función
        for state in states:
            #print("sacando cerradura epsilon de: ",state)
            cerradura = self.C_Epsilon(state)
            # Recorremos cada estado de la cerradura y checamos
            # si existe alguna transición con ese estado y con ese simbolo
            # y lo agregamos al conjunto
            for estado in cerradura:
                #print(estado.id_state)
                for trans in self.transitions:
                    if caracter in trans.range() and trans.state_from == estado:
                        #print(trans.state_to)
                        conjunto.append(trans.state_to.id_state)
                        return conjunto


#--------------  M  A  I  N  --------------
AFN1 = AFN.createBasicAutomata('a')
print ("Basico 1:\n")
print(AFN1)
AFN2 = AFN.createBasicAutomata('b')
print ("Basico 2:\n")
print(AFN2)
AFNU = AFN1.union(AFN2)
print("Union (1,2)")
print(AFNU)
AFNCon = AFN1.concatenate(AFN2)
print("Concatenar (1,2)")
print(AFNCon)
AFN_OP = AFNU.optional()
print("Opcional Union(1,2)")
print(AFN_OP)
# CE = AFN_OP.C_Epsilon(AFN_OP.ini_state)
# print("Cerradura Epislon IniState de Automata Opcional")
# for state in CE:
#     print(state)
conjunto = AFN_OP.C_Epsilon(AFN_OP.ini_state)
print(AFN_OP.move_state(conjunto, 'a'))



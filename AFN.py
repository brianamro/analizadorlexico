import sys

from transition import Transition
from transition import Epsilon
from state import State

class AFN():
    id_AFN = 0
    def __init__(self, ini_state, end_state, transitions, states):
        #El modelo de THomposon inidica que solo puede haber un unico estado inicial, 
        #Y un unico estado de Aceptacion
        if isinstance(transitions, list) and isinstance(states, list):
            self.ini_state = ini_state
            self.end_state = end_state
            self.transitions = transitions
            self.states = states
            self.id_AFN = AFN.id_AFN
            AFN.id_AFN = AFN.id_AFN + 1
        else:
            print("Las transiciones y estados deben ser arreglos")
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
        Out += "Acceptacion: " +str(self.end_state)+ "\n"
        return Out
    #Agregar un array de estados al AFN
    def addStates(self, states):
        if isinstance(states, list):
            for state in states:
                self.states.append(state)
        else:
            print("Solo se recibe array de estados")
            sys.exit()
    #Poner en falso el estado de aceptacion de un autoamta
    def deleteAcceptState(self):
        self.end_state.deleteAccept()
    #Creacion de un automata basico con un solo caracter
    def createBasicAutomata(car):
        iniSt = State()
        endSt = State(True)
        trans = Transition(iniSt, endSt, car)
        basicAFN = AFN(iniSt, endSt, [trans], [iniSt, endSt])
        return basicAFN

    def createRangeAutomata(carIni, carFin):
        iniSt = State()
        endSt = State(True)
        trans = Transition(iniSt, endSt, carIni, carFin)
        rangeAFN = AFN(iniSt, endSt, [trans], [iniSt, endSt])
        return rangeAFN
    #Union del objetos de auntomota con otro autoamta
    #Sobreescribe el automata SELF
    def union(self, AFN2):
        if isinstance(AFN2, AFN):
            #Borramos el estado de aceptacion de los AFN
            self.deleteAcceptState()   
            AFN2.deleteAcceptState()   
            #Creamos nuevos Estados
            newIniSt = State()
            newEndSt = State(True)
            #Creamos las nuevas Trancisiones Iniciales
            t1_i = Transition(newIniSt, self.ini_state, Epsilon.symbol)
            t2_i = Transition(newIniSt, AFN2.ini_state, Epsilon.symbol)
            allTrans = [t1_i, t2_i]
            #Creamos Transiciones de estados finales
            t1_e = Transition(self.end_state, newEndSt, Epsilon.symbol)
            t2_e = Transition(AFN2.end_state, newEndSt, Epsilon.symbol)
            allTrans = allTrans + [t1_e, t2_e]   
            #Insertamos las transiciones ya exisitentes de cada uno de los Automatas
            for trans in self.transitions:
                allTrans.append(trans)
            for trans in AFN2.transitions:
                allTrans.append(trans)
            #Agregamos los nuevos estados
            newStates = [newIniSt, newEndSt]  
            #Estados ya exisitentes
            for state in self.states:
                newStates.append(state)
            for state in AFN2.states:
                newStates.append(state)
            #Modificamos el objeto
            self.ini_state = newIniSt
            self.end_state = newEndSt
            self.transitions = allTrans
            self.states = newStates
        else:
            print("Se espera un Objeto Clase AFN como argumento")
            sys.exit()

    #Concatenar dos Automatas        
    #Recibe un obejto AFN, sobreescribe el automata SELF
    def concatenate(self, AFN2):
        if isinstance(AFN2, AFN):
            #Borramos estados de aceptacion
            self.deleteAcceptState()
            #Nuevas transiciones
            allTrans = []
            #Creamos Transiciones del estado de aceptacion del AFN1 al inicial del AFN2
            #Transicion Intermedia (Estado Final del "This" a estado Inicial AFN2)
            t_inter = Transition(self.end_state, AFN2.ini_state, Epsilon.symbol)
            allTrans.append(t_inter)     #Insertar Transicion Intermedia
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
            #Segundo auotamta
            for state in AFN2.states:
                newStates.append(state)
            #Modifacion del autoamata
            self.end_state = AFN2.end_state
            self.transitions = allTrans
            self.states = newStates
            
        else:
            print("Se esperaba un obejeto clase AFN\n")
            sys.exit()
    
    #Opcional "?"   
    #Modifica el mismo automata
    def optional(self):
        #Eliminar Aceptacion del mismo automata
        self.deleteAcceptState()
        #Traer estados existentes
        newStates = self.states
        #Crear Nuevos estados
        newIniState = State()   
        newStates.append(newIniState)
        newEndState = State(True)
        newStates.append(newEndState)
        #Transiciones ya exisitentes
        newTransitions = self.transitions   
        #Nuevas Transiciones 
        t_ini = Transition(newIniState, self.ini_state, Epsilon.symbol)
        newTransitions.append(t_ini)
        t_end = Transition(self.end_state, newEndState, Epsilon.symbol)
        newTransitions.append(t_end)
        t_optional = Transition(newIniState, newEndState, Epsilon.symbol)
        newTransitions.append(t_optional)
        #Modificacion del Objeto
        self.ini_state = newIniState
        self.end_state = newEndState
        self.transitions = newTransitions
        self.states = newStates

    #Cerradura +
    #Modifica el automata SELF
    def kleene_plus(self):
        #Eliminar estado de aceptacion
        self.deleteAcceptState()
        #Traemos las Transiciones ya existentes
        newTransitions = self.transitions
        #Transicion del final acutal, al inicial actual
        t_return = Transition(self.end_state, self.ini_state, Epsilon.symbol)
        newTransitions.append(t_return)
        #Nuevos estados
        newStates = self.states
        ini_State = State()
        newStates.append(ini_State)
        end_State = State(True)
        newStates.append(end_State)
        #Nuevas transiciones
        t_ini = Transition(ini_State, self.ini_state, Epsilon.symbol)
        newTransitions.append(t_ini)
        t_end = Transition(self.end_state, end_State, Epsilon.symbol)
        newTransitions.append(t_end)
        #Modificacion del Objeto
        self.ini_state = ini_State
        self.end_state = end_State
        self.transitions = newTransitions
        self.states = newStates
    
    #Cerradura *
    #Modifica el automata SELF
    def kleene_star(self):
        #Eliminar estado de aceptacion
        self.deleteAcceptState()
        #Traemos las Transiciones ya existentes
        newTransitions = self.transitions
        #Transicion del final acutal, al inicial actual
        t_return = Transition(self.end_state, self.ini_state, Epsilon.symbol)
        newTransitions.append(t_return)
        #Traer Estados acutales
        newStates = self.states
        #Nuevos estados
        ini_State = State()
        newStates.append(ini_State)
        end_State = State(True)
        newStates.append(end_State)
        #Nuevas transiciones
        t_ini = Transition(ini_State, self.ini_state, Epsilon.symbol)
        newTransitions.append(t_ini)
        t_end = Transition(self.end_state, end_State, Epsilon.symbol)
        newTransitions.append(t_end)
        t_optional = Transition(ini_State, end_State, Epsilon.symbol)
        newTransitions.append(t_optional)
        #Modificacion del Objeto
        self.ini_state = ini_State
        self.end_state = end_State
        self.transitions = newTransitions
        self.states = newStates
    
    #Cerradura Epsilon, recibe un estado
    def C_Epsilon_state(self, state):
        if isinstance(state, State):
            #Recorremos las transiciones del Automata
            outStates = []
            for trans in self.transitions:
                if(trans.state_from == state):   #Estado inicial de la transicion igual al estado a igualar
                    if(trans.hasEpsilon):        #La transicion tiene a epsilon
                        outStates.append(trans.state_to)   #Agregamos el estado al que llega con dicha transicion
            #Regresa un areglo de estados
            return state.unionSt(outStates)
        else:
            print("Se esperaba un estado")
            sys.exit()

    # Este metodo obtiene el alfabeto de un AFN
    def get_alpahbet(self):
        # En el arreglo llamado aux guardaremos todos los caracteres
        # de todas las transiciones
        aux = []
        for trans in self.transitions:
            # for car in trans.range():
            aux.append(trans.min_Symbol)
        # Eliminamos los caracteres repetidos
        alfabeto = []
        for elem in aux:
            if elem not in alfabeto:
                alfabeto.append(elem)
        alfabeto.remove(Epsilon.symbol)
        return alfabeto
            

    # Esta función calcula la cerradura epsilon de un conjunto de estados
    # a partir de la funcion c_epsilon_sate
    def C_Epsilon(self, states):
        arrayStates = []
        for state in states:
            arrayStates = arrayStates + self.C_Epsilon_state(state)
        #Quitar elementos repetidos del arreglo
        outArrayStates = []
        for i in arrayStates:
            if i not in outArrayStates:
                outArrayStates.append(i)
        return outArrayStates    
    # Esta función calcula los estados a donde se puede mover
    # a partir de un estado y un caracter

    def move_state(self, state, caracter):
        arrayStates = []
        #Recorrer todas las transiciones
        for trans in self.transitions:
            # if caracter in trans.range() and state==trans.state_from:
            if caracter == trans.min_Symbol and state == trans.state_from:
                arrayStates.append(trans.state_to)
        #Quitar elementos repetidos del arreglo
        outArrayStates = []
        for i in arrayStates:
            if i not in outArrayStates:
                outArrayStates.append(i)
        return outArrayStates

    # Esta funcion calcula el conjunto de estados
    # a donde se puede mover a partir de un caracter
    # regresa un conjunto de estados y recibe un 
    # conjunto de estados y un caracter
    def move_arrayStates(self, states, caracter):
        arrayStates = []
        for state in states:
            arrayStates = arrayStates + self.move_state(state,caracter)
        #Quitar elementos repetidos del arreglo
        outArrayStates = []
        for i in arrayStates:
            if i not in outArrayStates:
                outArrayStates.append(i)
        return outArrayStates
    # Go to regresa la cerradura epsilon de los estados
    # obtenidos a partir de la función move_arrayStates (mover a)
    
    def go_to(self, states, caracter=False):
        if caracter or caracter != "":
            arrayMove = self.move_arrayStates(states,caracter)
            return self.C_Epsilon(arrayMove)

# La función convert_to_afd recibe un automata con transiciones 
    # epsilon y devuelve un nuevo automata pero de la forma
    # determinista
    def convert_to_afd(self): 
        c_e_ini = []
        matrixFinal = []
        contStates = 1
        
        #Calcular cerradura epislon con el estado inicial
        c_e_ini = self.C_Epsilon_state(self.ini_state)
        alfabeto = self.get_alpahbet()      #Regresa arreglo de caracteres
        nuevos_PseaudoEstados = []

        # Hacer estados iniciales con la cerradura epislon del estado inicial, y los caracteres del alfabeto
        print("Alfabeto: ", alfabeto)
        print("Cerradura Inicial")
        for elem in alfabeto:
            arrayEstadosTemp = self.go_to(c_e_ini, elem)
            stateTo = 0
            if len(arrayEstadosTemp) > 0:   #Verificamos que devuelva un conjunto NO vacio
                nuevos_PseaudoEstados.append(arrayEstadosTemp)
                stateTo = len(nuevos_PseaudoEstados) - 1        #Indice de los nuevos PseudoEstados
            else:
                stateTo = -1
            #Insertar en la matriz
            matrixFinal.append([contStates, elem, stateTo])     #Transcion => IniState, Caracter, FinEstado
        
        #Pila                  
        indexUlitmoItem = len(nuevos_PseaudoEstados)-1
        print(matrixFinal)
        print("Despues de Cerradura Inicial")
        while contStates < indexUlitmoItem:
            #Recorrer alfabeto
            for elem in alfabeto:
                arrayAuxEstados = self.go_to(nuevos_PseaudoEstados[contStates], elem)
                stateTo = 0
                if len(arrayEstadosTemp) > 0:   #Conjunto de Estados NO Vacios
                    if State.arrayIsMatrix(arrayAuxEstados, nuevos_PseaudoEstados):       #  Verficiamos si no se ha insertado con anteriordad
                        nuevos_PseaudoEstados.append(arrayEstadosTemp)
                        stateTo = len(nuevos_PseaudoEstados) - 1        #Indice de los nuevos PseudoEstados
                else:
                    stateTo = -1
                #Insertamos en la matriz Final
                matrixFinal.append([contStates, elem, stateTo])

            contStates = contStates + 1
            indexUlitmoItem = len(nuevos_PseaudoEstados)-1

        #Agregar Estado Inicial
        nuevos_PseaudoEstados.append(c_e_ini)
        print(matrixFinal)
        print("FIN")
        return matrixFinal
    
def main():
    #--------------  M  A  I  N  --------------
    #     #Concatenar
    # print("Concatenar Basico 3 y Basico 4")
    # AFN3.concatenate(AFN4)
    # print(AFN3)
    # #Opcional
    # AFN5 = AFN.createBasicAutomata('e')
    # print("Basico 5:")
    # print(AFN5)
    # AFN5.optional()
    # print("Opcional")
    # print(AFN5)
    # # #Cerradura+
    # AFN6 = AFN.createBasicAutomata('f')
    # print("Basico 6:")
    # print(AFN6)
    # AFN6.kleene_plus()
    # print("Cerradura+")
    # print(AFN6)
    # #Cerradura*
    # AFN7 = AFN.createBasicAutomata('a')
    # print("Basico 6:")
    # print(AFN7)
    # AFN7.kleene_star()
    # print("Cerradura*")
    # print(AFN7)
    # c_e = AFN1.convert_to_afd()
    # for state in c_e:
    #     print(state)
    # afd = AFN1.convert_to_afd()
    # for state in afd:
    #     for st in state:
    #         print(st, end='')
    #         print(" ", end='')
        # print()
    # conjunto = AFN1.go_to([AFN1.ini_state], 'b')

    # for i in conjunto:
    #     print(i)

    #Crear automata (+|-)?&[0-9]+&.&[0-9]+
    AFN1_main = AFN.createBasicAutomata('+')
    AFN1_men = AFN.createBasicAutomata('-')
    AFN1_nrA = AFN.createBasicAutomata('d')
    AFN1_poi = AFN.createBasicAutomata('.')
    AFN1_nrB = AFN.createBasicAutomata('d')

    AFN1_main.union(AFN1_men)   #(+|-)    
    AFN1_main.optional()        #(+|-)?
    AFN1_nrA.kleene_plus()      #[0-9]+
    AFN1_nrB.kleene_plus()      #[0-9]+
    AFN1_main.concatenate(AFN1_nrA)     #(+|-)?&[0-9]+
    AFN1_main.concatenate(AFN1_poi)     #(+|-)?&[0-9]+&.
    AFN1_main.concatenate(AFN1_nrB)     #(+|-)?&[0-9]+&.&[0-9]+

    print("(+|-)?&[0-9]+&.&[0-9]+\n")
    print(AFN1_main.convert_to_afd())

    #Crear Autonata (+!-)?&[0-9]?
    AFN2_main = AFN.createBasicAutomata('+')
    AFN2_men = AFN.createBasicAutomata('-')
    AFN2_nrA = AFN.createRangeAutomata('0','9')

    AFN2_main.union(AFN2_men)   #(+|-)    
    AFN2_main.optional()        #(+|-)?
    AFN2_nrA.kleene_plus()      #[0-9]+
    AFN2_main.concatenate(AFN2_nrA)     #(+|-)?&[0-9]+

    print("(+|-)?&[0-9]+&.&[0-9]+\n")
    # print(AFN2_main)

    #Crear Automata +&+
    AFN4_main = AFN.createBasicAutomata('+')
    AFN4_plus = AFN.createBasicAutomata('+')
    AFN4_main.concatenate(AFN4_plus)

    #Crear Automata +
    AFN5_main = AFN.createBasicAutomata('+')
    





if __name__ == '__main__':
    main()  

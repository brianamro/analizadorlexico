import sys

from transition import Transition
from transition import Epsilon
from state import State
from alphabet import Alphabet

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
            #Creacion del nuevo Objeto
            newAFN = AFN(newIniSt, newEndSt, allTrans, newStates)
            return newAFN
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
            #Creacion del nuevo Objeto
            newAFN = AFN(self.ini_state, AFN2.end_state, allTrans, newStates)
            return newAFN
            
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
        #Creacion del nuevo Objeto
        newAFN = AFN(newIniState, newEndState, newTransitions, newStates)
        return newAFN

    #Cerradura +
    #Modifica el automata SELF
    def kleene_plus(self):
        #Eliminar estado de aceptacion
        self.deleteAcceptState()
        #Traemos las Transiciones ya existentes
        newTransitions = self.transitions
        #Transicion del final actual, al inicial actual
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
        #Creacion del nuevo Objeto
        newAFN = AFN(ini_State, end_State, newTransitions, newStates)
        return newAFN

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
        #Creacion del nuevo Objeto
        newAFN = AFN(ini_State, end_State, newTransitions, newStates)
        return newAFN
    
    #Cerradura Epsilon, recibe un estado
    def C_Epsilon_state(self, state):
        if isinstance(state, State):
            #Recorremos las transiciones del Automata
            outStates = []
            #Calcular las transciones epsilon del estado argumento State
            for trans in self.transitions:
                if(trans.state_from == state):   #Estado inicial de la transicion igual al estado a igualar
                    if(trans.hasEpsilon()):        #La transicion tiene a epsilon
                        outStates.append(trans.state_to)   #Agregamos el estado al que llega con dicha transicion
            apunt = 0
            indexLastItem = len(outStates)
            #Calcular las transciones epsilon de los otros estados
            while apunt < indexLastItem:
                for trans in self.transitions:
                    if(trans.state_from == outStates[apunt]):
                        if(trans.hasEpsilon()):
                            outStates.append(trans.state_to)
                indexLastItem = len(outStates)
                apunt = apunt + 1
            
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
        #Eliminamos Epsilon si existe
        if Epsilon.symbol in alfabeto:
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
        # print("Move St car: ", caracter, " State From: ", state) 
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
    # Regresa un conjunto de estados
    # Recibe un conjunto de estados y un caracter
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
        # if caracter or caracter != "":
        arrayMove = self.move_arrayStates(states,caracter)
        return self.C_Epsilon(arrayMove)

    #Funcion que un un arreglo de AFNS en un uno solo,
    # ademas de asignar un token unico a cada uno de los estados de aceptacion
    # de los automatas dados como argumentos
    #Recibe arreglo de AFN, retorna AFN
    def union_nAFN(arrayAFNS):
        iniState = State()    
        token = 10
        newTransitions = []
        newStates = []
        endStates = []
        token = 10       #Inicializar
        for automata in arrayAFNS:
            automata.end_state.token = token
            token = token + 10
            
        automata_union = arrayAFNS[0]
        for i in range(1,len(arrayAFNS)):
            automata_union = automata_union.union(arrayAFNS[i])

        #return AFN(iniState,endStates,newTransitions,newStates)
        return automata_union
            

    # La función convert_to_afd recibe un automata con transiciones 
    # epsilon y devuelve un nuevo automata pero de la forma
    # determinista
    def convert_to_afd(self): 
        #Conseguir alfabeto del afn
        alphabet = self.get_alpahbet()
        #Calcular la cerradura epislon del estado inicial
        S0 = self.C_Epsilon_state(self.ini_state)
        
        stackAux = []           #Conjuntos de Estados
        stackAux.append(S0)     #Instartar S0

        tableFinal = []         #Tabla fina de elementos
        cont = 0
        #Analizano S0 para cada elemento del alfabeto
        for elem in alphabet:
            arrayStatesAux = self.go_to(S0, elem)
            if len(arrayStatesAux) > 0: #Conjunto NO vacio
                stackAux.append(arrayStatesAux)
                stateTo = len(stackAux) - 1 #COnjunto que se acaba de crear 
            else:
                stateTo = -1    #Conjunto Vacio  
                # Agregamos token
            bandera = -1
            tableFinal.append([cont, elem, stateTo,bandera])    #Transicon -> State Ini, Caracter, StateFinal
        #Fin de Analisis S0
        
        #Analizar los nuevos conjuntos de estados
        apunt = 1
        indexLastItem = len(stackAux)

       # print("I: ", indexLastItem)
        
        #Calcular las transciones epsilon de los otros estados
        while apunt < indexLastItem:
            #Analizar nuevos conjuntos SX
            for elem in alphabet:
                arrayStatesAux = self.go_to(stackAux[apunt], elem)
                if len(arrayStatesAux) > 0: #Conjunto NO vacio
                    
                    if arrayStatesAux not in stackAux:
                        stackAux.append(arrayStatesAux)
                        stateTo = len(stackAux) - 1 #COnjunto que se acaba de crear 
                    elif arrayStatesAux in stackAux:
                        stateTo =  stackAux.index(arrayStatesAux)
                else:
                    stateTo = -1    #Conjunto Vacio   
                # Agregamos un elemento al arreglo para
                # identificar a los estados de aceptación
                bandera = -1
                tableFinal.append([apunt,elem, stateTo, bandera])    
                
            indexLastItem = len(stackAux)
            apunt = apunt + 1    

        #Buscar el token del subconjunto de estados
        for elem in stackAux:
            elem.sort()
            if self.end_state in elem:  #Estado de aceptacion del autoamta esta en el conjunto de estados
                for state in elem:
                    if state.token != -1:
                        #Buscar el indice del element
                        #Ya que hace el papel de State To em la tabla final
                        index = stackAux.index(elem)
                        # print(index, "", state.token, end=",")
                        for tupla in tableFinal:
                            if tupla[0] == index:
                                tupla[3] = state.token
     
        return tableFinal

    def funcion_transicion(self,matrix, state_from, symbol):
        for column in matrix:
            if column[0] == state_from and column[1] == symbol:
                return column[2]    #EstadoIr, token

    #Funcion que imprime la tabla de transicion Fiinal
    def tableAFD(self):
        matrixFinal = self.convert_to_afd()     #Conseguimos la matriz de transciones
        allSymbols = []
        statesFrom = []
        
        for column in matrixFinal:
            if column[1] not in allSymbols:     #Traer Simbolos
                allSymbols.append(column[1])  
            if column[0] not in statesFrom:
                statesFrom.append(column[0])    #Traes Estados Inciales
        #Recorrer Arreglo de simbolos
        print("\n  Estado   ",end="")
        for elem in allSymbols:
            out = ""
            if elem == Alphabet.range_num:
                out = "[0-9]"  
            elif elem == Alphabet.range_min:
                out = "[A-Z]"  
            elif elem == Alphabet.range_may:
                out = "[a-z]"
            else:
                out = elem
            print("| ",out," |", end="")
        print("| token |", end="")
        print("\n")
        
        cont = 0
        for state in statesFrom:
            print("  ",state,"  | ", end="")
            for symbol in allSymbols:
                print("  ",self.funcion_transicion(matrixFinal,state,symbol), "  | ",end="")
            for tupla in matrixFinal:
                if tupla[0] == state:
                    print(" || ",tupla[3])
                    break
            cont = cont + 1


def main():
    #--------------  M  A  I  N  --------------

    #Crear automata (+|-)?&[0-9]+&.&[0-9]+
    AFN1_main = AFN.createBasicAutomata('+')
    AFN1_men = AFN.createBasicAutomata('-')
    AFN1_nrA = AFN.createBasicAutomata(Alphabet.range_num) #0-9
    AFN1_poi = AFN.createBasicAutomata('.')
    AFN1_nrB = AFN.createBasicAutomata(Alphabet.range_num) #0-9

    AFN1_main = AFN1_main.union(AFN1_men)   #(+|-)    
    AFN1_main = AFN1_main.optional()        #(+|-)?
    AFN1_nrA = AFN1_nrA.kleene_plus()       #[0-9]+
    AFN1_nrB = AFN1_nrB.kleene_plus()       #[0-9]+
    AFN1_main = AFN1_main.concatenate(AFN1_nrA)     #(+|-)?&[0-9]+
    AFN1_main = AFN1_main.concatenate(AFN1_poi)     #(+|-)?&[0-9]+&.
    AFN1_main = AFN1_main.concatenate(AFN1_nrB)     #(+|-)?&[0-9]+&.&[0-9]+
    print("\nAFN1 (+|-)?&[0-9]+&.&[0-9]+\n")
    # matriz = AFN1_main.tableAFD()
    #func
    
    #Crear Autonata (+!-)?&[0-9]?
    AFN2_main = AFN.createBasicAutomata('+')
    AFN2_men = AFN.createBasicAutomata('-')
    AFN2_nrA = AFN.createBasicAutomata(Alphabet.range_num)

    AFN2_main = AFN2_main.union(AFN2_men)   #(+|-)    
    AFN2_main = AFN2_main.optional()        #(+|-)?
    AFN2_nrA = AFN2_nrA.kleene_plus()      #[0-9]+
    AFN2_main = AFN2_main.concatenate(AFN2_nrA)     #(+|-)?&[0-9]+
    print("\nAFN2: (+|-)?&[0-9]+&.&[0-9]+\n")
    # print(AFN2_main.convert_to_afd())

    #Crear Automata ([a-z]|[A-Z])&([a-z]|[A-Z]|[0-9])*
    AFN3_main = AFN.createBasicAutomata(Alphabet.range_min) #[a-z]
    AFN3_may1 = AFN.createBasicAutomata(Alphabet.range_may)  #[A-Z]
    AFN3_min1 = AFN.createBasicAutomata(Alphabet.range_min) #[a-z]
    AFN3_may2 = AFN.createBasicAutomata(Alphabet.range_may)  #[A-Z]
    AFN3_num = AFN.createBasicAutomata(Alphabet.range_num)  #[A-Z]

    AFN3_num = AFN3_num.union(AFN3_may2)            #AFN3_num = [A-Z]|[0-9]
    AFN3_num = AFN3_num.union(AFN3_min1)            #AFN3_num = [A-Z]|[0-9]|[a-z]
    AFN3_num = AFN3_num.kleene_star()               #AFN3_num = ([A-Z]|[0-9]|[a-z])*

    AFN3_main = AFN3_main.union(AFN3_may1)          #AFN3_main = ([a-z]|[A-Z])
    AFN3_main = AFN3_main.concatenate(AFN3_num)     #AFN3_main = ([a-z]|[A-Z]) & ([A-Z]|[0-9]|[a-z])*

    print("\nAFN3: (a-z)(A-Z)&([a-z]|[A-Z]|[0-9])*n")
    # print(AFN3_main.convert_to_afd())

    #Crear Automata +&+
    AFN4_main = AFN.createBasicAutomata('+')
    AFN4_plus = AFN.createBasicAutomata('+')
    AFN4_main = AFN4_main.concatenate(AFN4_plus)
    print("\nAFN4: +&+\n")
    # print(AFN4_main.convert_to_afd())

    #Crear Automata +
    AFN5_main = AFN.createBasicAutomata('+')
    print("\nAFN5: +\n")
    # print(AFN5_main.convert_to_afd())

    #AUTOMATA GRANDE UNION DE LOS 5 ANTERIORES
    mainAFN = AFN1_main.union(AFN2_main)    #mainAFN = AFN1 | AFN2
    mainAFN = mainAFN.union(AFN3_main)      #mainAFN = (AFN1 | AFN2) | AFN3
    mainAFN = mainAFN.union(AFN4_main)      #mainAFN = ((AFN1 | AFN2) | AFN3) | AFN4
    mainAFN = mainAFN.union(AFN5_main)      #mainAFN = (((AFN1 | AFN2) | AFN3) | AFN4) | AFN5

    print("\nMAIN AUTOMATA\n")
    mainAFN2 = AFN.union_nAFN([AFN1_main,AFN2_main,AFN3_main,AFN4_main,AFN5_main])
    mainAFN2.tableAFD()
    
if __name__ == '__main__':
    main()  

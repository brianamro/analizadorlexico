import sys

from alphabet import Alphabet
from regEx import RegularExp
from AFN import AFN
from state import State
from transition import Transition

class AFD():
    id_AFD = 0
    #Constructor de la clase AFD
    #ini_state (Entero)
    #end_state (Arreglo de enteros)
    #Alphabet (Arrelglo de: caracteres, simbolos especiales, palabras etc)
    #Token = ?
    def __init__(self, ini_state, end_states, allStates, transitions, alphabet, token = None):
        self.id_AFD = AFD.id_AFD
        AFD.id_AFD = AFD.id_AFD +1
        self.ini_state = ini_state
        self.end_states = end_states
        self.all_states = allStates
        self.transitions = transitions
        self.alphabet = alphabet
        self.token = token
        # Atributos para anailizar cadenas
        self.apCarActual = 0
        self.thisString = ""

    #Funcion de Transcion dado el estado del cual se parte y el simbolo 
    def funcion_transicion(self,matrix, state_from, symbol):
        for column in matrix:
            if column[0] == state_from and column[1] == symbol:
                return column[2]    #EstadoIr, token
        return -1

    #Funcion que imprime la tabla de transicion del AFD
    def printTransitionTable(self, convert=False):

        matrixFinal = self.transitions     #Conseguimos la matriz de transciones
        allSymbols = []
        statesFrom = []
        #Recorremos Matrices de Transicion del AFD
        for column in matrixFinal:
            if column[1] not in allSymbols:     #Traer Simbolos
                allSymbols.append(column[1])  
            if column[0] not in statesFrom:
                statesFrom.append(column[0])    #Traes Estados Inciales
        #Recorrer Arreglo de simbolos
        print("\n  Estado | ",end="")
        for elem in allSymbols:
            out = ""
            if convert:
                if elem == Alphabet.range_num or elem == 'N':
                    out = "[0-9]"  
                elif elem == Alphabet.range_min or elem == 'a':
                    out = "[a-z]"  
                elif elem == Alphabet.range_may or elem == 'A':
                    out = "[A-Z]"
                elif elem == 'P':
                    out = "+"
                elif elem == 'M':
                    out = "-"
                elif elem == 'D':
                    out = "."
                else:
                    out = elem
            else:
                out = elem
            print("  {:>2}  |".format(out), end="")
        print("| token |", end="")
        print("\n")
        
        cont = 0
        for state in statesFrom:
            #Fila de Estados
            #Estado Inicial es de aceptacion
            if state == self.ini_state and state in self.end_states:
                print(" ->*{:>2}   | ".format(state), end="")
            elif state == self.ini_state:
                print(" -> {:>2}   | ".format(state), end="")
            elif state in self.end_states:
                print("  * {:>2}   | ".format(state), end="")
            else:
                print("    {:>2}   | ".format(state), end="")
            for symbol in allSymbols:
                car = self.funcion_transicion(matrixFinal,state,symbol)
                print('  {:>2}  |'.format(car),end="")
            #Imprimir Columna de Tokens
            for tupla in matrixFinal:
                if tupla[0] == state:
                    print("|  ",tupla[3]," |")
                    break
            cont = cont + 1


    #Funcion que genera un AFD apartir una de una expresion regular 
    # ademas de agregar un token dado, en su estado de aceptacion
    #Regresa un objeto AFD
    def createAFDexpRegular(regularExp, token=1):
        EXPReg = RegularExp(regularExp)
        AFNReg = EXPReg.createAFN()
        AFNReg.end_state.token = token  #Asigna el token al estado de aceptacion del AFN
        arrayAFD =  AFNReg.convert_to_afd() #Devuleve un arreglo de 3 parametros para crear un AFD 
        AFDReg = AFD(0, arrayAFD[0], arrayAFD[1], arrayAFD[2], arrayAFD[3])
                    #Inicial,      Aceptacion,    Transiciones,  Alfabeto
        return AFDReg

    #Funcion que une arreglo de expresiones regulares dando a cada un token diferente
    # Recibe arreglo de expresiones regulares, arreglo de tokenes (misma longitud),
    # y arreglo de caracteres (serviaran para la impresion correcta de la tabla)
    # Regresa un AFD
    def createSuperAFD(arrayRegExps, arrayTokens, arrayLetters = False):
        if isinstance(arrayRegExps,list) and isinstance(arrayTokens, list):
            if len(arrayRegExps) == len(arrayTokens):
                arrayAFNS = []
                #Se crean los AFNS a partir de la expreison Regular
                for i in range(0,len(arrayTokens)):
                    #Creamos el AFN con la expresion regular
                    RegExpAux = RegularExp(arrayRegExps[i])
                    AFNRegExpAux = RegExpAux.createAFN()
                    print(AFNRegExpAux)
                    #Lo insertamos en la lista de AFN's
                    arrayAFNS.append(AFNRegExpAux)
                #Llamamos al metodo de union de AFN's
                mainAFN = AFN.union_nAFN(arrayAFNS, arrayTokens)
                #Convertimos a AFD
                #Pasamos el alfabeto en el cual se mostaran la tabla de transiciones
                arrayAFD = mainAFN.convert_to_afd(arrayLetters)
                #Creamos el Objeto AFD
                AFDReturn = AFD(0, arrayAFD[0], arrayAFD[1], arrayAFD[2], arrayAFD[3])
                return AFDReturn
        else:
            print("Error")
            sys.exit() 

    #Metodo que verirfica si un conjunto existe en otro
    # sin importar el orden de los elementos de dicho conjunto
    #Recibe un conjunto de conjuntos y un conjunto de elementos
    #Devuelve un booleano
    def existThisSetIn(self, arraySets, set):
        if isinstance(arraySets, list) and isinstance(set, list):
            auxSet = set.copy()
            cont = 0
            for setA in arraySets:
                if len(setA) == len(auxSet):
                    for elemA in setA:
                        for elemB in auxSet:
                            if elemA == elemB:
                                cont = cont + 1
                                #Eliminamos el elemento que ya fue comparado
                                auxSet.pop(auxSet.index(elemA)) 
                                break
            if cont == len(set):
                return True
            return False
            
    #Metodo que analiza la tabla de transciones del automata
    #Recibe un estado inicial y un caracter
    #Retorna el valor del estado al que llega (valor enter)
    def transitionFuc(self, iniState, caracter, convert = False):
        for reng in self.transitions:
            #reng = [iniState, caracter, endState]
            if convert:
                if caracter.isdigit():
                    caracter = 'N'
                elif caracter == 'a'<=caracter<='z':
                    caracter = 'a'
                elif caracter == 'A'<=caracter<='A':
                    caracter = 'A'
                elif caracter == '+':
                    caracter = 'P'
                elif caracter == '-':
                    caracter = 'M'
                elif caracter == '.':
                    caracter = 'D'
            if reng[0] == iniState and reng[1] == caracter:
                return reng[2]
        return -1 

    #Metodo que devuleve el indice del conjunto al cual pertenece un estado
    #Recibe un arreglo de conjuntos de estados, y el estado
    #Retorna un valor entero > 0 si se encontro, -1 si no se encontro
    def belongTo(self, arraySets, state):
        for set in arraySets:
            if state in set:
                return arraySets.index(set)
        return -1

    
    #Metodo que minimiza la el AFD con el metodo "Conjunto Cociente"
    def minimize(self):
        #Atrapamos los estados de aceptacion y los no estados de aceptacion
        conjAccept = self.end_states    #Aceptacion
        conjNoAcpt = []
        #Conseguir estados de no aceptacion
        for st in self.all_states:
            if st not in conjAccept:
                conjNoAcpt.append(st)
        Q_EIni = [conjAccept, conjNoAcpt]   #Q_E0
        Q_EAux = []
        Q_E = []
        Q_E.extend(Q_EIni)
        #Empezamos a Iterar todos los conjuntos de estados
        while Q_E != Q_EAux:
            brokenSet = False
            #Primera Comparacion no entra en la condicion
            if len(Q_EAux) > 0:
                Q_E = Q_EAux.copy()
                Q_EAux = []
            #Comienza la interacion de conjuntos
            for set in Q_E:     #Analizar cada uno de los conjuntos
                for i in range(0,len(set)):
                    for j in range(i+1, len(set)):
                        arrayBelongA = []
                        arrayBelongB = []
                        for car in self.alphabet:
                            arrayBelongA.append(self.belongTo(Q_E, self.transitionFuc(set[i], car)))
                            arrayBelongB.append(self.belongTo(Q_E, self.transitionFuc(set[j], car)))
                            #Si alguna de los conjutnos a los cuales van dejan de coincidir detiene el ciclo
                            if arrayBelongA != arrayBelongB:
                                break
                        if arrayBelongA == arrayBelongB:
                            newQ_E = [set[i], set[j]]
                            excStates = []
                            #Revisamos que el nuevo conjunto no se encuentre ya en Q_E
                            if not self.existThisSetIn(Q_E,newQ_E):
                                #Operacion exclusion de conjuntos
                                oldArray = Q_E[Q_E.index(set)]
                                for state in oldArray:
                                    if state not in newQ_E:
                                        excStates.append(state)
                            brokenSet = False
                            if len(newQ_E) > 0 and not (self.existThisSetIn(Q_EAux, newQ_E)):
                                Q_EAux.append(newQ_E)
                            if len(excStates) > 0 and not self.existThisSetIn(Q_EAux, excStates):
                                Q_EAux.append(excStates)
                                brokenSet = True
                        if brokenSet:   #El conjunto con el que se esta operando se ha dividido
                            indexSet = Q_E.index(set)
                            for i in range(indexSet+1, len(Q_E)):
                                Q_EAux.append(Q_E[i])
                            break
                    if brokenSet:   
                        break
                if brokenSet:   
                        break
        
        print(Q_EAux) 

    #Metodo que analiza una cadena dada de acuerdo con las transiciones del automata
    #Recibe la cadena a analizar
    #Retorna un arreglo con tokens
    def analizeStr(self, string, convert=False):
        #Buscamos los tokens de cada estado
        arrayStatesTokens = []
        for state in self.all_states:
            for trans in self.transitions:
                if state == trans[0]:
                    arrayStatesTokens.append([state, trans[len(trans)-1]])
                    break
        arrayTokens = []
        actualState = self.ini_state    #Inciamos con el estado final del automata
        lastToken = -1
        wrongString = False
        cont = 0
        while cont < len(string):
            newState = self.transitionFuc(actualState, string[cont], convert)
            if  newState != -1:
                #Buscamos el token que corresponde con ese estado
                for elem in arrayStatesTokens:
                    if newState == elem[0]:
                        lastToken = elem[1]
                        break
                actualState = newState
                if cont == len(string)-1:
                    arrayTokens.append(lastToken)
            else:
                if lastToken != -1:     #Ctrl -z
                    # wrongString = True
                    actualState = self.ini_state
                    cont = cont - 1
                    arrayTokens.append(lastToken)
                    lastToken = -1
                else:
                    wrongString = True
            cont = cont + 1
            
            if wrongString:
                print("Hay un error en la cadena: '"+string+"' en la posicion [",cont,"]")
                sys.exit()
        return arrayTokens

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
def afd_main():
    #P = '+'            #M = '-'
    #N = '[0-9]'        #D = '.'
    #A = '[A-z]'        #a = '[a-z]'

    print()
    print("---- A   F   D ----")
    # RegExp1 = "(P|M)?&(N+)&D&(N+)"  #(+|-)?&[0-9]+&.&[0-9]+
    # RegExp2 = "(P|M)?&(N+)"         #(+!-)?&[0-9]?
    # RegExp3 = "(a|A)&(a|A|N)*"      #([a-z]|[A-Z])&([a-z]|[A-Z]|[0-9])*
    # RegExp4 = "P&P"                 #+&+
    # RegExp5 = "P"                   #+

    # arrayRegExp = [RegExp1, RegExp2, RegExp3, RegExp4, RegExp5]
    # arrayToken = [10,20,30,40,50]
    # alphabet = ['P', 'M', 'N', 'D', 'a', 'A']

    # mainAFD = AFD.createSuperAFD(arrayRegExp, arrayToken, alphabet)
    # # mainAFD.printTransitionTable()
    # tokens = mainAFD.analizeStr("15+10....1+a++9850+++aaaa")
    # print(tokens)

    #RegExpTest = "((m-o&b)+)|(c&d)|((0-2)*&(a-b))"
    RegFloat = "(+|-)?&(0-3)!&.&(0-3)!"
    # AFDTest = AFD.createAFDexpRegular(RegExpTest, 10)
    AFDFloat = AFD.createSuperAFD([RegFloat], [20])
    AFDFloat.printTransitionTable()
    TokenTest =AFDFloat.analizeStr("-2.231")
    print(TokenTest)
    # minAFD.analizeStr("aabaaba")
    # minAFD.printTransitionTable()
    # minAFD.minimize()

    # varCheck = mainAFD.existThisSetIn([['q','r'], ['p','q','r','t','s','u']], ['r', 'q', 's', 'u', 't', 'p'])
    # print(varCheck)

if __name__ == '__afd_main__':
    afd_main()  

import sys

from alphabet import Alphabet
from regEx import RegularExp
from AFN import AFN

class AFD():
    id_AFD = 0
    #Constructor de la clase AFD
    #ini_state (Entero)
    #end_state (Arreglo de enteros)
    #Alphabet (Arrelglo de: caracteres, simbolos especiales, palabras etc)
    #Token = ?
    def __init__(self, ini_state, end_states, transitions, alphabet, token = None):
        self.id_AFD = AFD.id_AFD
        AFD.id_AFD = AFD.id_AFD +1
        self.ini_state = ini_state
        self.end_states = end_states
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
    def printTransitionTable(self):

        matrixFinal = self.transitions     #Conseguimos la matriz de transciones
        allSymbols = []
        statesFrom = []
        
        for column in matrixFinal:
            if column[1] not in allSymbols:     #Traer Simbolos
                allSymbols.append(column[1])  
            if column[0] not in statesFrom:
                statesFrom.append(column[0])    #Traes Estados Inciales
        #Recorrer Arreglo de simbolos
        print("\n  Estado | ",end="")
        for elem in allSymbols:
            out = ""
            if elem == Alphabet.range_num:
                out = "[0-9]"  
            elif elem == Alphabet.range_min:
                out = "[a-z]"  
            elif elem == Alphabet.range_may:
                out = "[A-Z]"
            else:
                out = elem
            print("  {:>2}  |".format(out), end="")
        print("| token |", end="")
        print("\n")
        
        cont = 0
        for state in statesFrom:
            print("    {:>2}   | ".format(state), end="")
            for symbol in allSymbols:
                car = self.funcion_transicion(matrixFinal,state,symbol)
                print('   {:>2}  |'.format(car),end="")
            for tupla in matrixFinal:
                if tupla[0] == state:
                    print(" || ",tupla[3])
                    break
            cont = cont + 1


    #Funcion que genera un AFD apartir una de una expresion regular 
    # ademas de agregar un token dado, en su estado de aceptacion
    #Regresa un objeto AFD
    def createAFDexpRegular(string, token=None):
        EXPReg = RegularExp(string)
        AFNReg = EXPReg.createAFN()
        print(AFNReg)
        AFNReg.end_state.token = token  #Asigna el token al estado de aceptacion del AFN
        arrayAFD =  AFNReg.convert_to_afd() #Devuleve un arreglo de 3 parametros para crear un AFD 
        AFDReg = AFD(0, arrayAFD[0], arrayAFD[1], arrayAFD[2])
        return AFDReg

    #Funcion que une arreglo de expresiones regulares dando a cada un token diferebte
    # Recibe arreglo de expresiones regulares, arreglo de tokenes (misma longitud)
    # Regresa un AFD
    def union_nAFDs(arrayRegExps, arrayTokens, arrayLetters):
        if isinstance(arrayRegExps,list) and isinstance(arrayTokens, list):
            if len(arrayRegExps) == len(arrayTokens):
                arrayAFNS = []
                #Se crean los AFNS a partir de la expreison Regular
                for i in range(0,len(arrayTokens)):
                    #Creamos el AFN con la expresion regular
                    RegExpAux = RegularExp(arrayRegExps[i])
                    AFNRegExpAux = RegExpAux.createAFN()
                    #Lo insertamos en la lista de AFN's
                    arrayAFNS.append(AFNRegExpAux)
                # arrayAFNS.reverse()
                #Llamamos al metodo de union de AFN's
                mainAFN = AFN.union_nAFN(arrayAFNS, arrayTokens)
                #Convertimos a AFD
                arrayAFD = mainAFN.convert_to_afd(arrayLetters)
                #Creamos el Objeto AFD
                AFDReturn = AFD(0,arrayAFD[0], arrayAFD[1], arrayAFD[2])
                return AFDReturn
        else:
            print("Error")
            sys.exit() 
#P = '+'
#M = '-'
#N = '[0-9]'
#D = '.'
#A = '[A-z]'
#a = '[a-z]'
print("---- A   F   D ----")
RegExp1 = "(P|M)?&(N+)&D&(N+)"  #(+|-)?&[0-9]+&.&[0-9]+
RegExp2 = "(P|M)?&(N+)"         #(+!-)?&[0-9]?
RegExp3 = "(a|A)&(a|A|N)*"      #([a-z]|[A-Z])&([a-z]|[A-Z]|[0-9])*
RegExp4 = "P&P"                 #+&+
RegExp5 = "P"                   #+

arrayRegExp = [RegExp1, RegExp2, RegExp3, RegExp4, RegExp5]
arrayToken = [10,20,30,40,50]
alphabet = ['P', 'M', 'N', 'D', 'a', 'A']

mainAFD = AFD.union_nAFDs(arrayRegExp, arrayToken, alphabet)
mainAFD.printTransitionTable()

import sys

from alphabet import Alphabet

class AFD():
    id_AFD = 0
    #Constructor de la clase AFD
    #ini_state (Entero)
    #end_state (Arreglo de enteros)
    #Alphabet (Arrelglo de: caracteres, simbolos especiales, palabras etc)
    #Token = ?
    def __init__(self, ini_state, end_state, transitions, alphabet, token = None):
        self.id_AFD = AFD.id_AFD
        AFD.id_AFD = AFD.id_AFD +1
        self.ini_state = ini_state
        self.end_state = end_state
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
    def printTrasitionTable(self):
        matrixFinal = self.transitions     #Conseguimos la matriz de transciones
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

    #  --------------------------------------------------------------
    #           R E G L A S    G R A M A T I C A L E S
    #  --------------------------------------------------------------

    def getToken():
        car = self.thisString[self.apCarActual]




    #Funcion que genera un AFD apartir una de una expresion regular 
    # ademas de agregar un token dado, en su estado de aceptacion

    def createAFDexpRegular( string, token):



import sys

from AFN import AFN
from alphabet import Alphabet
from alphabet import Token

class RegularExp():

    #Reglas Gramaticales para construir un AFD a partir de una
    # expresion regular
    def __init__(self, stringAn):
        self.stringAn = stringAn
        self.apCarActual = 0
        self.stackSymbol = []

    def error(self):
        print("Error al analizar la cadena, en el caracter: ",self.apCarActual+1, " '",self.stringAn[self.apCarActual],"'")
        sys.exit()
    #Funcion que da  "un paso atras" en el apuntador de la cadena
    def backTrack(self):
        self.apCarActual = self.apCarActual - 1

    #Funcion que devuleve el Token de acuerdo con el caracter de la cadena que se esta analizando
    def getToken(self):
        if self.apCarActual < len(self.stringAn):
            car = self.stringAn[self.apCarActual]
            self.apCarActual = self.apCarActual + 1 #Incrementamos el apuntador del caracter Actual
            if car == Alphabet.symbol_PLUS:            #'+':
                return Token.symbol_PLUS
            elif car == Alphabet.symbol_STAR:       #'*'
                return Token.symbol_STAR
            elif car == Alphabet.symbol_OR:         #'|'
                return Token.symbol_OR
            elif car == Alphabet.symbol_CONC:       #'&'
                return Token.symbol_CONC
            elif car == Alphabet.symbol_PARI:       #'('
                return Token.symbol_PARI
            elif car == Alphabet.symbol_PARD:       #')'
                return Token.symbol_PARD
            elif car == Alphabet.symbol_INTER:      #'?'
                return Token.symbol_INTER
            else:                                   #a-z, A-Z, 0-9
                return Token.symbol_ALL
        else:
            return 0    #Se ha terminado de analizar la cadena

    
    def E(self):    #E -> TE'
        if(self.T()):
            if(self.Ep()):
                return True
        self.error()
        return False

    def Ep(self):   #E' -> OR TE'|Epsilon
        token = 0
        token = self.getToken()
        if(token == Token.symbol_OR):   # '|'
            if(self.T()):
                self.stackSymbol.append("|")   #Insertar en la pila simbolo de union
                if(self.Ep()):
                    return True
            self.error()
            return False
        #Si no Fue mas o menos etonces esta vacia osea "Epsilon"
        self.backTrack()
        return True

    def T(self):    #T -> CT'
        if(self.C()):
            if(self.Tp()):
                return True
        self.error()
        return False
    
    def Tp(self):   #T' -> &CT'|Epsilon
        token = 0
        token = self.getToken()
        if token == Token.symbol_CONC:
            if(self.C()):
                self.stackSymbol.append("&")   #Insertar en la pila simbolo de concatenacion
                if(self.Tp()):
                    return True
            self.error()
            return False
        #Si no Fue ambersal, es vacio "Epislon"
        self.backTrack()   #Regresamos
        return True 

    def C(self):    #C -> FC'
        if(self.F()):
            if(self.Cp()):
                return True
        self.error()
        return False
    
    def Cp(self):   #C' -> *C'|+C'|?C'|Epsilon
        token = 0
        token = self.getToken()
        if token == Token.symbol_STAR:
            self.stackSymbol.append("*")   #Insertar en la pila simbolo de cerradura de Kleene
            if self.Cp():
                return True
            self.error()
            return False
        elif token == Token.symbol_PLUS:
            self.stackSymbol.append("+")   #Insertar en la pila simbolo de cerradura de Positiva
            if self.Cp():
                return True
            self.error()
            return False
        elif token == Token.symbol_INTER:
            self.stackSymbol.append("?")   #Insertar en la pila simbolo de Opcional
            if self.Cp():
                return True
            self.error()
            return False
        
        #Si no Fue mas o menos etonces esta vacia osea "Epsilon"
        self.backTrack()
        return True
    
    def F(self):
        token = 0
        token = self.getToken()
        if token == Token.symbol_PARI: 
            if self.E():
                token = self.getToken()
                if token == Token.symbol_PARD:
                    return True
            self.error()
            return False
        elif token == Token.symbol_ALL:
            self.stackSymbol.append(self.stringAn[self.apCarActual-1])   #Insertar en la pila simbolo de un caracter
            return True
    
    #Crea un AFN apartir de la expresion Regular
    #Returna un Objeto AFN
    def createAFN(self):
        self.E()        #Crear pila de simbolos
        self.stackSymbol.reverse()
        stackSym = self.stackSymbol #Invertir Simbolos
        stackAutomata = []
        while len(stackSym) > 0:
            #Sacar cada elemento de pila
            car = stackSym.pop()
            # |
            if car == Alphabet.symbol_OR:   
                #Sacar los dos ultimos automatas de la pila de Automtas
                # Para hacer la operacion union, y meterlo de nuevo en la pila
                AFN1 = stackAutomata.pop() 
                AFN2 = stackAutomata.pop()
                AFNUnion = AFN1.union(AFN2)
                stackAutomata.append(AFNUnion)  #Lo insertamos en la pila
            # &
            elif car == Alphabet.symbol_CONC:   
                #Sacar los dos ultimos automatas de la pila de Automtas
                # Para hacer la operacion concatenacion, y meterlo de nuevo en la pila
                AFN1 = stackAutomata.pop() 
                AFN2 = stackAutomata.pop()
                AFNConc = AFN2.concatenate(AFN1)
                stackAutomata.append(AFNConc)  #Lo insertamos en la pila
            # ?
            elif car == Alphabet.symbol_INTER:
                #Operacion Opcional del ultimo automata en la pila
                AFN1 = stackAutomata.pop()
                AFNOp = AFN1.optional()
                stackAutomata.append(AFNOp)  #Lo insertamos en la pila
            # +
            elif car == Alphabet.symbol_PLUS:
                #Operacion Positiva del ultimo automata en la pila
                AFN1 = stackAutomata.pop()
                AFNPo = AFN1.kleene_plus()
                stackAutomata.append(AFNPo)  #Lo insertamos en la pila
            # *
            elif car == Alphabet.symbol_STAR:
                #Operacion Positiva del ultimo automata en la pila
                AFN1 = stackAutomata.pop()
                AFNS = AFN1.kleene_star()
                stackAutomata.append(AFNS)  #Lo insertamos en la pila
            #Crear un autamata basico con el caracter
            else:
                AFNBasic = AFN.createBasicAutomata(car)
                stackAutomata.append(AFNBasic)  #Insertar en la pila
        #Devolver el automata creado
        FinalAFN = stackAutomata.pop()
        return FinalAFN

#Ejemplo de Como Crear un AFN a partir de una expresion regular

# EXP1 = RegularExp("((a&b)?)|(c&d)|((e&f)|z?)|n?|(d&.&d)")  
# print(EXP1.stackSymbol)
# AFNR = EXP1.createAFN()
# print(AFNR)

        

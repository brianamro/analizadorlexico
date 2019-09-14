

from AFN import AFN
from alphabet import Alphabet
from alphabet import Token

class RegularExp():

    #Reglas Gramaticales para construir un AFD a partir de una
    # expresion regular
    def __init__(self, stringAn):
        self.stringAn = stringAn
        self.apCarActual = 0

    def error(self):
        print("Error al analizar la cadena, en el caracter: ",self.apCarActual, " '",self.stringAn[self.apCarActual],"'")
    
    #Funcion que da  "un paso atras" en el apuntador de la cadena
    def backTrack(self):
        self.apCarActual = self.apCarActual - 1

    #Funcion que devuleve el Token de acuerdo con el caracter de la cadena que se esta analizando
    def getToken(self):
        # print("Car actual: ", self.stringAn[self.apCarActual])
        # print("Longitud: ", len(self.stringAn))
        if self.apCarActual < len(self.stringAn):
            car = self.stringAn[self.apCarActual]
            self.apCarActual = self.apCarActual + 1 #Incrementamos el apuntador del caracter Actual
            if car == Token.symbol_PLUS:            #'+':
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
            return 100    #Se ha terminado de analizar la cadena

    
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
                print("|")
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
                print("&")
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
            print("*")
            if self.Cp():
                return True
            self.error()
            return False
        elif token == Token.symbol_PLUS:
            print("+")
            if self.Cp():
                return True
            self.error()
            return False
        elif token == Token.symbol_INTER:
            print("?")
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
            print("(")
            if self.E():
                token = self.getToken()
                if token == Token.symbol_PARD:
                    print(")")
                    return True
            self.error()
            return False
        elif token == Token.symbol_ALL:
            print("car ",self.stringAn[self.apCarActual-1])
            return True
    
    def analizeStr(self):
        self.E()

EXP1 = RegularExp("((a&b)?)|(c&d)|((e&f)|z?)&(a*&s+fgdas)")
EXP1.analizeStr()
        

import sys

from transition import Transition
from transition import Epsilon
from state import State

class AFN:
    id_State = 0
    def __init__(self, ini_state, end_state, transitions, states):
        if isinstance(transitions, list):
            self.ini_state = ini_state
            self.end_state = end_state
            self.transitions = transitions
            self.states = states
            self.id_State = AFN.id_State
            AFN.id_State = AFN.id_State + 1
        else:
            print("Las transiciones deben ser un arreglo")
            sys.exit()
    
    def __str__(self):
        Out  = "\nAFN: "+str(self.id_State)+"\n"
        Out  += "Ini: "+str(self.ini_state)+"\n"
        for trans in self.transitions:
            Out += str(trans)+"\n"
        Out += "Acc: "+str(self.end_state)
        return Out
    def
    
    def createBasicAutomata(car):
        iniSt = State()
        endSt = State(True)
        trans = Transition(iniSt, endSt, car)
        basicAFN = AFN(iniSt, endSt, [trans])
        return basicAFN
    
    def union(self, AFN2):
        iniSt = State()
        endSt = State(True)
        #Borramos el estado de aceptacion de los AFN
        self.end_state.deleteAccept()   
        AFN2.end_state.deleteAccept()   
        #Creamos las nuevas Trancisiones
        t1_i = Transition(iniSt, self.ini_state, Epsilon.symbol)
        t1_e = Transition(self.end_state, endSt, Epsilon.symbol)
        t2_i = Transition(iniSt, AFN2.ini_state, Epsilon.symbol)
        t2_e = Transition(AFN2.end_state, endSt, Epsilon.symbol)
        #Agregamos todas las transiciones
        allTrans = [t1_i,t1_e, t2_i, t2_e]
        for trans in self.transitions:
            allTrans.append(trans)
        for trans in AFN2.transitions:
            allTrans.append(trans)

        newAFN = AFN(iniSt, endSt, allTrans)
        return newAFN
    
    def concatenate(self, AFN2):
        #Nuevos estados final e inicial
        iniSt = State()
        endSt = State()
        #Borramos estados de aceptacion
        self.end_state.deleteAccept()
        AFN2.end_state.deleteAccept()
        #Nuevas transiciones
        tini = Transition(iniSt, self.ini_state, Epsilon.symbol)
        tinter = Transition(self.end_state, AFN2.ini_state, Epsilon.symbol)
        tend = Transition(AFN2.end_state, endSt, Epsilon.symbol)
        #Juntamos todas las transiciones para el nuevo atomata
        allTrans = [tini, tinter, tend]
        for trans in self.transitions:
            allTrans.append(trans)
        for trans in AFN2.transitions:
            allTrans.append(trans)

        newAFN = AFN(iniSt, endSt, allTrans)
        return newAFN

AFN1 = AFN.createBasicAutomata('a')
print(AFN1)
AFN2 = AFN.createBasicAutomata('b')
print(AFN2)
AFNU = AFN1.union(AFN2)
print(AFNU)
AFNCon = AFN1.concatenate(AFN2)
print(AFNCon)
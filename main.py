from AFN import AFN
from AFN import Alphabet
from AFD import AFD
import pickle
import os


# EN esta variable se guardarán todas las expresiones 
# regulares
regex_stack = []
# En esta variable se guardarán los token asignados a cada
# AFD 
tokens_stack = []
# En esta variable se guardarán los AFD para anlisis
# léxico a partir de un arreglo de expresiones regulares
afd_stack = []
# En esta variable se guardarán todos los automatas no deterministas
# que vayamos creando
automata_stack = []
# Esta función hará el papel del menú para crear automatas 
def menu_automata():
    os.system('cls||clear')   
    opcion = True
    while opcion == True:
        print()
        print("------------- AUTOMATAS ------------------")
        print("1. Crear autómata básico")
        print("2. Cerradura de Kleen de un automata (*)")
        print("3. Cerradura positiva de un automata (+)")
        print("4. Cerradura opcional de un automat (?)")
        print("5. Unir dos automatas")
        print("6. Concatenar automatas")
        print("7. Guardar automata")
        print("8. Cargar automata")
        print("9. Salir al menú principal")
        entrada = input("Ingresa una opción: ")
        if entrada.isdigit():
            opc = int(entrada)
            print()
            if opc == 9:
                print("Saliendo de Crear automatas...")
                main()
                opcion = False
            else:
                if opc == 1:
                    print()
                    print("  Creando automata básico..")
                    caracter = input("Ingresa el caracter: ")
                    nombre = "AFN_"+caracter
                    nombre = AFN.createBasicAutomata(caracter)
                    automata_stack.append(nombre)
                    print("ID de automata: ",automata_stack.index(nombre))
                    #print(nombre)
                    opcion = True
                elif opc == 2:
                    print("  Aplicando cerradura de Kleene..")
                    indice = int(input("Ingresa el ID del automata: "))
                    if indice < len(automata_stack) and len(automata_stack) >= 0:
                        
                        nuevo = automata_stack[indice].kleene_star()
                        automata_stack[indice] = nuevo
                        print("ID de automata: ",automata_stack.index(nuevo))
                        print(nuevo)
                        opcion = True
                    else:
                        print("ERROR: Ingresa un automata valido")
                        opc = 2
                        opcion = True
                elif opc == 3:
                    print(" Aplicando cerradura postiva...")
                    indice = int(input("Ingresa el ID del automata: "))
                    if indice < len(automata_stack) and len(automata_stack) >= 0:
                        nuevo = automata_stack[indice].kleene_plus()
                        automata_stack[indice] = nuevo
                        print("ID de automata: ",automata_stack.index(nuevo))
                        print(nuevo)
                        opcion = True
                    else:
                        print("ERROR: ingresa un automata válido")
                        opcion = True
                elif opc == 4:
                    print()
                    print("  Aplicando cerradura opcional..")
                    indice = int(input("Ingresa el ID del automata: "))
                    if indice < len(automata_stack) and len(automata_stack) >= 0:
                        nuevo = automata_stack[indice].optional()
                        automata_stack[indice] = nuevo
                        print("ID de automata: ",automata_stack.index(nuevo))
                        print(nuevo)
                        opcion = True
                    else:
                        print("ERROR: ingresa un automata válido")
                        opcion = True
                elif opc == 5:
                    if len(automata_stack) > 1:
                        print()
                        print("  Uniendo automatas...")
                        id_1 = int(input("Ingresa el ID del automata 1: "))
                        id_2 = int(input("Ingresa el ID del automata 2: "))
                        if id_1 < len(automata_stack) and id_2 < len(automata_stack):
                            nuevo = automata_stack[id_1].union(automata_stack[id_2])
                            automata_stack[id_1] = nuevo
                            automata_stack.pop(id_2)
                            print("ID de automata: ",automata_stack.index(nuevo))
                            print(nuevo)
                            opcion = True
                        else:
                            print("ERROR: ingresa un automata válido")
                            opcion = True
                    else:
                        print("ERROR: No hay suficientes autómatas")
                        opcion = True
                elif opc == 6:
                    if len(automata_stack) > 1:
                        print()
                        print("  Concatenando 2 automatas...")
                        id_1 = int(input("Ingresa el ID del automata 1: "))
                        id_2 = int(input("Ingresa el ID del automata 2: "))
                        if id_1 < len(automata_stack) and id_2 < len(automata_stack):
                            nuevo = automata_stack[id_1].concatenate(automata_stack[id_2])
                            automata_stack[id_1] = nuevo
                            automata_stack.pop(id_2)
                            print("ID de automata: ",automata_stack.index(nuevo))
                            print(nuevo)
                            opcion = True
                        else:
                            print("ERROR: ingresa un automata válido")
                            opcion = True    
                    else:
                        print("ERROR: No hay suficientes autómatas")
                        opcion = True
                elif opc == 7:
                    if len(automata_stack) >= 1:
                        print("  Guardando autómata...")
                        entrada = input("Ingresa el ID del autómata a guardar: ")
                        if entrada.isdigit() and int(entrada)>=0:
                            id = int(entrada)
                            automata = automata_stack[id]
                            archivo = open("automatas.pickle","wb")
                            pickle.dump(automata,archivo)
                            archivo.close()
                            print("Guardado exitoso!")
                            print()
                        else:
                            print("Entrada no valida")
                    else:
                        print("ERROR: No hay automatas")
                elif opc == 8:
                    id_aux = input("Ingresa el ID del autómata a imprimir")
                    if id_aux.isdigit():
                        if id_aux < len(automata_stack):
                            print(automata_stack[id_aux])
                    else:
                        print("ERROR: entrada no valida")
                        opcion = True
                            

                else:
                    print("ERROR: opción no valida")
                    opcion = True
        else:
            print("ERROR: entrada invalida") 
            opcion = True           

def menu_lex():
    print("-- ANÁLISIS LÉXICO ---")
    print("1. Añadir una expresión regular")
    print("2. Crear un analizador léxico a partir de las")
    print("   expresiones regulares introducidas")
    print("3. Analizar una cadena con un analizador léxico")
    print("4. Regresar al menu principal")
    OPC = input("Ingresa una opción: ")
    os.system('cls||clear')
    if OPC.isdigit():
        if int(OPC) == 1:   
            regexAux = input("Ingresa la expresión regular: ")
            if regexAux not in regex_stack:
                regex_stack.append(regexAux)
                print("Expresión regular agregada")
                tokenAux = input("Ingresa token: ")
                if tokenAux.isdigit():
                    tokens_stack.append(int(tokenAux))
                    print("Token agregado")
                elif tokenAux in tokens_stack:
                    print("Token ya existente.")
                else:
                    print("Token no valido")
            else: 
                print("Expresión ya asignada")
            menu_lex()
        elif int(OPC) == 2:
            if len(regex_stack) > 0:
                print("")
                os.system('cls||clear')
                print("... Creando analizador léxico ...")
                superAFDaux = AFD.createSuperAFD(regex_stack,tokens_stack)
                afd_stack.append(superAFDaux)
                superAFDaux.printTransitionTable()
                print("AFD creado correctamente!")
                print(f"AFD ID: {afd_stack.index(superAFDaux)}")
                regex_stack.clear()
            else:
                print("No hay suficientes expresiones regulares")
            menu_lex()
        elif int(OPC) == 3:
            if len(afd_stack) > 0:
                id_aux = input("Ingresa el ID del AFD a usar: ")
                if int(id_aux) < len(afd_stack):
                    cadena = input("Ingresa una cadena: ")
                    tokenTest = afd_stack[int(id_aux)].analizeStr(cadena)
                    print(tokenTest)
                else:
                    print("Error: ese automata no existe")
            else:
                print("ERROR: no hay automatas")
            menu_lex()
        elif int(OPC) == 4:
            main()

    else:
        print("Ingresa una opción válida")
        menu_lex()


def main():
    print("---------------------------------------------------")
    print("")
    print("------ BIENVENIDO AL ANALIZADOR SINTÁCTICO --------")
    print("")
    print("---------------------------------------------------")
    print("")
    print("1. Crear un automata a partir de automatas básicos")
    print("2. Análisis sintáctico dadas expresiones regulares")
    opcion = input("Ingresa una opción: ")
    if opcion.isdigit():
        os.system('cls||clear')   
        if int(opcion) == 1:
            menu_automata()
        elif int(opcion) == 2:
            menu_lex()
        else:
            print("Ingrese una opción valida")
            main()
    else:
        print("Ingrese una opción valida")
        main()
    
    

            

    # #--------------  M  A  I  N  --------------

    # #Crear automata (+|-)?&[0-9]+&.&[0-9]+
    # AFN1_main = AFN.createBasicAutomata('+')
    # AFN1_men = AFN.createBasicAutomata('-')
    # AFN1_nrA = AFN.createBasicAutomata(Alphabet.range_num) #0-9
    # AFN1_poi = AFN.createBasicAutomata('.')
    # AFN1_nrB = AFN.createBasicAutomata(Alphabet.range_num) #0-9

    # AFN1_main = AFN1_main.union(AFN1_men)   #(+|-)    
    # AFN1_main = AFN1_main.optional()        #(+|-)?
    # AFN1_nrA = AFN1_nrA.kleene_plus()       #[0-9]+
    # AFN1_nrB = AFN1_nrB.kleene_plus()       #[0-9]+
    # AFN1_main = AFN1_main.concatenate(AFN1_nrA)     #(+|-)?&[0-9]+
    # AFN1_main = AFN1_main.concatenate(AFN1_poi)     #(+|-)?&[0-9]+&.
    # AFN1_main = AFN1_main.concatenate(AFN1_nrB)     #(+|-)?&[0-9]+&.&[0-9]+
    # print("\nAFN1 (+|-)?&[0-9]+&.&[0-9]+\n")
    # # matriz = AFN1_main.tableAFD()
    # #func
    
    # #Crear Autonata (+!-)?&[0-9]?
    # AFN2_main = AFN.createBasicAutomata('+')
    # AFN2_men = AFN.createBasicAutomata('-')
    # AFN2_nrA = AFN.createBasicAutomata(Alphabet.range_num)

    # AFN2_main = AFN2_main.union(AFN2_men)   #(+|-)    
    # AFN2_main = AFN2_main.optional()        #(+|-)?
    # AFN2_nrA = AFN2_nrA.kleene_plus()      #[0-9]+
    # AFN2_main = AFN2_main.concatenate(AFN2_nrA)     #(+|-)?&[0-9]+
    # print("\nAFN2: (+|-)?&[0-9]+&.&[0-9]+\n")
    # # print(AFN2_main.convert_to_afd())

    # #Crear Automata ([a-z]|[A-Z])&([a-z]|[A-Z]|[0-9])*
    # AFN3_main = AFN.createBasicAutomata(Alphabet.range_min) #[a-z]
    # AFN3_may1 = AFN.createBasicAutomata(Alphabet.range_may)  #[A-Z]
    # AFN3_min1 = AFN.createBasicAutomata(Alphabet.range_min) #[a-z]
    # AFN3_may2 = AFN.createBasicAutomata(Alphabet.range_may)  #[A-Z]
    # AFN3_num = AFN.createBasicAutomata(Alphabet.range_num)  #[A-Z]

    # AFN3_num = AFN3_num.union(AFN3_may2)            #AFN3_num = [A-Z]|[0-9]
    # AFN3_num = AFN3_num.union(AFN3_min1)            #AFN3_num = [A-Z]|[0-9]|[a-z]
    # AFN3_num = AFN3_num.kleene_star()               #AFN3_num = ([A-Z]|[0-9]|[a-z])*

    # AFN3_main = AFN3_main.union(AFN3_may1)          #AFN3_main = ([a-z]|[A-Z])
    # AFN3_main = AFN3_main.concatenate(AFN3_num)     #AFN3_main = ([a-z]|[A-Z]) & ([A-Z]|[0-9]|[a-z])*

    # print("\nAFN3: (a-z)(A-Z)&([a-z]|[A-Z]|[0-9])*n")
    # # print(AFN3_main.convert_to_afd())

    # #Crear Automata +&+
    # AFN4_main = AFN.createBasicAutomata('+')
    # AFN4_plus = AFN.createBasicAutomata('+')
    # AFN4_main = AFN4_main.concatenate(AFN4_plus)
    # print("\nAFN4: +&+\n")
    # # print(AFN4_main.convert_to_afd())

    # #Crear Automata +
    # AFN5_main = AFN.createBasicAutomata('+')
    # print("\nAFN5: +\n")
    # # print(AFN5_main.convert_to_afd())

    # #AUTOMATA GRANDE UNION DE LOS 5 ANTERIORES
    # mainAFN = AFN1_main.union(AFN2_main)    #mainAFN = AFN1 | AFN2
    # mainAFN = mainAFN.union(AFN3_main)      #mainAFN = (AFN1 | AFN2) | AFN3
    # mainAFN = mainAFN.union(AFN4_main)      #mainAFN = ((AFN1 | AFN2) | AFN3) | AFN4
    # mainAFN = mainAFN.union(AFN5_main)      #mainAFN = (((AFN1 | AFN2) | AFN3) | AFN4) | AFN5

    # print("\nMAIN AUTOMATA\n")
    # mainAFN2 = AFN.union_nAFN([AFN1_main,AFN2_main,AFN3_main,AFN4_main,AFN5_main])
    # mainAFN2.tableAFD()


if __name__ == '__main__':
    main() 
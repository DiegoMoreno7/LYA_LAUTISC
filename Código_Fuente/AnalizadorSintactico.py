#analizador Sintactico
import ply.yacc as yacc
from AnalizadorLexico import tokens  # Importa tokens desde archivo léxico
import sys
import io
from TablaSimbolos import SymbolTable
from AnalizadorSemantico import *

def limpiar_errores():
    global lista_errores_sintacticos
    lista_errores_sintacticos = []
    global errores_Sinc_Desc
    errores_Sinc_Desc = []
    global lista_errores_semanticos
    lista_errores_semanticos = []
    global errores_Sem_Desc
    errores_Sem_Desc = []
    global tabla_simbolos
    tabla_simbolos = SymbolTable()

global lista_errores_sintacticos
lista_errores_sintacticos = []
global errores_Sinc_Desc
errores_Sinc_Desc = []
global lista_errores_semanticos
lista_errores_semanticos = []
global errores_Sem_Desc
errores_Sem_Desc = []

global tabla_simbolos
tabla_simbolos = SymbolTable()

linea = 0

precedence = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
    ('left', 'IGUAL', 'DIFERENTE'),
    ('left', 'MENORQUE', 'MENORIGUAL', 'MAYORQUE', 'MAYORIGUAL'),
)

# Programa principal
def p_programa(p):
    """
    programa : BEGIN bloque_codigo END
    """
    p[0] = ('programa', p[2])


# Bloque de código
def p_bloque_codigo(p):
    """
    bloque_codigo : LLAVE_A lista_declaraciones LLAVE_C
    """
    p[0] = ('bloque_codigo', p[2])

# Lista de declaraciones
def p_lista_declaraciones(p):
    """
    lista_declaraciones : lista_declaraciones lista_declaraciones
                        | declaracion
                        | si
                        | mientras
                        | for_loop
                        | graImport
                        | funcion
                        | mover
                        | posicion
                        | abrir
                        | llamadafunc
                        | imprimir
    """
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

#DEFINIR CADENAS
#----------- Validar cadenas dentro de las comillas del SMS -------------
def p_listaExpresiones(p):
    """
    lista_expresiones : CADENA 
                      | ID
                      | lista_expresiones SUMA CADENA
                      | lista_expresiones SUMA ID
                      

    """
    if len(p) == 2:
        p[0] = [p[1]]
    else: 
        p[0]=p[1] + [p[3]]   
#---------------------Imprimir cadenas----------------
def p_imprimirPantalla(p):
    """
    imprimir : SMS PARENTESIS_A lista_expresiones PARENTESIS_B PUNTOCOMA            
    """
    if len(p)==8:
        for expresion in p[4]:  # p[4] contiene la lista de expresiones
         print(expresion)
        p[0]="Imprimir",p[4]
        print(p[3])
    else:
        print(p[3])
        p[0]="imprimir",p[3]

#-----------------------------------------------------------------------#
def p_imprimirPantallaError(p):
    """
    imprimir : SMS PARENTESIS_A lista_expresiones PARENTESIS_B 
                          
    """
    errores_Sinc_Desc.append("Error sintactico en la linea: "+str(p.lineno(2)-linea)+
                            "\nFalta punto y coma cerca de: "+"'"+p[4]+"'"+
                             "\nSe espera SMS PARENTESIS_A lista_expresiones PARENTESIS_B PUNTOCOMA"+
                             "\n                                                          ^^^^^^^^^"+
                             "\nPruebe con: "+str(p[1])+str(p[2])+str(p[3])+str(p[4])+";")
    
def p_imprimirPantallaError2(p):
    """
    imprimir : SMS PARENTESIS_A lista_expresiones PUNTOCOMA
                          
    """
    errores_Sinc_Desc.append("Error sintactico en la linea: "+str(p.lineno(2)-linea)+
                             "\nFalta parentesis B (')') cerca de: "+"'"+str(p[3])+"'"+
                             "\nSe espera SMS PARENTESIS_A lista_expresiones PARENTESIS_B PUNTOCOMA"+
                             "\n                                             ^^^^^^^^^^^^"+
                             "\nPruebe con: "+str(p[1])+str(p[2])+str(p[3])+")"+str(p[4]))

def p_imprimirPantallaError3(p):
    """
    imprimir : SMS PARENTESIS_A PARENTESIS_B PUNTOCOMA
                          
    """
    errores_Sinc_Desc.append("Error sintactico en la linea: "+str(p.lineno(2)-linea)+
                             "\nSMS Sin argumentos cerca de: "+"'"+str(p[2])+"'"+
                             "\nSe espera SMS PARENTESIS_A lista_expresiones PARENTESIS_B PUNTOCOMA"+
                             "\n                           ^^^^^^^^^^^^^^^^^"+
                             "\nPruebe con: "+str(p[1])+str(p[2])+"ExpresionesAImprimir"+str(p[3])+str(p[4]))

def p_imprimirPantallaError4(p):
    """
    imprimir : SMS lista_expresiones PARENTESIS_B PUNTOCOMA
                          
    """
    errores_Sinc_Desc.append("Error sintactico en la linea: "+str(p.lineno(2)-linea)+
                             "\nFalta parentesis A ('()') cerca de: "+"'"+str(p[2])+"'"+
                             "\nSe espera SMS PARENTESIS_A lista_expresiones PARENTESIS_B PUNTOCOMA"+
                             "\n              ^^^^^^^^^^^^"+
                             "\nPruebe con: "+str(p[1])+"("+str(p[2])+str(p[3])+str(p[4]))
 
def p_imprimirPantallaError5(p):
    """
    imprimir : PARENTESIS_A lista_expresiones PARENTESIS_B PUNTOCOMA
                          
    """
    errores_Sinc_Desc.append("Error sintactico en la linea: "+str(p.lineno(2)-linea)+
                             "\nPosible Funcion de SMS cerca de: "+"'"+str(p[2])+"'"+
                             "\nSe espera SMS PARENTESIS_A lista_expresiones PARENTESIS_B PUNTOCOMA"+
                             "\n          ^^^"+
                             "\nPruebe con: SMS "+str(p[1])+str(p[2])+str(p[3])+str(p[4]))
 

   


def p_declaracion(p):
    """
    declaracion : tipo ID ASIGNACION expresion PUNTOCOMA
    """
    if(p[4] == 'True'):
        p[4] = True
    elif(p[4] == 'False'):
        p[4] = False
    if(tabla_simbolos.insertar_variable(p[2], p[1], p[4])):
        errores_Sem_Desc.append("Error semántico en la linea "+str(p.lineno(2)-linea)+": La variable "+p[2]+" ya ha sido declarada")
    else:
        try:
            verificar_asignacion(tabla_simbolos, p[2], str(p[4]), p.lineno(2)-linea)
        except Exception as e:
            errores_Sem_Desc.append(str(e))
    
    if len(p) == 6:
        p[0] = ('declaracion', p[1], p[2], p[4])
    else:
        p[0] = p[1]

def p_declaracionsintipo(p):
    """
    declaracion : ID ASIGNACION expresion PUNTOCOMA
    """
    try:
        verificar_asignacion(tabla_simbolos, p[1], str(p[3]), p.lineno(2)-linea)
    except Exception as e:
        errores_Sem_Desc.append(str(e))
  

#-----------------Crear Objeto------------------------------
def p_declaracion_crearObj(p):
    '''declaracion : ID ASIGNACION CO ID PUNTOCOMA'''

#-----------------Arreglo------------------------------
def p_declaracion_crearArreglo(p):
    '''declaracion : ID ASIGNACION CA CORCHETE_A NUMERO CORCHETE_B PUNTOCOMA'''

def p_ElementoArreglo(p):
    '''
    elementoArr : ID CORCHETE_A expresion CORCHETE_B
                | ID CORCHETE_A atrObjeto CORCHETE_B
                | ID CORCHETE_A elementoArr CORCHETE_B
    '''

def p_declaracion_AsignarArreglo(p):
    '''declaracion : elementoArr ASIGNACION expresion PUNTOCOMA
                   | elementoArr ASIGNACION True PUNTOCOMA
                   | elementoArr ASIGNACION False PUNTOCOMA'''

# Tipos de datos
def p_tipo(p):
    """
    tipo : int
         | bool
         | stg
         | real
    """
    p[0] = p[1]

# Expresiones
def p_expresion_suma(p):
    'expresion : expresion SUMA expresion'
    tipo = TipoValor(str(p[1]))
    tipo2 = TipoValor(str(p[3]))
    if(tipo == 'bool' or tipo == 'stg' or tipo==None or tipo2 == 'bool' or tipo2 == 'stg' or tipo2==None):
        errores_Sem_Desc.append("Error semántico en la linea "+str(p.lineno(2)-linea)+": La operacion no es compatible con los tipos")
    else:
        p[0] = p[1] + p[3]

def p_expresion_resta(p):
    'expresion : expresion RESTA expresion'
    tipo = TipoValor(str(p[1]))
    tipo2 = TipoValor(str(p[3]))
    if(tipo == 'bool' or tipo == 'stg' or tipo==None or tipo2 == 'bool' or tipo2 == 'stg' or tipo2==None):
        errores_Sem_Desc.append("Error semántico en la linea "+str(p.lineno(2)-linea)+": La operacion no es compatible con los tipos")
    else:
        p[0] = p[1] - p[3]

def p_expresion_mult(p):
    'expresion : expresion MULTIPLICACION expresion'
    tipo = TipoValor(str(p[1]))
    tipo2 = TipoValor(str(p[3]))
    if(tipo == 'bool' or tipo == 'stg' or tipo==None or tipo2 == 'bool' or tipo2 == 'stg' or tipo2==None):
        errores_Sem_Desc.append("Error semántico en la linea "+str(p.lineno(2)-linea)+": La operacion no es compatible con los tipos")
    else:
        p[0] = p[1] * p[3]

def p_expresion_div(p):
    'expresion : expresion DIVISION expresion'
    tipo = TipoValor(str(p[1]))
    tipo2 = TipoValor(str(p[3]))
    if(tipo == 'bool' or tipo == 'stg' or tipo==None or tipo2 == 'bool' or tipo2 == 'stg' or tipo2==None):
        errores_Sem_Desc.append("Error semántico en la linea "+str(p.lineno(2)-linea)+": La operacion no es compatible con los tipos")
    else:
        if p[3] != 0:
            p[0] = p[1] / p[3]
            if(p[0]%1 == 0):
                p[0] = int(p[0])
        else:
            errores_Sem_Desc.append("Error semántico en la linea "+str(p.lineno(2)-linea)+": No se puede dividir por cero")
            p[0] = None

def p_expresion_comparacion(p):
    '''
    expresion : expresion MENORQUE expresion
              | expresion MENORIGUAL expresion
              | expresion MAYORQUE expresion
              | expresion MAYORIGUAL expresion
    '''
    tipo = TipoValor(str(p[1]))
    tipo2 = TipoValor(str(p[3]))
    if(tipo == 'bool' or tipo == 'stg' or tipo==None or tipo2 == 'bool' or tipo2 == 'stg' or tipo2==None):
        errores_Sem_Desc.append("Error semántico en la linea "+str(p.lineno(2)-linea)+": La operacion no es compatible con los tipos")
    else:
        if p[2] == '<':
            p[0] = p[1] < p[3]
        elif p[2] == '<=':
            p[0] = p[1] <= p[3]
        elif p[2] == '>':
            p[0] = p[1] > p[3]
        elif p[2] == '>=':
            p[0] = p[1] >= p[3]

def p_expresion_comparacion2(p):
    '''
    expresion : expresion IGUAL expresion
              | expresion DIFERENTE expresion
    '''
    tipo = TipoValor(str(p[1]))
    tipo2 = TipoValor(str(p[3]))
    if(tipo==None or tipo2==None):
        errores_Sem_Desc.append("Error semántico en la linea "+str(p.lineno(2)-linea)+": La operacion no es compatible con los tipos")
    else:
        if p[2] == '==':
            p[0] = p[1] == p[3]
        elif p[2] == '!=':
            p[0] = p[1] != p[3]

def p_expresion(p):
    """
    expresion : PARENTESIS_A expresion PARENTESIS_B
              | NUMERO
              | REAL
              | CADENA
              | True
              | False
              | posicion
    """
    p[0] = p[1]

def p_expresionId(p):
    """
    expresion : ID
    """
    valorVar = tabla_simbolos.Buscar(p[1])
    if(valorVar != None):
        if(valorVar['type'] != 'funcion'):
                p[0] = valorVar['value']
        else:
            p[0] = 'funcion'
    else:
        errores_Sem_Desc.append("Error semántico en la linea "+str(p.lineno(1)-linea)+": La variable "+p[1]+" no ha sido declarada")


# Operadores
def p_operador(p):
    """
    operador : SUMA
             | RESTA
             | MULTIPLICACION
             | DIVISION
             | IGUAL
             | DIFERENTE
             | MENORQUE
             | MAYORQUE
             | MENORIGUAL
             | MAYORIGUAL
             | AND
             | OR
             | NOT
    """
    p[0] = p[1]

def p_si(p):
    """
    si : IF PARENTESIS_A expresion PARENTESIS_B bloque_codigo
       | IF PARENTESIS_A expresion PARENTESIS_B bloque_codigo ELSE bloque_codigo
    """
    if(p[3] == True or p[3] == False):
        p[0] = p[1]
    else:
        errores_Sem_Desc.append("Error semántico en la linea "+str(p.lineno(1)-linea)+": La condicion del if no es valida")

def p_siError1(p):
    """
    si : IF PARENTESIS_A expresion  bloque_codigo
       | IF PARENTESIS_A expresion  bloque_codigo ELSE bloque_codigo
    """
    errores_Sinc_Desc.append("Error semántico en la linea "+str(p.lineno(1)-linea)+
                             "\nFalta cerrar el Parentesis (')')"+
                             "\nSe espera: IF PARENTESIS_A expresion PARENTESIS_B BloqueCodigo"
                             +"\n                                    ^^^^^^^^^^^^")

def p_siError2(p):
    """
    si : IF  expresion PARENTESIS_B bloque_codigo
       | IF  expresion PARENTESIS_B bloque_codigo ELSE bloque_codigo
    """
    errores_Sinc_Desc.append("Error semántico en la linea "+str(p.lineno(1)-linea)+
                             "\nFalta abrir el Parentesis ('(')"+
                             "\nSe espera: IF PARENTESIS_A expresion PARENTESIS_B BloqueCodigo"
                             +"\n             ^^^^^^^^^^^^")    

def p_siError3(p):
    """
    si : IF PARENTESIS_A  PARENTESIS_B bloque_codigo
       | IF PARENTESIS_A  PARENTESIS_B bloque_codigo ELSE bloque_codigo
    """
    errores_Sinc_Desc.append("Error semántico en la linea "+str(p.lineno(1)-linea)+
                             "\nCondicion IF requiere mas argumentos"+
                             "\nSe espera: IF PARENTESIS_A expresion PARENTESIS_B BloqueCodigo"
                             +"\n                          ^^^^^^^^^")    
def p_While(p):
    """
    mientras : WHILE PARENTESIS_A expresion PARENTESIS_B bloque_codigo
    """
    if(p[3] == True or p[3] == False):
        p[0] = p[1]
    else:
        errores_Sem_Desc.append("Error semántico en la linea "+str(p.lineno(1)-linea)+": La condicion del while no es valida")

def p_WhileError1(p):
    """
    mientras : WHILE PARENTESIS_A expresion bloque_codigo
    """
    errores_Sinc_Desc.append("Error Sintactico en la linea "+str(p.lineno(1)-linea)+
                            "\nFalta cerrar el Parentesis (')')"+
                            "\nSe espera: WHILE PARENTESIS_A expresion PARENTESIS_B BloqueCodigo"+
                            "\n                                        ^^^^^^^^^^^^")


def p_WhileError2(p):
    """
    mientras : WHILE expresion PARENTESIS_B bloque_codigo
    """
    errores_Sinc_Desc.append("Error Sintactico en la linea "+str(p.lineno(1)-linea)+
                            "\nFalta abrir el Parentesis ('(')"+
                            "\nSe espera: WHILE PARENTESIS_A expresion PARENTESIS_B BloqueCodigo"+
                            "\n                 ^^^^^^^^^^^^")
    
def p_WhileError3(p):
    """
    mientras : WHILE PARENTESIS_A PARENTESIS_B bloque_codigo
    """
    errores_Sinc_Desc.append("Error Sintactico en la linea "+str(p.lineno(1)-linea)+
                            "\nFaltan Argumentos"+
                            "\nSe espera: WHILE PARENTESIS_A expresion PARENTESIS_B BloqueCodigo"+
                            "\n                              ^^^^^^^^^")



#-----------------Import------------------------------
def p_import(p):
    '''graImport : IMPORT ID FROM CADENA PUNTOCOMA'''


#-----------------------------------------------------

#_--------------bucle for--------------------------------

def p_for_loop(p):
    """
    for_loop : FOR PARENTESIS_A for_init PUNTOCOMA for_condicion PUNTOCOMA for_actualizacion PARENTESIS_B bloque_codigo
    """
    p[0] = ('for_loop', {'init': p[3], 'condition': p[5], 'update': p[7], 'body': p[9]})

def p_for_init(p):
    """
    for_init : tipo ID ASIGNACION expresion
             | ID ASIGNACION expresion
    """
    if len(p) == 5:
        p[0] = ('init', {'type': p[1], 'id': p[2], 'value': p[4]})
    else:
        p[0] = ('init', {'id': p[1], 'value': p[3]})

def p_for_condicion(p):
    """
    for_condicion : expresion
    """
    p[0] = ('condition', p[1])

def p_for_actualizacion(p):
    """
    for_actualizacion : ID ASIGNACION expresion
                       | ID MASMAS
                       | ID MENOSMENOS
    """
    if len(p) == 4:
        p[0] = ('update', {'id': p[1], 'operation': p[2], 'value': p[3]})
    elif p[2] == 'i+':
        p[0] = ('increment', {'id': p[1]})
    elif p[2] == 'i-':
        p[0] = ('decrement', {'id': p[1]})



#----fin bucle for ------------------------------------
#-----------------Atributo de Objeto------------------------------
def p_AtrObjeto(p):
    '''atrObjeto : ID PUNTO ID
                 | ID CORCHETE_A NUMERO CORCHETE_B PUNTO ID'''

def p_declaracion_asignarAtrObjeto(p):
    '''declaracion : atrObjeto ASIGNACION expresion PUNTOCOMA
                    | atrObjeto ASIGNACION True PUNTOCOMA
                    | atrObjeto ASIGNACION False PUNTOCOMA'''

#-----------------Crear Funcion------------------------------
parametros = []
def p_param(p):
    """
    param : tipo ID COMA param
    """
    parametros.append([p[1], p[2]])
    p[0] = parametros

def p_param2(p):
    """
    param : tipo ID
    """
    parametros.append([p[1], p[2]])
    p[0] = parametros

def p_errorFaltanParametros(p):
    """
    param : ID
    """
    errores_Sinc_Desc.append("Error sintactico en la linea: "+str(p.lineno(1)-linea)+
                             "\nNo se definio el tipo de dato del parametro '"+p[1]+"'")


def p_funcion1(p):
    """
    funcion : FUN ID PARENTESIS_A PARENTESIS_B bloque_codigo
    """
    if(tabla_simbolos.insertar_funcion(p[2], [])):
        errores_Sem_Desc.append("Error semántico en la linea "+str(p.lineno(1)-linea)+": El nombre de la función "+p[2]+" ya ha sido declarado")
    p[0] = p[1]

def p_funcion(p):
    """
    funcion : FUN ID PARENTESIS_A param PARENTESIS_B bloque_codigo
    """
    global parametros
    if(tabla_simbolos.insertar_funcion(p[2], parametros)):
        errores_Sem_Desc.append("Error semántico en la linea "+str(p.lineno(1)-linea)+": El nombre de la función "+p[2]+" ya ha sido declarado")

    parametros = []

valores = []

def p_funcionError1(p):
    """
    funcion : ID PARENTESIS_A PARENTESIS_B bloque_codigo

    """
    errores_Sinc_Desc.append("Error sintactico en la linea: "+str(p.lineno(1)-linea)+
                             "\nPosible Funcion.  Se espera: FUN ID PARENTESIS_A PARENTESIS_B bloque_codigo"+
                             "\n                             ^^^"+
                             "\nIntente FUN "+p[1]+" "+p[2]+p[3]+"Su bloque de codigo")

def p_funcionError2(p):
    """
    funcion : ID PARENTESIS_A param PARENTESIS_B bloque_codigo

    """
    errores_Sinc_Desc.append("Error sintactico en la linea: "+str(p.lineno(1)-linea)+
                             "\nPosible Funcion.  Se espera: FUN ID PARENTESIS_A Parametros PARENTESIS_B bloque_codigo"+
                             "\n                             ^^^"+
                             "\nIntente FUN "+p[1]+" "+p[2]+"Sus parametros"+p[4]+"Su bloque de codigo")
    
def p_funcionError3(p):
    """
    funcion : FUN ID param PARENTESIS_B bloque_codigo

    """
    errores_Sinc_Desc.append("Error sintactico en la linea: "+str(p.lineno(1)-linea)+
                             "\nFalta Iniciar Paretensis ('(').  Se espera: FUN ID PARENTESIS_A Parametros PARENTESIS_B bloque_codigo"+
                             "\n                                                   ^^^^^^^^^^^^"+
                             "\nIntente "+p[1]+" "+p[2]+"(Sus parametros"+p[4]+"Su bloque de codigo")

    
def p_funcionError4(p):
    """
    funcion : FUN ID PARENTESIS_A param bloque_codigo

    """
    errores_Sinc_Desc.append("Error sintactico en la linea: "+str(p.lineno(1)-linea)+
                             "\nFalta Cerrar Paretensis (')').  Se espera: FUN ID PARENTESIS_A Parametros PARENTESIS_B bloque_codigo"+
                             "\n                                                                           ^^^^^^^^^^^^"+
                             "\nIntente "+p[1]+" "+p[2]+p[3]+"Sus parametros)"+" BloqueCodigo")
    
    
def p_funcionError5(p):
    """
    funcion : FUN ID PARENTESIS_A param PARENTESIS_B

    """
    errores_Sinc_Desc.append("Error sintactico en la linea: "+str(p.lineno(1)-linea)+
                             "\nNo se detecta el bloque de codigo de la funcion")
    
def p_funcionError6(p):
    """
    funcion : FUN ID PARENTESIS_B bloque_codigo

    """
    errores_Sinc_Desc.append("Error sintactico en la linea: "+str(p.lineno(1)-linea)+
                             "\nFalta iniciar Parentesis ('(')"
                             +"\nSe espera FUN ID PARENTESIS_A PARENTESIS_B BloqueCodigo"+
                             "\n                  ^^^^^^^^^^^^"+
                             "\nPruebe con: "+p[1]+" "+p[2]+"("+p[3]+" BloqueCodigo")
    
def p_funcionError7(p):
    """
    funcion : FUN ID PARENTESIS_A bloque_codigo

    """
    errores_Sinc_Desc.append("Error sintactico en la linea: "+str(p.lineno(1)-linea)+
                             "\nFalta cerrar Parentesis (')')"
                             +"\nSe espera FUN ID PARENTESIS_A PARENTESIS_B BloqueCodigo"+
                             "\n                               ^^^^^^^^^^^^"+
                             "\nPruebe con: "+p[1]+" "+p[2]+p[3]+") BloqueCodigo")
        
    
def p_valorparam(p):
    """
    valorparam : expresion COMA valorparam
               | expresion 
    """
    valores.append(p[1])

def p_llamadafunc(p):
    """
    llamadafunc : ID PARENTESIS_A valorparam PARENTESIS_B PUNTOCOMA
    """
    global valores
    funcion = tabla_simbolos.Buscar(p[1])
    if(funcion == None):
        errores_Sem_Desc.append("Error semántico en la linea "+str(p.lineno(1)-linea)+": La función "+p[1]+" no ha sido declarada")
    else:
        parame = funcion['parameters']
        i = 0
        for fila in parame:
            tipo = TipoValor(str(valores[i]))
            i+=1
            if(tipo != fila[0]):
                errores_Sem_Desc.append("Error semántico en la linea "+str(p.lineno(1)-linea)+": Se esperaba un valor de tipo "+fila[0]+" no uno de tipo "+tipo)

    valores = []

#-----------------Funciones------------------------------
def p_mover(p):
    """
    mover : moveTo PARENTESIS_A expresion PARENTESIS_B PUNTOCOMA
          | moveTo PARENTESIS_A atrObjeto PARENTESIS_B PUNTOCOMA
          | moveTo PARENTESIS_A elementoArr PARENTESIS_B PUNTOCOMA
    """
    p[0] = p[1]

def p_moverError1(p):
    """
    mover : moveTo PARENTESIS_A expresion PARENTESIS_B 
          | moveTo PARENTESIS_A atrObjeto PARENTESIS_B 
          | moveTo PARENTESIS_A elementoArr PARENTESIS_B
    """
    errores_Sinc_Desc.append("Error Sintactico en la linea "+str(p.lineno(1)-linea)+
                             "\nFalta punto y coma. Se espera: moveTo PARENTESIS_A expresion PARENTESIS_B PUNTOCOMA"+
                             "\n                                                                          ^^^^^^^^^")
                            
def p_moverError2(p):
    """
    mover : moveTo PARENTESIS_A expresion PUNTOCOMA 
          | moveTo PARENTESIS_A atrObjeto PUNTOCOMA
          | moveTo PARENTESIS_A elementoArr PUNTOCOMA
    """
    errores_Sinc_Desc.append("Error Sintactico en la linea "+str(p.lineno(1)-linea)+
                             "\nFalta cerrar Parentesis('('). Se espera: moveTo PARENTESIS_A expresion PARENTESIS_B PUNTOCOMA"+
                             "\n                                                                       ^^^^^^^^^")
    
def p_moverError3(p):
    """
    mover : moveTo  expresion PARENTESIS_B PUNTOCOMA 
          | moveTo atrObjeto PARENTESIS_B PUNTOCOMA
          | moveTo elementoArr PARENTESIS_B PUNTOCOMA
    """
    errores_Sinc_Desc.append("Error Sintactico en la linea "+str(p.lineno(1)-linea)+
                             "\nFalta abrir Parentesis('('). Se espera: moveTo PARENTESIS_A expresion PARENTESIS_B PUNTOCOMA"+
                             "\n                                               ^^^^^^^^^^^^")

def p_moverError4(p):
    """
    mover : moveTo PARENTESIS_A  PARENTESIS_B PUNTOCOMA 

    """
    errores_Sinc_Desc.append("Error Sintactico en la linea "+str(p.lineno(1)-linea)+
                             "\nFalta Se requieren Argumentos. Se espera: moveTo PARENTESIS_A expresion PARENTESIS_B PUNTOCOMA"+
                             "\n                                                               ^^^^^^^^")
            


def p_posicion(p):
    """
    posicion : glassPosition PARENTESIS_A expresion PARENTESIS_B
             | glassPosition PARENTESIS_A atrObjeto PARENTESIS_B
             | glassPosition PARENTESIS_A elementoArr PARENTESIS_B
    """
    p[0] = 'True'

def p_posicionError1(p):
    """
    posicion : glassPosition PARENTESIS_A expresion 
             | glassPosition PARENTESIS_A atrObjeto 
             | glassPosition PARENTESIS_A elementoArr 
    """
    errores_Sinc_Desc.append("Error Sintactico en la linea: "+str(p.lineno(1)-linea)+
                             "\nFalta cerrar el Parentesis (')')"+
                             "\nSe espera: glassPosition PARENTESIS_A expresion PARENTESIS_B"+
                             "\n                                                ^^^^^^^^^^^^")

def p_posicionError2(p):
    """
    posicion : glassPosition PARENTESIS_A PARENTESIS_B

    """
    errores_Sinc_Desc.append("Error Sintactico en la linea: "+str(p.lineno(1)-linea)+
                             "\nFaltan Argumentos"+
                             "\nSe espera: glassPosition PARENTESIS_A expresion PARENTESIS_B"+
                             "\n                                      ^^^^^^^^^")
def p_posicionError3(p):
    """
    posicion : glassPosition expresion PARENTESIS_B
             | glassPosition atrObjeto PARENTESIS_B
             | glassPosition elementoArr PARENTESIS_B

    """
    errores_Sinc_Desc.append("Error Sintactico en la linea: "+str(p.lineno(1)-linea)+
                             "\nFaltan abrir Parentesis ('(') "+
                             "\nSe espera: glassPosition PARENTESIS_A expresion PARENTESIS_B"+
                             "\n                         ^^^^^^^^^^^^")




def p_abrir(p):
    """
    abrir : gateOpen PARENTESIS_A expresion PARENTESIS_B PUNTOCOMA
          | gateOpen PARENTESIS_A atrObjeto PARENTESIS_B PUNTOCOMA
          | gateOpen PARENTESIS_A elementoArr PARENTESIS_B PUNTOCOMA
    """
    p[0] = p[1]

def p_abrirError1(p):
    """
    abrir : gateOpen PARENTESIS_A expresion PARENTESIS_B 
          | gateOpen PARENTESIS_A atrObjeto PARENTESIS_B 
          | gateOpen PARENTESIS_A elementoArr PARENTESIS_B
    """
    errores_Sinc_Desc.append("Error Sintactico en la linea: "+str(p.lineno(1)-linea)+
                             "\nFalta Punto Y Coma"+
                             "\nSe espera: gateOpen PARENTESIS_A expresion PARENTESIS_B PUNTOCOMA"+
                             "\n                                                        ^^^^^^^^^")

def p_abrirError2(p):
    """
    abrir : gateOpen PARENTESIS_A expresion PUNTOCOMA
          | gateOpen PARENTESIS_A atrObjeto PUNTOCOMA
          | gateOpen PARENTESIS_A elementoArr PUNTOCOMA
    """
    errores_Sinc_Desc.append("Error Sintactico en la linea: "+str(p.lineno(1)-linea)+
                             "\nFalta Cerrar Parentesis (')')"+
                             "\nSe espera: gateOpen PARENTESIS_A expresion PARENTESIS_B PUNTOCOMA"+
                             "\n                                           ^^^^^^^^^^^")
    

def p_abrirError3(p):
    """
    abrir : gateOpen expresion PARENTESIS_B PUNTOCOMA
          | gateOpen atrObjeto PARENTESIS_B  PUNTOCOMA
          | gateOpen elementoArr PARENTESIS_B  PUNTOCOMA
    """
    errores_Sinc_Desc.append("Error Sintactico en la linea: "+str(p.lineno(1)-linea)+
                             "\nFalta Abrir Parentesis ('(')"+
                             "\nSe espera: gateOpen PARENTESIS_A expresion PARENTESIS_B PUNTOCOMA"+
                             "\n                    ^^^^^^^^^^^")
    
def p_abrirError4(p):
    """
    abrir : gateOpen PARENTESIS_A  PARENTESIS_B  PUNTOCOMA
          
    """
    errores_Sinc_Desc.append("Error Sintactico en la linea: "+str(p.lineno(1)-linea)+
                             "\nFuncion gateOpen Requiere argumentos"+
                             "\nSe espera: gateOpen PARENTESIS_A expresion PARENTESIS_B PUNTOCOMA"+
                             "\n                                 ^^^^^^^^^")





#-----------------Declaracion de variables errores------------------------------
def p_declaracion_asignar_error1(t):
    '''declaracion : tipo ASIGNACION expresion PUNTOCOMA'''
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+": Falta nombre del identificador cerca de " +str("'")+ str(t[1])+str("'")+"\nSe espera: tipo ID Asignacion expresion PUNTOCOMA"+
                                                                                                      "\n                ^^"+
                                                                                                      "\nPruebe con: "+str(t[1])+" NombreEjemplo"+str(t[2])+str(t[3])+str(t[4]))
    
def p_declaracion_asignar_error2(t):
    '''declaracion : tipo ID expresion PUNTOCOMA'''
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+": Falta simbolo de asignación (=) cerca de '"+str(t[2])+"'"+
                                                                        "\nSe espera: tipo ID ASIGNACION expresion PUNTOCOMA"+
                                                                        "\n                   ^^^^^^^^^^"+
                                                                        "\nPruebe con: "+str(t[1])+" "+str(t[2])+"="+str(t[3])+str(t[4])+"\n")

def p_declaracion_asignar_error3(t):
    '''declaracion : tipo ID ASIGNACION PUNTOCOMA'''
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+": El valor asignado no es valido o faltante cerca de: "+str(t[3])+
                                                                                                         "\nSe espera: tipo ID Asignacion EXPRESION PUNTOCOMA"+
                                                                                                         "\n                              ^^^^^^^^^"+
                                                                                                         "\nPruebe con: "+str(t[1])+" "+str(t[2])+str(t[3]+"Expresion")+str(t[4])+"\n")
    
def p_declaracion_asignar_error4(t):
    '''declaracion : tipo ID ASIGNACION expresion'''
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+": Falta punto y coma cerca de "+str("'")+str(t[4])+str("'")+
                                                                                        "\nSe espera: tipo ID Asignacion expresion PUNTOCOMA"+
                                                                                        "\n                                        ^^^^^^^^^"+
                                                                                        "\nPruebe con: "+str(t[1])+" "+str(t[2])+" "+str(t[3])+" "+str(t[4])+" ;\n")

def p_declaracion_asignar_error6(t):
    '''declaracion : ID ID ASIGNACION expresion PUNTOCOMA'''
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+": No se reconoce tipo de dato: "+str(t[1])+
                                                                        "\nSe espera: tipo ID ASIGNACION expresion PUNTOCOMA"+
                                                                        "\n           ^^^^"+"\nPruebe con: "+"TipoDeDatoValido "+str(t[2])+str(t[3])+str(t[4])+str(t[5])+"\n")
    

#----------------------Error bloque de código-------------------------------------------   
def p_programaError1(t):
    """programa : bloque_codigo END"""
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+": Falta la palabra clave 'BEGIN'")
    
def p_programaError2(t):
    """programa : BEGIN bloque_codigo """
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(1)-linea)+": Falta la palabra clave 'END'")

def p_error(p):
    if p:
        errores_Sinc_Desc.append(f"Error de sintaxis en '{p.value}', línea {p.lineno - linea}")
        print(f"Error de sintaxis en '{p.value}', línea {p.lineno - linea}")
    else:
        print("Error de sintaxis: expresión incompleta")
    
 
 #--------------------Error bloque de codigo-----------------------------------------
def p_bloque_codigo_error1(t):
    """
    bloque_codigo : lista_declaraciones LLAVE_C
    """
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+": Falta la llave de apertura '{'")

def p_bloque_codigo_error2(t):
    """
    bloque_codigo : LLAVE_A lista_declaraciones
    """
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(1)-linea)+": Falta la llave de cierre '}'")  
    
#----------------------Error crear objeto-----------------------------
def p_declaracion_crearObjError1(t):
    '''declaracion : ASIGNACION CO ID PUNTOCOMA'''
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+": Falta el nombre del objeto")
    
def p_declaracion_crearObjError2(t):
    '''declaracion : ID CO ID PUNTOCOMA'''
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+": Falta simbolo de asignación (=)")

def p_declaracion_crearObjError3(t):
    '''declaracion : ID ASIGNACION ID PUNTOCOMA'''
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+": Falta la palabra reserva 'CO'")
    
def p_declaracion_crearObjError4(t):
    '''declaracion : ID ASIGNACION CO PUNTOCOMA'''
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+": Falta el nombre del objeto")

def p_declaracion_crearObjError5(t):
    '''declaracion : ID ASIGNACION CO ID'''
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+": Falta punto y coma")
    

#----------------------Error crear arreglo-----------------------------
def p_declaracion_crearArregloError1(t):
    '''declaracion : ASIGNACION CA CORCHETE_A NUMERO CORCHETE_B PUNTOCOMA'''
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+": Falta el nombre del arreglo")

def p_declaracion_crearArregloError2(t):
    '''declaracion : ID CA CORCHETE_A NUMERO CORCHETE_B PUNTOCOMA'''
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+": Falta simbolo de asignación (=)")
              
def p_declaracion_crearArregloError3(t):
    '''declaracion : ID ASIGNACION CORCHETE_A NUMERO CORCHETE_B PUNTOCOMA'''
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+"Falta la palabra reserva 'CA'")
    
def p_declaracion_crearArregloError4(t):
    '''declaracion : ID ASIGNACION CA NUMERO CORCHETE_B PUNTOCOMA'''
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+": Falta el corchete de apertura '['")

def p_declaracion_crearArregloError5(t):
    '''declaracion : ID ASIGNACION CA CORCHETE_A CORCHETE_B PUNTOCOMA'''
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+":Falta el número entre los corchetes")
    
def p_declaracion_crearArregloError6(t):
    '''declaracion : ID ASIGNACION CA CORCHETE_A NUMERO PUNTOCOMA'''
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+": Falta el corchete de cierre ']'")

def p_declaracion_crearArregloError7(t):
    '''declaracion : ID ASIGNACION CA CORCHETE_A NUMERO CORCHETE_B'''
    errores_Sinc_Desc.append("Error sintáctico en la linea "+str(t.lineno(2)-linea)+": Falta punto y coma")
    
# Construir el analizador
parser = yacc.yacc()

def test_parser(input_string, num):
    global linea
    linea = num
    result = parser.parse(input_string)
    print(result)
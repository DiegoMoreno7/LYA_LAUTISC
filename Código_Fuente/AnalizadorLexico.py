#analizador Lexico
import ply.lex as lex

lista_errores_lexicos = []
errores_Desc = []

def limpiar_errores_lex():
    global lista_errores_lexicos
    lista_errores_lexicos = []
    global errores_Desc
    errores_Desc = []

tokens = [
    'ID',
    'NUMERO',
    'REAL',
    'SUMA',
    'ASIGNACION',
    'RESTA',
    'DIVISION',
    'MULTIPLICACION',
    'IGUAL',
    'DIFERENTE',
    'MAYORQUE',
    'MENORQUE',
    'MENORIGUAL',
    'MAYORIGUAL',
    'PUNTO',
    'COMA',
    'DOSPUNTOS',
    'PUNTOCOMA',
    'COMILLASIMPLE',
    'COMILLADOBLE',
    'PARENTESIS_A',
    'PARENTESIS_B',
    'LLAVE_A',
    'LLAVE_C',
    'CORCHETE_A',
    'CORCHETE_B',
    'MASMAS',
    'MENOSMENOS',
    'AND',
    'OR',
    'NOT',
    'CADENA',
    'BEGIN',
    'END',
    'True',
    'False',
    'IMPORT',
    'FUN',
    'FROM',
    'WHILE',
    'FOR',
    'IF',
    'ELSE',
    'RETURN',
    'DESTROY', 
    'ONOFF',
    'SMS',
    'DSEN',
    'DLED',
    'GVS',
    'real',
    'int',
    'bool',
    'stg',
    'moveTo',
    'glassPosition',
    'gateOpen',
    'CO',
    'CA',
]

t_ignore = ' \t'

t_SUMA = r'\+'
t_ASIGNACION = r'='
t_RESTA = r'\-'
t_DIVISION = r'/'
t_MULTIPLICACION = r'\*'
t_IGUAL = r'=='
t_DIFERENTE = r'!='
t_MAYORQUE = r'>'
t_MENORQUE = r'<'
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_PUNTO = r'\.'
t_COMA = r'\,'
t_DOSPUNTOS = r'\:'
t_PUNTOCOMA = r'\;'
t_COMILLASIMPLE = r'\''
t_COMILLADOBLE = r'\"'
t_PARENTESIS_A = r'\('
t_PARENTESIS_B = r'\)'
t_LLAVE_A = r'\{'
t_LLAVE_C = r'\}'
t_CORCHETE_A = r'\['
t_CORCHETE_B = r'\]'
t_MASMAS = r'i\+'
t_MENOSMENOS = r'i\-'
t_AND = r'\&\&'
t_OR = r'\|{2}'
t_NOT = r'\!'

contador = 0

def t_SALTOLINEA(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_CADENA(t):
    r'\#.*?\#'
    t.type = 'CADENA'
    return t

# Token para IF
def t_SI(t):
    r'IF'
    t.type = 'IF'
    return t

# Identificadores no válidos
def t_IDError(t):
    r'\d+[a-zA-ZñÑ]+[a-zA-Z0-9ñÑ]*'
    global lista_errores_lexicos
    lista_errores_lexicos.append(t.lineno)
    global errores_Desc
    errores_Desc.append("Identificador no válido en la línea " + str(t.lineno))
    # t.lexer.skip(1)

# Expresión regular para identificadores (nombres de variables, funciones, etc.)
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value == 'BEGIN':
        t.type = 'BEGIN'
    elif t.value == 'END':
        t.type = 'END'
    elif t.value == 'FOR':
        t.type = 'FOR'
    elif t.value == 'WHILE':
        t.type = 'WHILE'
    elif t.value == 'ELSE':
        t.type = 'ELSE'
    elif t.value == 'int':
        t.type = 'int'
    elif t.value == 'real':
        t.type = 'real'
    elif t.value == 'bool':
        t.type = 'bool'
    elif t.value == 'stg':
        t.type = 'stg'    
    elif t.value == 'SMS':
        t.type = 'SMS'
    elif t.value == 'FUN':
        t.type = 'FUN'
    elif t.value == 'True':
        t.type = 'True'
    elif t.value == 'False':
        t.type = 'False'
    elif t.value == 'CO':
        t.type = 'CO'
    elif t.value == 'CA':
        t.type = 'CA'
    elif t.value == 'moveTo':
        t.type = 'moveTo'
    elif t.value == 'glassPosition':
        t.type = 'glassPosition'
    elif t.value == 'gateOpen':
        t.type = 'gateOpen'
    else:
        t.type = 'ID'
    return t

def t_COMENTARIO(t):
    r'\/\/(.*?)\/\/'
    pass

def t_REAL(t):
    r'(\d+\.\d+|\.\d+)'
    t.value = float(t.value)
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_TRUE(t):
    r'TRUE'
    t.type = 'TRUE'
    return t

def t_FALSE(t):
    r'FALSE'
    t.type = 'FALSE'
    return t

def t_error(t):
    global lista_errores_lexicos
    lista_errores_lexicos.append(t.lineno)
    global errores_Desc
    errores_Desc.append(f"Símbolo no válido '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def analisis(cadena):
    lexer.input(cadena)
    tokens = []
    # Inicia el número de línea en 1
    lexer.lineno = 1
    for tok in lexer:
        columna = tok.lexpos - cadena.rfind('\n', 0, tok.lexpos)
        tokens.append((tok.value, tok.type, tok.lineno, columna))
    return tokens
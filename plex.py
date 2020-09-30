import ply.lex as lex

tokens = [
    'SEMICOL',
    'CORKSCREW',
    'COMMA',
    'DOT',
    'R_PAREN',
    'L_PAREN',
    'LITERAL',
    'NUMBER',
    'ID'
]

t_SEMICOL = r';'
t_CORKSCREW = r':-'
t_COMMA = r','
t_DOT = r'\.'
t_L_PAREN = r'\('
t_R_PAREN = r'\)'
t_LITERAL = r'\".*\"'

t_ignore = ' \t'


def t_NUMBER(t):
    r'0|[1-9][0-9]*'
    return t


def t_ID(t):
    r'[a-zA-Z_]+'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    raise ValueError(f'Invalid character at position {t.lexpos}')


lexer = lex.lex()

def token_list_from_text(text):
    lexer.input(text)
    result = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        result.append(tok)
    return result

def token_list_from_file(inputfile):
    with open(inputfile, 'r') as file:
        return token_list_from_text(file.read())

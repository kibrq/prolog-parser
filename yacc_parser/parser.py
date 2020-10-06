import ply.yacc as yacc

from plex import tokens

import prolog_ast as ast


def p_prog(p):
    '''prog : definitions'''
    p[0] = ast.Prog(p[1])


def p_prog_empty(p):
    '''prog : '''
    p[0] = None


def p_definitions(p):
    '''definitions : definition definitions
                   | definition'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]


def p_definition(p):
    '''definition : head DOT
                  | head CORKSCREW body DOT'''
    if p[2] == '.':
        p[0] = ast.Relation(p[1], None)
    else:
        p[0] = ast.Relation(p[1], p[3])


def p_head(p):
    '''head : atom'''
    p[0] = p[1]


def p_atom(p):
    '''atom : atom_head
            | atom_head atom_args'''
    if len(p) == 2:
        p[0] = ast.Atom(p[1], [])
    else:
        p[0] = ast.Atom(p[1], p[2])


def p_atom_head(p):
    '''atom_head : ID'''
    p[0] = p[1]


def p_atom_args(p):
    '''atom_args : atom_arg atom_args
                | atom_arg'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]


def p_atom_arg(p):
    '''atom_arg : ID
               | L_PAREN subatom R_PAREN'''
    if len(p) == 2:
        p[0] = ast.Atom(p[1], [])
    else:
        p[0] = p[2]

def p_subatom(p):
    '''subatom : atom
               | L_PAREN subatom R_PAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_body(p):
    '''body : expression'''
    p[0] = p[1]


def parse_binop(p):
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ast.Binop(p[1], p[2], p[3])


def p_expression(p):
    '''expression : term SEMICOL expression
                  | term'''
    parse_binop(p)


def p_term(p):
    '''term : factor COMMA term
            | factor'''
    parse_binop(p)


def p_factor(p):
    '''factor : L_PAREN expression R_PAREN
              | atom'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]



def p_error(p):
    raise ValueError(p)


parser = yacc.yacc()


def parse(string):
    return parser.parse(string)

from parsec import *
from prolog_ast import *
import re


# ignore cases.
whitespace = regex(r'(\s)+', re.MULTILINE)
ignore = many(whitespace)

# lexer for words.


def lexeme(p): return ignore >> p << ignore  # skip all ignored characters.


# keywords
kw_module = lexeme(string('module'))
kw_type = lexeme(string('type'))

keywords = ['module', 'type']


def check_identificator(s):
    if s in keywords:
        raise ValueError('expected identificator')
    return s


lparen = lexeme(string('('))
rparen = lexeme(string(')'))
lbrak = lexeme(string('['))
rbrak = lexeme(string(']'))
vdash = lexeme(string('|'))
number = lexeme(regex(r'\d+')).parsecmap(int)
dot = lexeme(string('.'))
ident = lexeme(regex(r'[a-z][a-z0-9_A-Z]*')).parsecmap(check_identificator)
var = lexeme(regex(r'[A-Z][a-z0-9_A-Z]*')).parsecmap(Variable)
arrow = lexeme(string('->'))
corkscrew = lexeme(string(':-'))
comma = lexeme(string(','))
semicol = lexeme(string(';'))


def mySepBy(parser, delim, mint):
    assert mint in [0, 1]

    @generate
    def separser():
        if mint == 1:
            fst = yield parser
        else:
            fst = yield optional(parser)
        if mint == 0 and fst is None:
            return []
        snd = yield many(delim >> parser)
        return [fst] + snd
    return separser


@generate
def def_module():
    '''Module definition'''
    yield kw_module
    name = yield ident
    yield dot
    return name


@generate
def atom():
    name = yield atom_head
    body = yield atom_body
    return Atom(name, body)


CONS = 'cons'
NIL = 'nil'


@generate
def array():
    yield lbrak
    es = yield elems
    yield rbrak
    res = Atom(NIL, [])
    for e in reversed(es):
        res = Atom(CONS, [e, res])
    return res


subarray = atom | var | array
headNtail = (atom | var) + (vdash >> var)
elems = headNtail ^ (mySepBy(subarray, comma, 0))

atom_head = ident


@generate
def parenatom():
    patom = yield lparen >> parenatom << rparen | atom | var
    return patom


null_args_atom = ident.parsecmap(lambda x: Atom(x, []))

subatom = lparen >> parenatom << rparen | null_args_atom | var | array

atom_body = many(subatom)


@generate
def def_type():
    '''Type definition'''
    yield kw_type
    name = yield ident
    defin = yield subtype
    yield dot
    return TypeDecl(name, defin)


@generate
def subtype():
    types = yield mySepBy(type_part, arrow, 0)
    return createRightAssocExpr(types, Arrow)

type_part = (atom | var | lparen >> subtype << rparen)


@generate
def def_rel():
    '''Relation definition'''
    head = yield rel_head
    body = yield corkscrew >> expr << dot | dot.parsecmap(lambda x: None)
    return Relation(head, body)


rel_head = atom


@generate
def expr():
    '''Expression'''
    terms = yield mySepBy(term, semicol, 1)
    return createRightAssocExpr(terms, lambda x, y : Binop(x, y, ';'))


rel_body = expr


@generate
def term():
    '''Term'''
    factors = yield mySepBy(factor, comma, 1)
    return createRightAssocExpr(factors, lambda x, y : Binop(x, y, ','))


factor = (lparen >> expr << rparen) | atom


@generate
def prog():
    module = yield optional(def_module)
    types = yield many(def_type)
    relations = yield many(def_rel)
    yield eof()
    return Module(None if not module else module[0], types, relations)


program = ignore >> prog


def parse(s):
    try:
        return program.parse(s)
    except ParseError:
        return False
    except ValueError:
        return False

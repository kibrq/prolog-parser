from parsec import *
from prolog_ast import *
import functools as ft
import re


class ParserWrapper:
    def __init__(self, val):
        self.val = val

    def __iadd__(self, parser):
        if not self.val:
            self.val = parser
        else:
            self.val = val | parser


def createTree(ctor, argc, assoc):
    def createTree_(elems, init=None):
        if assoc == 0:
            if not init:
                init = elems.pop(0)
            if len(elems) == 0:
                return init
            args = elems[:argc - 1]
            init = ctor(init, *args)
            return createTree_(elems[argc - 1:], init)
        else:
            if len(elems) == 1:
                return elems[0]
            args = elems[:argc - 1]
            init = createTree_(elems[argc - 1:], init)
            return ctor(*args, init)
    return createTree_


@generate
def comment():
    yield lcomm >> inner_comment << rcomm


lcomm = string('(*')
rcomm = string('*)')


@Parser
def anybutcomm(text, index=0):
    vall, valr = lcomm(text, index), rcomm(text, index)
    if vall.status or valr.status:
        return Value.failure(index, 'not a comment')
    return Value.success(index + 1, text[index])


inner_comment = many(anybutcomm | comment)

# ignore cases.
whitespace = regex(r'(\s)+', re.MULTILINE)
ignore = many(whitespace | comment)

# lexer for words.


def lexeme(p): return ignore >> p << ignore  # skip all ignored characters.


operatorkw = lexeme(string('operator'))
modulekw = lexeme(string('module'))
typekw = lexeme(string('type'))


lparen = lexeme(string('('))
rparen = lexeme(string(')'))
lbrak = lexeme(string('['))
rbrak = lexeme(string(']'))
vdash = lexeme(string('|'))
number = lexeme(regex(r'\d+')).parsecmap(int)
dot = lexeme(string('.'))
ident = lexeme(regex(r'[a-z][a-z0-9_A-Z]*'))
var = lexeme(regex(r'[A-Z][a-z0-9_A-Z]*')).parsecmap(Variable)
arrow = lexeme(string('->'))
corkscrew = lexeme(string(':-'))
comma = lexeme(string(','))
semicol = lexeme(string(';'))

opsymbols = lexeme(regex(r'[\,\;\-\+\*\&\^\%\$\#\@\!\?\>\<]+'))
opprior = lexeme(regex(r'[0-9]+')).parsecmap(int)
opassoc = lexeme(regex(r'[LR]'))


def separateMutableBy(parser, wdelim, mint):
    assert mint in [0, 1]

    @generate
    def separser():
        delim = wdelim.val
        if mint == 1:
            fst = yield parser
        else:
            fst = yield optional(parser)
        if mint == 0 and fst is None:
            return []
        snd = yield many(delim >> parser)
        return [fst] + snd
    return separser


def separateBy(parser, delim, mint):
    return separateMutableBy(parser, ParserWrapper(delim), mint)


def separateMutableWith(parser, wdelim, mint):
    assert mint in [0, 1]

    def concat(x):
        res = []
        for el in x:
            res += list(el)
        return res

    @generate
    def separser():
        delim = wdelim.val
        if delim is None:
            alt = parser.parsecmap(lambda x: [x])
            return alt if mint == 1 else optional(alt, [])
        if mint == 1:
            fst = yield parser
        else:
            fst = yield optional(parser)
        if mint == 0 and fst is None:
            return []
        snd = yield many(delim + parser).parsecmap(concat)
        return [fst] + snd
    return separser


def separateWith(parser, delim, mint):
    return separateMutableWith(parser, ParserWrapper(delim), mint)


@generate
def def_module():
    '''Module definition'''
    name = yield modulekw >> ident << dot
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
    es = yield lbrak >> elems << rbrak
    return ft.reduce(lambda x, y: Atom(CONS, [y, x]), reversed(es), Atom(NIL, []))


subarray = atom | var | array
headNtail = (atom | var) + (vdash >> var)
elems = headNtail ^ (separateBy(subarray, comma, 0))

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
    yield typekw
    name = yield ident
    defin = yield subtype
    yield dot
    return TypeDecl(name, defin)


@generate
def subtype():
    types = yield separateBy(type_part, arrow, 0).parsecmap(createTree(Arrow, 2, 1))
    return types


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
    res = yield termsholder.exec()
    return res


class OperatorsHolder:
    def __init__(self, max_prior):
        self.max_prior = max_prior
        self.registered = set()
        self.operators = [ParserWrapper(None) for _ in range(2 * max_prior)]

    def register(self, name, prior, assoc):
        if name in self.registered:
            raise ValueError('operator already in use')
        if prior >= self.max_prior:
            raise ValueError('too big operator priority')

        self.registered.add(name)
        self.operators[2 * prior + assoc] += lexeme(string(name))


class TermsHolder:
    def __init__(self, operators):
        self.terms = [None for _ in range(len(operators))]
        self.terms.append(lparen >> expr << rparen | atom | var)
        for i in reversed(range(len(operators))):
            self.terms[i] = separateMutableWith(
                self.terms[i + 1], operators[i], 1).parsecmap(createTree(Binop, 3, i & 1))

    def exec(self):
        return self.terms[0]


opsholder = OperatorsHolder(10)
termsholder = TermsHolder(opsholder.operators)
opsholder.register(',', 5, 1)
opsholder.register(';', 4, 1)


@generate
def def_op():
    ((name, prior), assoc) = yield (operatorkw >> opsymbols) + opprior + opassoc
    body = yield corkscrew >> expr << dot | dot.parsecmap(lambda x: None)
    opsholder.register(name, prior, 0 if assoc == 'L' else 1)
    return Relation(f'{name} with priority={prior} associative={assoc}', body)


@generate
def program():
    prog = many(def_op ^ def_type ^ def_rel)
    res = yield def_module + prog ^ prog
    name, data = '', None
    if isinstance(res, tuple):
        name, data = res
    else:
        data = res
    return Module(name, data)


def parse(s):
    return program.parse(s)

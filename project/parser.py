from parsec import *
from prolog_ast import *
import re


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
opprior = lexeme(regex(r'[0-9]')).parsecmap(int)
opassoc = lexeme(regex(r'[LR]'))

operatorkw = lexeme(string('operator'))
modulekw = lexeme(string('module'))
typekw = lexeme(string('type'))

# comments


def separateBy(parser, delim, mint):
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


def separateWith(parser, delim, mint):
    assert mint in [0, 1]

    def concat(x):
        res = []
        for el in x:
            res += list(el)
        return res

    @generate
    def separser():
        if mint == 1:
            fst = yield parser
        else:
            fst = yield optional(parser)
        if mint == 0 and fst is None:
            return []
        snd = yield many(delim + parser).parsecmap(concat)
        return [fst] + snd
    return separser if delim is not None else parser.parsecmap(lambda x: [x])


class ExpressionParser:
    MAX_PRIOR = 10
    ASSOC_LEFT, ASSOC_RIGHT = 0, 1

    registered = set()
    opcombs = [None for i in range(2 * MAX_PRIOR)]
    termcombs = [None for i in range(2 * MAX_PRIOR + 1)]

    @generate
    def operator():
        ((name, prior), assoc) = yield operatorkw >> (opsymbols + opprior + optional(opassoc, 'R')) << dot
        assoc = ExpressionParser.ASSOC_LEFT if assoc == 'L' else ExpressionParser.ASSOC_RIGHT
        ExpressionParser.register(name, prior, assoc)
        return None

    @generate
    def expr():
        res = yield ExpressionParser.termcombs[0]
        return res

    @classmethod
    def register(cls, name,  prior, assoc):
        assert prior < cls.MAX_PRIOR
        assert assoc in [cls.ASSOC_LEFT, cls.ASSOC_RIGHT]

        if name in cls.registered:
            raise ValueError('Such operator already in use.')

        cls.registered.add(name)
        parser = lexeme(string(name))
        prior = 2 * prior + assoc
        if cls.opcombs[prior] is None:
            cls.opcombs[prior] = parser
        else:
            cls.opcombs[prior] |= parser
        cls.update_termcombs()

    @classmethod
    def register_builtin(cls):
        cls.register(',', 5, cls.ASSOC_RIGHT)
        cls.register(';', 3, cls.ASSOC_RIGHT)

    def __build_ast__(exprs, ctor):
        init, op = exprs[0], None
        for i, exp in enumerate(exprs[1:]):
            if i & 1:
                init = ctor(init, exp, op)
            else:
                op = exp
        return init

    @classmethod
    def build_expast(cls, assoc):
        def helper(exprs):
            assert len(exprs) > 0
            def ctor(a, b, o): return Binop(a, o, b)
            if assoc is cls.ASSOC_RIGHT:
                exprs = reversed(exprs)
                def ctor(a, b, o): return Binop(b, o, a)
            return cls.__build_ast__(list(exprs), ctor)
        return helper

    @classmethod
    def create_termcombs(cls):
        cls.termcombs[-1] = lparen >> cls.expr << rparen | ident.parsecmap(
            Variable)

    @classmethod
    def update_termcombs(cls):
        for i in reversed(range(2 * cls.MAX_PRIOR)):
            cls.termcombs[i] = separateWith(
                cls.termcombs[i + 1], cls.opcombs[i], 1).parsecmap(cls.build_expast(i & 1))


program = ignore >> optional(ExpressionParser.operator |
                             ExpressionParser.expr) << ignore << eof()


def parse(s):
    return program.parse(s)

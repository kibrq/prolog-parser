''' RULES

S -> DEFINITIONS
DEFINITIONS -> DEFINITION DEFINITIONS | EPS
DEFINITION -> HEAD :- BODY.
HEAD -> ID
BODY -> EXP
EXP -> P,EXP | P;EXP | P
P -> ID, (EXP)

'''


class Parser:

    DEFINITIONS = 'parse_definitions'
    DEFINITION = 'parse_definition'
    HEAD = 'parse_head'
    BODY = 'parse_body'
    EXP, EXP1, EXP2, EXP3 = 'parse_exp', 'parse_exp1', 'parse_exp2', 'parse_exp3'
    P, P1, P2 = 'parse_paren', 'parse_paren1', 'parse_paren2'
    '''
    '''
    CORKSCREW = 'CORKSCREW'
    ID, DOT = 'ID', 'DOT'
    SEMICOL = 'SEMICOL'
    COMMA = 'COMMA'
    L_PAREN, R_PAREN = 'L_PAREN', 'R_PAREN'

    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def execute(self):
        return self.parse_nonterminal(self.DEFINITIONS)

    def current_token(self):
        if self.index == len(self.tokens):
            return ''
        return self.tokens[self.index].type

    def next(self):
        self.index += 1

    def is_eof(self):
        return self.index == len(self.tokens)

    def parse_terminal(self, terminal):
        if self.current_token() == terminal:
            self.next()
            return True
        return False

    def parse_nonterminal(self, method):
        current_index = self.index
        if not getattr(self, method)():
            self.index = current_index
            return False
        return True

    def parse_alt(self, methods):
        for m in methods:
            if self.parse_nonterminal(m):
                return True
        return False

    def parse_definitions(self):
        if self.is_eof():
            return True
        if not self.parse_nonterminal(self.DEFINITION):
            return False
        return self.parse_nonterminal(self.DEFINITIONS)

    def parse_definition(self):
        if not self.parse_nonterminal(self.HEAD):
            return False
        if not self.parse_terminal(self.CORKSCREW):
            return False
        if not self.parse_nonterminal(self.BODY):
            return False
        return self.parse_terminal(self.DOT)

    def parse_head(self):
        return self.parse_terminal(self.ID)

    def parse_body(self):
        return self.parse_nonterminal(self.EXP)

    def parse_exp(self):
        return self.parse_alt([self.EXP1, self.EXP2, self.EXP3])

    def parse_exp1(self):
        if not self.parse_nonterminal(self.P):
            return False
        if not self.parse_terminal(self.COMMA):
            return False
        return self.parse_nonterminal(self.EXP)

    def parse_exp2(self):
        if not self.parse_nonterminal(self.P):
            return False
        if not self.parse_terminal(self.SEMICOL):
            return False
        return self.parse_nonterminal(self.EXP)

    def parse_exp3(self):
        return self.parse_nonterminal(self.P)

    def parse_paren(self):
        return self.parse_alt([self.P1, self.P2])

    def parse_paren1(self):
        return self.parse_terminal(self.ID)

    def parse_paren2(self):
        if not self.parse_terminal(self.L_PAREN):
            return False
        if not self.parse_nonterminal(self.EXP):
            return False
        return self.parse_terminal(self.R_PAREN)
def parse(tokens):
    return Parser(tokens).execute()

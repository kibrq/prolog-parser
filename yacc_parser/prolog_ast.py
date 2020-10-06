class BGColors:
    TYPE = '\033[95m'
    NAME = '\033[94m'
    OP = '\033[93m'
    ENDC = '\033[0m'


class Node:
    def __init__(self, children):
        self.children = children

    def __eq__(self, other):
        if other is None:
            return False
        if not len(self.children) == len(other.children):
            return False
        res = True
        for i, child in enumerate(self.children):
            res = res and child.__eq__(other.children[i])
        return res


class Prog(Node):
    def __init__(self, relations):
        Node.__init__(self, relations)

    def pretty_info(self):
        return f'{BGColors.TYPE}Program{BGColors.ENDC}'

    def __str__(self):
        string = ''
        for rel in self.children:
            string += rel.__str__() + '\n'
        return string


class Relation(Node):
    def __init__(self, head, body):
        Node.__init__(self, [head, body])

    def pretty_info(self):
        return f'{BGColors.TYPE}Relation{BGColors.ENDC}'

    def __str__(self):
        return f'REL ({self.children[0].__str__()}) :- ({self.children[1].__str__()})'


class Atom(Node):
    def __init__(self, name, children):
        self.name = name
        Node.__init__(self, children)

    def pretty_info(self):
        return f'{BGColors.TYPE}Atom{BGColors.ENDC} named {BGColors.NAME}{self.name}{BGColors.ENDC}'

    def __str__(self):
        string = f'ATOM {self.name}'
        for child in self.children:
            string += f' ({child.__str__()})'
        return string

    def __eq__(self, other):
        res = Node.__eq__(self, other)
        return res and self.name == other.name


class Binop(Node):
    def __init__(self, lhs, op, rhs):
        self.op = op
        Node.__init__(self, [lhs, rhs])

    def __op_as_string__(self):
        return 'Conj' if self.op == ',' else 'Disconj'

    def pretty_info(self):
       return f'{BGColors.TYPE}Binop {BGColors.OP}{self.__op_as_string__()}{BGColors.ENDC}'

    def __str__(self):
        op = self.__op_as_string__()
        return f'BINOP_{op} ({self.children[0].__str__()}) ({self.children[1].__str__()})'

    def __eq__(self, other):
        res = Node.__eq__(self, other)
        return res and self.op == other.op


class ASTPrinter:
    def __init__(self, indent=1):
       self.current_indent = 0
       self.dindent = indent

    def __print_indent__(self):
        print(' '*self.current_indent, end='')

    def __print_node__(self, node):
        if node is None:
            return
        self.__print_indent__()
        end = ':\n' if len(node.children) > 0 else '\n'
        print(node.pretty_info(), end=end)
        for ch in node.children:
            self.current_indent += self.dindent
            self.__print_node__(ch)
            self.current_indent -= self.dindent

    def execute(self, program):
        self.__print_node__(program)

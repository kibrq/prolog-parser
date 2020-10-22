class Module:
    def __init__(self, name, prog):
        self.name = name
        self.prog = prog

    def __eq__(self, other):
        if not isinstance(other, Module):
            return False
        return self.name == other.name and self.prog == other.prog

class TypeDecl:
    def __init__(self, name, typeexpr):
        self.name = name
        self.typeexpr = typeexpr

    def __eq__(self, other):
        if not isinstance(other, TypeDecl):
            return False
        return self.name == other.name and self.typeexpr == other.typeexpr


class Arrow:
    def __init__(self, lhs, rhs):
        self.lhs, self.rhs = lhs, rhs

    def __eq__(self, other):
        if not isinstance(other, Arrow):
            return False
        return self.lhs == other.lhs and self.rhs == other.rhs


class Relation:
    def __init__(self, head, body):
        self.head, self.body = head, body

    def __eq__(self, other):
        if not isinstance(other, Relation):
            return False
        return self.head == other.head and self.body == other.body


class List:
    def __init__(self,  elements):
        self.elements = elements

    def __eq__(self, other):
        if not isinstance(other, List):
            return False
        return self.elements == other.elements


class Atom:
    def __init__(self, name, children):
        self.name = name
        self.children = children

    def __eq__(self, other):
        if not isinstance(other, Atom):
            return False
        return self.name == other.name and self.children == other.children


class Variable:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        return self.name == other.name


class Binop:
    def __init__(self, lhs, op, rhs):
        self.op = op
        self.lhs, self.rhs = lhs, rhs

    def __op_as_string__(self):
        return 'Conj' if self.op == ',' else 'Disconj'

    def __eq__(self, other):
        if not isinstance(other, Binop):
            return False
        return self.op == other.op and self.lhs == other.lhs and self.rhs == other.rhs


class ASTPrinter:
    def __init__(self, printer=print, dindent=4):
        self.indent = 0
        self.printer = printer
        self.dindent = dindent

    def execute(self, module):
        self.traverse(module)

    def visit_node(self, node, visiter):
        self.indent += self.dindent
        visiter(node)
        self.indent -= self.dindent

    def __print__(self, s):
        self.printer(' '*self.indent + s)
        if not self.printer == print:
            self.printer('\n')

    def visit_module(self, module):
        self.__print__(f'Module {module.name}')
        self.traverse_list(module.prog)

    def visit_type_decl(self, type_decl):
        self.__print__('')
        self.__print__(f'TypeDecl {type_decl.name}')
        self.traverse(type_decl.typeexpr)

    def visit_arrow(self, arrow):
        self.__print__('Arrow:')
        self.traverse(arrow.lhs)
        self.traverse(arrow.rhs)

    def visit_relation(self, relation):
        self.__print__('')
        self.__print__('Relation:')
        self.__print__('Head:')
        self.traverse(relation.head)
        self.__print__('Body:')
        self.traverse(relation.body)

    def visit_atom(self, atom):
        self.__print__(f'Atom {atom.name}')
        if not atom.children == []:
            self.__print__('Arguments:')
            self.traverse_list(atom.children)

    def visit_binop(self, binop):
        self.__print__(f'Binop {binop.op}')
        self.__print__('LHS:')
        self.traverse(binop.lhs)
        self.__print__('RHS:')
        self.traverse(binop.rhs)

    def visit_variable(self, var):
        self.__print__(f'Variable {var.name}')

    def visit_list(self, array):
        self.__print__('List:')
        self.traverse_list(array.elements)

    def visit_literal(self, string):
        self.__print__(string)

    def traverse(self, node):
        if isinstance(node, Module):
            self.visit_module(node)
        elif isinstance(node, TypeDecl):
            self.visit_node(node, self.visit_type_decl)
        elif isinstance(node, Arrow):
            self.visit_node(node, self.visit_arrow)
        elif isinstance(node, Relation):
            self.visit_node(node, self.visit_relation)
        elif isinstance(node, Atom):
            self.visit_node(node, self.visit_atom)
        elif isinstance(node, Binop):
            self.visit_node(node, self.visit_binop)
        elif isinstance(node, Variable):
            self.visit_node(node, self.visit_variable)
        elif isinstance(node, List):
            self.visit_node(node, self.visit_list)
        elif isinstance(node, str):
            self.visit_node(node, self.visit_literal)
        elif node is None:
            return
        else:
            assert False

    def traverse_list(self, nodes):
        if nodes is None:
            return
        for node in nodes:
            self.traverse(node)

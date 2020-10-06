#!/usr/bin/env python3

import parser as ps
import prolog_ast as ast


def helper(arg, exception_type=ValueError, result=None, have_to_except=False):
    try:
        res = ps.parse(arg)
        assert not have_to_except and res == result
    except exception_type:
        assert have_to_except


def test_accept():
    text = 'f.'
    helper(text, result=ast.Prog([ast.Relation(ast.Atom('f', []), None)]))

    text = 'f :- g.'
    helper(text, result=ast.Prog(
        [ast.Relation(ast.Atom('f', []), ast.Atom('g', []))]))

    text = 'a (b c d).'
    result = ast.Prog(
        [ast.Relation(
            ast.Atom('a',
                     [ast.Atom('b',
                               [ast.Atom('c', []),
                                ast.Atom('d', [])]
                               )]),
            None)])
    helper(text, result=result)

    text = 'f :- a , b.'
    result = ast.Prog(
        [ast.Relation(
            ast.Atom('f', []), ast.Binop(ast.Atom('a', []), ',', ast.Atom('b', [])))])
    helper(text, result=result)

    text = 'f :- a,b;c.'
    result = ast.Prog([ast.Relation(
        ast.Atom('f', []), ast.Binop(ast.Binop(ast.Atom('a', []), ',', ast.Atom('b', [])),
                                     ';', ast.Atom('c', [])))])
    helper(text, result=result)
    text = 'f :- a,(b;c).'
    result = ast.Prog([ast.Relation(
        ast.Atom('f', []), ast.Binop(ast.Atom('a', []), ',', ast.Binop(ast.Atom('b', []),
                                                                       ';', ast.Atom('c', []))))])
    helper(text, result=result)
    text = 'f :- a b, c,d.'
    result = ast.Prog([ast.Relation(
        ast.Atom('f', []), ast.Binop(ast.Atom('a', [ast.Atom('b', [])]), ',',
                                     ast.Binop(ast.Atom('c', []), ',', ast.Atom('d', []))))])
    helper(text, result=result)
    text = 'f (c a) :- a, b.\nf :- (g).'
    result = ast.Prog(
        [ast.Relation(
            ast.Atom('f', [
                ast.Atom('c', [ast.Atom('a', [])])]),
            ast.Binop(ast.Atom('a',[]),',',ast.Atom('b',[]))),
         ast.Relation(
             ast.Atom('f', []),
             ast.Atom('g', []))
         ])
    helper(text, result=result)

def test_reject():
    text = ':-.'
    helper(text, have_to_except=True)
    text = 'f'
    helper(text, have_to_except=True)
    text = '(a) :-a.'
    helper(text, have_to_except=True)
    text = 'a:-.'
    helper(text, have_to_except=True)
    text = 'f:-g;h,.'
    helper(text, have_to_except=True)
    text = 'f:-(g;(f).'
    helper(text, have_to_except=True)
    text = 'f ():-.'
    helper(text, have_to_except=True)

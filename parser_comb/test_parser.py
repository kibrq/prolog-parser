#!/usr/bin/env python3

import parser as ps
import prolog_ast as ast


def test_accept():
    text = 'module m. f.'
    assert ps.parse(text) == ast.Module('m', [], [ast.Relation(ast.Atom('f', []), None)])

    text = 'module m. \n\n f :- g.'
    assert ps.parse(text) == ast.Module('m', [], [
        ast.Relation(ast.Atom('f', []), ast.Atom('g', []))])

    text = 'module m. a (b c d).'
    result = ast.Module('m', [],
        [ast.Relation(
            ast.Atom('a',
                     [ast.Atom('b',
                               [ast.Atom('c', []),
                                ast.Atom('d', [])]
                               )]),
            None)])
    assert ps.parse(text) == result

    text = 'module m. f :- a , b.'
    result = ast.Module('m', [],
        [ast.Relation(
            ast.Atom('f', []), ast.Binop(ast.Atom('a', []), ',', ast.Atom('b', [])))])
    assert ps.parse(text) == result

    text = 'module m. f :- a,b;c.'
    result = ast.Module('m', [], [ast.Relation(
        ast.Atom('f', []), ast.Binop(ast.Binop(ast.Atom('a', []), ',', ast.Atom('b', [])),
                                     ';', ast.Atom('c', [])))])
    assert ps.parse(text) == result

    text = 'module m.f :- a,(b;c).'
    result = ast.Module('m', [], [ast.Relation(
        ast.Atom('f', []), ast.Binop(ast.Atom('a', []), ',', ast.Binop(ast.Atom('b', []),
                                                                       ';', ast.Atom('c', []))))])
    assert ps.parse(text) == result

    text = 'module m. type a.'
    result = ast.Module('m', [ast.TypeDecl('a', [])], [])
    assert ps.parse(text) == result

    text = 'module m. type a a->b.'
    result = ast.Module('m', [ast.TypeDecl(
                            'a',
                            [
                            ast.Type([ast.Atom('a', [])]),
                            ast.Type([ast.Atom('b', [])])
                            ]
                        )], [])
    assert ps.parse(text) == result

def test_reject():
    text = 'module m. :-.'
    assert not ps.parse(text)
    text = 'f'
    assert not ps.parse(text)
    text = 'module m.(a) :-a.'
    assert not ps.parse(text)
    text = 'module m.a:-.'
    assert not ps.parse(text)
    text = 'f:-g;h,.'
    assert not ps.parse(text)
    text = 'f:-(g;(f).'
    assert not ps.parse(text)
    text = 'f ():-.'
    assert not ps.parse(text)

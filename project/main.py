#!/usr/bin/env python3

import argparse as ap

import sys

from parser import parse, ExpressionParser

from prolog_ast import ASTPrinter


def init_argparse():
    parser = ap.ArgumentParser()
    parser.add_argument('--pretty', dest='pretty',
                        action='store_true', help='prints pretty')
    parser.add_argument('inputfile', type=str, help='source file')
    parser.add_argument('outputfile', type=str, nargs='?', help='output file')
    return parser


def main(argv):
    ExpressionParser.create_termcombs()
    ExpressionParser.register_builtin()
    while True:
        try:
            inp = input()
            if (inp == 'exit'):
                exit()
            res = parse(inp)
            ASTPrinter(print).execute(res)
        except:
            print('Syntax error')


if __name__ == '__main__':
    main(sys.argv[1:])

#!/usr/bin/env python3

import argparse as ap

import sys

from parser import *

from prolog_ast import ASTPrinter


def init_argparse():
    parser = ap.ArgumentParser()
    parser.add_argument('--pretty', dest='pretty',
                        action='store_true', help='prints pretty')
    parser.add_argument('--atom', dest='atom', action='store_true')
    parser.add_argument('--typeexpr', dest='typeexpr', action='store_true')
    parser.add_argument('--type', dest='type', action='store_true')
    parser.add_argument('--module', dest='module', action='store_true')
    parser.add_argument('--relation', dest='relation', action='store_true')
    parser.add_argument('--list', dest='list', action='store_true')
    parser.add_argument('--prog', dest='prog', action='store_true')

    parser.add_argument('inputfile', type=str, help='source file')
    parser.add_argument('outputfile', type=str, nargs='?', help='output file')
    return parser


def main(argv):
    args = init_argparse().parse_args(argv)
    try:
        lines = []
        with open(args.inputfile, 'r') as file:
            lines = file.read()
        func = None
        if args.atom:
            func = atom
        elif args.typeexpr:
            func = subtype
        elif args.type:
            func = def_type
        elif args.module:
            func = def_module
        elif args.relation:
            func = def_rel
        elif args.list:
            func = array
        else:
            func = prog
        res = (func << eof()).parse(lines)

        if args.outputfile is None:
            args.outputfile = args.inputfile + '.out'

        file = open(args.outputfile, 'w')

        printer = print if args.pretty else file.write

        ASTPrinter(printer).execute(res)

        if not file is None:
            file.close()

    except ParseError:
        print('Syntax Error')

    except FileNotFoundError:
        print('There is no such file to open')


if __name__ == '__main__':
    main(sys.argv[1:])

#!/usr/bin/env python3

import argparse as ap

import sys

from parser import parse

from prolog_ast import ASTPrinter


def init_argparse():
    parser = ap.ArgumentParser()
    parser.add_argument('--pretty', dest='pretty',
                        action='store_true', help='prints pretty')
    parser.add_argument('inputfile', type=str, help='source file')
    parser.add_argument('outputfile', type=str, nargs='?', help='output file')
    return parser


def main(argv):
    args = init_argparse().parse_args(argv)
    try:
        lines = []
        with open(args.inputfile, 'r') as file:
            lines = file.read()
        res = parse(lines)

        if res is None:
            print('Syntax error')
            return

        if args.outputfile is None:
              args.outputfile = args.inputfile + '.out'

        file = open(args.outputfile, 'w')

        printer = print if args.pretty else file.write

        ASTPrinter(printer).execute(res)

        if not file is None:
            file.close()

    except FileNotFoundError:
        print('There is no such file to open')


if __name__ == '__main__':
    main(sys.argv[1:])

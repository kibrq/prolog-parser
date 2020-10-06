#!/usr/bin/env python3

import sys
import plex
import parser as ps
import argparse as ap

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
    lines = []
    try:
        with open(args.inputfile, 'r') as file:
            lines = file.read()
        res = ps.parse(lines)
        if args.pretty:
            ASTPrinter(4).execute(res)
        else:
            if args.outputfile is None:
                args.outputfile = args.inputfile + '.out'
            with open(args.outputfile, 'w') as file:
                file.write(res.__str__())
    except ValueError as ve:
        print('Syntax error')
    except FileNotFoundError:
        print('There is no such file to open')


if __name__ == '__main__':
    main(sys.argv[1:])

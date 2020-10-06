#!/usr/bin/env python3

import plex
import parser as ps
import sys


def main(argv):
    try:
        tokens = plex.token_list_from_file(argv[0])
        res = ps.parse(tokens)
        print(res)
    except FileNotFoundError:
        print('There is no such file')
    except ValueError as ve:
        print(ve)

if __name__ == '__main__':
    main(sys.argv[1:])

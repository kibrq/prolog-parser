#!/usr/bin/env python3

import plex
import parser as ps
import sys


def main(argv):
    try:
        tokens = plex.token_list_from_file(argv[0])
    except ValueError as ve:
        print(ve)
        return
    res = ps.parse(tokens)
    print(res)


if __name__ == '__main__':
    main(sys.argv[1:])

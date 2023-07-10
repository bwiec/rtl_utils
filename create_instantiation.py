#!/usr/bin/env python3

import sys
import argparse
from module_parser import module_parser

# Entry point of this file
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=sys.argv[0], description='Create instantiation template from module/entity definition')
    parser.add_argument('--debug', action='store_true', help='Print script debug messages')
    parser.add_argument('--inc_sig_property_comments', action='store_true', help='Adds comments about port type and dimensionality to each signal instantiation')
    parser.add_argument('filename',nargs='+')
    Args = sys.argv
    Args.pop(0)
    args = parser.parse_args(Args)

    for filename in args.filename:
        parser = module_parser(filename)
        if args.debug:
            print(parser.get_module_properties())
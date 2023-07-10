#!/usr/bin/env python3

import sys
import argparse
from module_parser import module_parser

def _print_instantiation(properties, prefix):
    print(prefix + properties["module_name"][0] + " ", end="")
    if len(properties["parameters"]) > 0:
        print("")
        print(prefix + "#(")
        _print_properties(properties["parameters"], prefix)
        print(prefix + ")")
    print(prefix + properties["module_name"][0] + "_inst")
    print(prefix + "(")
    _print_signals(properties["ordered_signals"], prefix)
    print(prefix + ");")

def _print_properties(parameters, prefix):
    loop_idx = 0
    for ii in parameters:
        if loop_idx % 3 == 0:
            if loop_idx == (len(parameters)-2)-1:
                this_line = "\t." + ii + "(" + ii + ")"
            else:
                this_line = "\t." + ii + "(" + ii + "),"
            print(prefix + this_line)
        loop_idx += 1

def _print_signals(signals, prefix):
    loop_idx = 0
    for ii in signals:
        if loop_idx % 2 == 0:
            if loop_idx == (len(signals)-1)-1:
                this_line = "\t." + ii + "(" + ii + ")"
            else:
                this_line = "\t." + ii + "(" + ii + "),"
            print(prefix + this_line)
        loop_idx += 1

# Entry point of this file
if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(prog=sys.argv[0], description='Create instantiation template from module/entity definition')
    arg_parser.add_argument('--debug', action='store_true', help='Print script debug messages')
    arg_parser.add_argument('--inc_sig_property_comments', action='store_true', help='Adds comments about port type and dimensionality to each signal instantiation')
    arg_parser.add_argument('filename',nargs='+')
    Args = sys.argv
    Args.pop(0)
    args = arg_parser.parse_args(Args)

    for filename in args.filename:
        mod_parser = module_parser(filename)
        properties = mod_parser.get_module_properties()
        if args.debug:
            print(properties)
        
        _print_instantiation(properties, "")
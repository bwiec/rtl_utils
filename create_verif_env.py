#!/usr/bin/env python3

import sys
import os
import pathlib
import argparse
import shutil

def _create_verif_env(script_dir, dirname):
    dst = os.path.join(dirname, 'example_verif_env')
    shutil.copytree(script_dir + '/template/verif_env', dst)

# Entry point of this file
if __name__ == "__main__":
    
    script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    arg_parser = argparse.ArgumentParser(prog=sys.argv[0], description='Create verification environment')
    arg_parser.add_argument('--debug', action='store_true', help='Print script debug messages')
    arg_parser.add_argument('dirname',nargs='+')
    Args = sys.argv
    Args.pop(0)
    args = arg_parser.parse_args(Args)

    for dirname in args.dirname:
        if args.debug:
            print('Nothing to do for debug for now')
        
        _create_verif_env(script_dir, dirname)

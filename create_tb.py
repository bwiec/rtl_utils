#!/usr/bin/env python3

import sys
import argparse
from module_parser import module_parser
import create_instantiation

def _print_tb(properties):
    print("`timescale 1ns / 1ps")
    print("")
    print("module tb_" + properties["module_name"][0] + ";")
    print("")
    print("\t// TB parameters")
    _print_clk_periods(properties["input_clocks"])
    print("")
    print("\t// UUT parameters")
    _print_parameter_defs(properties["parameters"])
    print("")
    print("\t// Inputs")
    _print_signals(properties["inputs"], "input")
    print("")
    print("\t// Outputs")
    _print_signals(properties["outputs"], "output")
    print("")
    print("\t// Inouts")
    _print_signals(properties["inouts"], "inout")
    print("")
    print("\t// Instantiate UUT")
    create_instantiation._print_instantiation(properties, "\t")
    print("")
    print("\t// Generate clocks")
    _print_clock_generation(properties["input_clocks"])
    print("")
    _print_reset_task_template(properties["input_clocks"][0])
    print("")
    _print_initial_block(properties["input_clocks"][0])
    print("")
    print("endmodule")
    print("")

def _print_clk_periods(clks):
    for ii in clks:
        print("\tparameter " + ii.upper() + "_PER = 10;")

def _print_parameter_defs(params):
    loop_idx = 0
    for ii in params:
        if loop_idx % 3 == 0:
            print("\tparameter [" + str(params[loop_idx+1]-1) + ":0] " + ii + " = " + params[loop_idx+2] + ";")
        loop_idx += 1

def _print_signals(signals, io_type):
    if io_type == "output":
        sig_type = "wire"
    else:
        sig_type = "reg"

    loop_idx = 0
    for ii in signals:
        if loop_idx % 2 == 0:
            if sig_type == "reg":
                initializer = " = 0"
            else:
                initializer = ""

            if signals[loop_idx+1] == 1:
                dimensions = " "
            else:
                dimensions = " [" + str(signals[loop_idx+1]-1) + ":0] "

            print("\t" + sig_type + dimensions + ii + initializer + ";")
        loop_idx += 1

def _print_clock_generation(clks):
    for ii in clks:
        print("\talways #(" + ii.upper() + "_PER/2) " + ii + " = ~" + ii + ";")

def _print_reset_task_template(first_clk):
    print("\ttask release_reset;")
    print("\t\tinput integer reset_extra_cycles;")
    print("\tbegin")
    print("\t\t#100; // GSR")
    print("\t\t#(" + first_clk.upper() + "_PER*reset_extra_cycles);")
    print("\t\t@(posedge " + first_clk + ");")
    print("\t\t<reset_sig> <= <reset_deassert_value>;")
    print("\tend")
    print("\tendtask")

def _print_initial_block(first_clk):
    print("\tinitial begin")
    print("\t\trelease_reset(100);")
    print("")
    print("\t\t// ***** Add stimulus here *****")
    print("")
    print("\t\t// *****************************")
    print("")
    print("\t\t#(" + first_clk.upper() + "_PER*100);")
    print("\t\t$stop;")
    print("\tend")

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
        
        _print_tb(properties)

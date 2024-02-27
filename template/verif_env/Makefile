SIM_TIME_MS := 10
START_GUI ?= 0

SYNTH_SRCS := rtl/ \
		  	  xdc/

SIM_SRCS := tb/ \
			rtl/

TEST_VECTORS := test/test1.dat \
			  	test/test2.dat

BUILD_DIR := build/proj
PROJ_LOCKFILE=$(BUILD_DIR)/.lock
PROJ := $(BUILD_DIR)/proj.xpr
SIM_RESULTS := $(BUILD_DIR)/proj.sim/sim_1/behav/xsim/test1.log \
			   $(BUILD_DIR)/proj.sim/sim_1/behav/xsim/test2.log

SYNTH_DCP := $(BUILD_DIR)/proj.runs/synth_1/example.dcp
TIMING_REPORT := $(BUILD_DIR)/proj.runs/synth_1/example_timing_report.txt
UTILIZATION_REPORT := $(BUILD_DIR)/proj.runs/synth_1/*_utilization_synth.rpt

TIME := $(shell date "+%Y_%m_%d")

.ONESHELL:

.PHONY: all
all: display_results print_timing print_utilization

.PHONY: proj
proj: $(PROJ) ## Create Vivado project
$(PROJ_LOCKFILE): tcl/build_hardware.tcl $(SIM_SRCS) $(SYNTH_SRCS) $(TEST_VECTORS)
	rm -rf build; # If one of those files/directories changes, we need to re-build the vivado project since build_hardware.tcl isn't re-entrant
	mkdir -p build
	vivado -mode batch -notrace -source "$<"
	touch $(PROJ_LOCKFILE)

.PHONY: sim
sim: $(SIM_RESULTS) ## Run simulation
$(subst $(BUILD_DIR)/proj.sim,%,$(SIM_RESULTS)): tcl/run_sim.tcl $(TEST_VECTORS) $(SIM_SRCS) $(PROJ_LOCKFILE)
	vivado -mode tcl -notrace -source "$<" -tclargs $(SIM_TIME_MS) $(START_GUI)

.PHONY: synth
synth: $(SYNTH_DCP) ## Run synthesis
$(SYNTH_DCP) $(UTILIZATION_REPORT): tcl/run_synth.tcl $(SYNTH_SRCS) $(PROJ_LOCKFILE)
	vivado -mode tcl -notrace -source "$<"

.PHONY: timing_report
timing_report: $(TIMING_REPORT) ## Generate post-synthesis timing report
$(TIMING_REPORT): tcl/generate_timing.tcl $(SYNTH_DCP)
	vivado -mode tcl -notrace -source "$<"

.PHONY: print_timing
print_timing: $(TIMING_REPORT) ## Print post-synthesis timing report
	grep -A 6 -B 1 "Design Timing Summary" $<

.PHONY: print_utilization
print_utilization: $(UTILIZATION_REPORT) ## Print post-synthesis utilization report
	grep -A 90 -B 1 "Tool Version" $<

.PHONY: open_proj_gui
open_proj_gui: $(PROJ) ## Open the Vivado GUI
	vivado $<

BASENAME=$(shell basename $(shell pwd))
.PHONY: publish
publish: clean ## Publish an archive of the verification environment
	cd ..
	zip -r $(TIME)_$(BASENAME).zip $(BASENAME)

.PHONY: clean
clean: ## Clean the verification environment
	rm -rf .Xil Packages
	rm -f *.jou *.log *.str	
	rm -rf build

.PHONY: help
help: ## Print this message
	echo ""
	echo "example_verif_environment - Template for quickly setting up RTL verification environment"
	echo ""
	echo "Environment Variables"
	printf "\033[36m%-30s\033[0m %s\n" "SIM_TIME_MS (default 10)" "Length of time (in milliseconds) to run the simulation"
	printf "\033[36m%-30s\033[0m %s\n" "START_GUI (default 0)" "Allows launching of Vivado GUI after running certain targets"
	printf "\033[31m%37s\033[0m - %s\n" "0" "Do not launch Vivado GUI after running a target"
	printf "\033[31m%37s\033[0m - %s\n" "1" "Launch the Vivado GUI after running a target"
	echo ""
	echo "Targets"
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	echo ""

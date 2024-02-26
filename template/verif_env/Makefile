SIM_TIME_MS := 10
START_GUI ?= 1

SYNTH_SRCS := rtl/ \
		  				xdc/

SIM_SRCS := tb/ \
						rtl/

TEST_VECTORS := test/ar0231_macbeth_demosaic_only_small.dat \
			  				test/ar0231_rgb_cereal_small.dat

BUILD_DIR := build/proj
PROJ_LOCKFILE=$(BUILD_DIR)/.lock
PROJ := $(BUILD_DIR)/proj.xpr
SIM_RESULTS := $(BUILD_DIR)/proj.sim/sim_1/behav/xsim/ar0231_macbeth_demosaic_only_small.result \
			   			 $(BUILD_DIR)/proj.sim/sim_1/behav/xsim/ar0231_rgb_cereal_small.result

SYNTH_DCP := $(BUILD_DIR)/proj.runs/synth_1/ccm.dcp
TIMING_REPORT := $(BUILD_DIR)/proj.runs/synth_1/ccm_timing_report.txt
UTILIZATION_REPORT := $(BUILD_DIR)/proj.runs/synth_1/*_utilization_synth.rpt

TIME := $(shell date "+%Y_%m_%d")

.SILENT:
.PHONY: all testvector proj sim display_results synth timing_report print_timing print_utilization open_proj_gui publish clean
.ONESHELL:

all: display_results print_timing print_utilization

testvector: $(TEST_VECTORS)
test/%.dat: test/%.png
	python3 test/generate_testvector.py $^

proj: $(PROJ)
$(PROJ) $(PROJ_LOCKFILE): tcl/build_hardware.tcl $(SIM_SRCS) $(SYNTH_SRCS) $(TEST_VECTORS)
	rm -rf build; # If one of those files/directories changes, we need to re-build the vivado project since build_hardware.tcl isn't re-entrant
	mkdir -p build
	cd build
	vivado -mode batch -notrace -source "../$<"
	touch ../$(PROJ_LOCKFILE)

sim: $(SIM_RESULTS)
$(subst $(BUILD_DIR)/proj.sim,%,$(SIM_RESULTS)): tcl/run_sim.tcl $(TEST_VECTORS) $(SIM_SRCS) $(PROJ_LOCKFILE)
	cd build
	vivado -mode tcl -notrace -source "../$<" -tclargs $(SIM_TIME_MS) $(START_GUI)

display_results: $(SIM_RESULTS)
	python3 test/display_results.py $^

synth: $(SYNTH_DCP)
$(SYNTH_DCP): tcl/run_synth.tcl $(SYNTH_SRCS) $(PROJ_LOCKFILE)
	cd build
	vivado -mode tcl -notrace -source "../$<"

timing_report: $(TIMING_REPORT)
$(TIMING_REPORT): tcl/generate_timing.tcl $(SYNTH_DCP)
	cd build
	vivado -mode tcl -notrace -source "../$<"

print_timing: timing_report
	grep -A 6 -B 1 "Design Timing Summary" $(TIMING_REPORT)

print_utilization: synth
	grep -A 90 -B 1 "Tool Version" $(UTILIZATION_REPORT)

open_proj_gui: $(PROJ)
	vivado $<

publish: clean
	cd ..
	zip -r $(TIME)_ece5752_proj.zip ece5752_proj

clean:
	rm -rf .Xil Packages
	rm -f *.jou *.log *.str	
	rm -rf build
	rm -f test/*.dat

#-----------------------------------------------------------
# Abort if design already exists
#-----------------------------------------------------------
set proj_name "proj"
if { [file exists "build/${proj_name}"] == 1 } {
	puts "Aborting. Project already exists"
	exit -1
}

#-----------------------------------------------------------
# Create project
#-----------------------------------------------------------
create_project ${proj_name} "build/${proj_name}" -part xczu9eg-ffvb1156-2-e
set_property BOARD_PART xilinx.com:zcu102:part0:3.4 [current_project]

#-----------------------------------------------------------
# Add HDL source to design
#-----------------------------------------------------------
add_files -norecurse -fileset sources_1 "rtl/"
set_property top example [get_filesets sources_1]

#-----------------------------------------------------------
# Add xdc constraints to design
#-----------------------------------------------------------
add_files -norecurse -fileset constrs_1 "xdc/"

#-----------------------------------------------------------
# Add testbench source to design
#-----------------------------------------------------------
add_files -norecurse -fileset sim_1 "tb/"
set_property file_type {SystemVerilog} [get_files -of [get_filesets sim_1]]
set_property top tb [get_filesets sim_1]

#-----------------------------------------------------------
# Add test vectors to design
#-----------------------------------------------------------
add_files -norecurse -fileset sim_1 [glob "test/*.dat"]

exit

set SIM_TIME_MS [lindex $argv 0]
set START_GUI [lindex $argv 1]

open_project ../build/proj/proj.xpr
set_property -name {xsim.simulate.log_all_signals} -value {true} -objects [get_filesets sim_1]
launch_simulation
open_wave_config ../wcfg/tb_behav.wcfg
restart

puts "Running simulation for ${SIM_TIME_MS} ms..."
run ${SIM_TIME_MS} ms

if { ${START_GUI} == 1 } {
  start_gui
} else {
  exit
}

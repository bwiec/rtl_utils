
open_project ../build/proj/proj.xpr
open_run synth_1 -name synth_1
report_timing_summary -delay_type max -check_timing_verbose -max_paths 3 -file ../build/proj/proj.runs/synth_1/[get_property top [current_design]]_timing_report.txt

close_design
exit
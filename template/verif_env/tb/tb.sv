`timescale 1ns / 1ps

`include "example_tb_env.svh"
`include "example_if.svh"

import example_tb_env_pkg::*;

module tb;

    parameter TDATA_WIDTH_BYTES = 4;
    reg aclk;
    reg resetn;
    
    // Instantiate DUT
    example
    #(
        .TDATA_WIDTH_BYTES(TDATA_WIDTH_BYTES)
    )
    dut
    (
        .aclk(aclk),
        .resetn(resetn),
        .s_axis_a_tvalid(example_if1.s_axis_a_tvalid),
        .s_axis_a_tready(example_if1.s_axis_a_tready),
        .s_axis_a_tdata(example_if1.s_axis_a_tdata),
        .s_axis_b_tvalid(example_if1.s_axis_b_tvalid),
        .s_axis_b_tready(example_if1.s_axis_b_tready),
        .s_axis_b_tdata(example_if1.s_axis_b_tdata),
        .m_axis_tvalid(example_if1.m_axis_tvalid),
        .m_axis_tready(example_if1.m_axis_tready),
        .m_axis_tdata(example_if1.m_axis_tdata)
    );
    
    // Instantiate interface
    example_if
    #(
        .TDATA_WIDTH_BYTES(TDATA_WIDTH_BYTES)
    )
    example_if1
    (
        .aclk(aclk),
        .resetn(resetn)
    );
    
    // Instantiate top level env class
    example_tb_env_c example_tb_env;
    
    always begin
        #5 aclk = ~aclk;
    end
    
    initial begin
        resetn = 0;
        aclk = 0;
        repeat (5) @(posedge aclk);
        resetn = 1;
        
        example_tb_env = new("example_env", example_if1, example_if1);
        $display("Created example TB env");
        fork
            begin
                example_tb_env.run();
            end
        join
    end

endmodule

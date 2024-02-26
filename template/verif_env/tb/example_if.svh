interface example_if
#(
    parameter TDATA_WIDTH_BYTES = 4
)
(
    input logic aclk,
    input logic resetn
);

    logic s_axis_a_tvalid;
    logic s_axis_a_tready;
    logic [TDATA_WIDTH_BYTES*8-1:0] s_axis_a_tdata;
    logic s_axis_b_tvalid;
    logic s_axis_b_tready;
    logic [TDATA_WIDTH_BYTES*8-1:0] s_axis_b_tdata;
    logic m_axis_tvalid;
    logic m_axis_tready;
    logic [TDATA_WIDTH_BYTES*8-1:0] m_axis_tdata;

    clocking driver_cb @(posedge aclk); // Ports from the perspective of the 'TB'
        //default input #2ns output #2ns; // By default, this is the output relationship
        input aclk;
        input resetn;
        output s_axis_a_tvalid;
        input s_axis_a_tready;
        output s_axis_a_tdata;
        output s_axis_b_tvalid;
        input s_axis_b_tready;
        output s_axis_b_tdata;
        input m_axis_tvalid;
        output m_axis_tready;
        input m_axis_tdata;
    endclocking: driver_cb
    modport driver_mp (clocking driver_cb);

    clocking monitor_cb @(posedge aclk);
        //default input #2ns output #2ns; // By default, this is the output relationship
        input aclk;
        input resetn;
        input s_axis_a_tvalid;
        input s_axis_a_tready;
        input s_axis_a_tdata;
        input s_axis_b_tvalid;
        input s_axis_b_tready;
        input s_axis_b_tdata;
        input m_axis_tvalid;
        input m_axis_tready;
        input m_axis_tdata;
     endclocking: monitor_cb
     modport monitor_mp (clocking monitor_cb);

endinterface
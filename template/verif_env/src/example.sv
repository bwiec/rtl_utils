`timescale 1ns / 1ps

module example
#(
    parameter TDATA_WIDTH_BYTES = 4
)
(
    input aclk,
    input resetn,
    input s_axis_a_tvalid,
    output reg s_axis_a_tready,
    input [TDATA_WIDTH_BYTES*8-1:0] s_axis_a_tdata,
    input s_axis_b_tvalid,
    output reg s_axis_b_tready,
    input [TDATA_WIDTH_BYTES*8-1:0] s_axis_b_tdata,
    output reg m_axis_tvalid,
    input m_axis_tready,
    output reg [TDATA_WIDTH_BYTES*8-1:0] m_axis_tdata
);

    localparam [1:0] RECV = 2'b00,
                     CAPTURE = 2'b01,
                     SEND = 2'b10;
    reg [1:0] state;
    always @ (posedge aclk) begin
        if (!resetn) begin
            s_axis_a_tready <= 0;
            s_axis_b_tready <= 0;
            m_axis_tvalid <= 0;
            m_axis_tdata <= 0;
            state <= RECV;
        end else begin
            case (state)
                RECV: begin
                    s_axis_a_tready <= 0;
                    s_axis_b_tready <= 0;
                    m_axis_tvalid <= 0;
                    m_axis_tdata <= 0;
                    if (s_axis_a_tvalid && s_axis_b_tvalid) begin
                        s_axis_a_tready <= 1;
                        s_axis_b_tready <= 1;  
                        state <= CAPTURE;
                    end
                end CAPTURE: begin
                    s_axis_a_tready <= 0;
                    s_axis_b_tready <= 0;
                    m_axis_tdata <= s_axis_a_tdata + s_axis_b_tdata;
                    state <= SEND;
                end SEND: begin
                    m_axis_tvalid <= 1'b1;
                    if (m_axis_tready) begin
                        m_axis_tvalid <= 0;
                        m_axis_tdata <= 0;
                        state <= RECV;
                    end
                end default: begin
                    s_axis_a_tready <= 0;
                    s_axis_b_tready <= 0;
                    m_axis_tvalid <= 0;
                    m_axis_tdata <= 0;
                    state <= RECV;
                end                
            endcase
        end
    end
    
    
    
endmodule

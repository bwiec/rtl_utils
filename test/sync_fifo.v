
`timescale 1ns / 1ps

module sync_fifo
#(
    parameter DATA_WIDTH = 36,
    parameter FIFO_DEPTH = 1024
)
(
    // Global signals
    input                   clk,
	input                   ce,
	input                   rst,
	
	// Status signals
	output                  empty,
	output                  full,
	output                  overflow,
	output                  underflow,
        
    // Input interface
	input                   we,
    input  [DATA_WIDTH-1:0] din,
    
    // Output interface
	input                   oe,
    output [DATA_WIDTH-1:0] dout
);

	// Local parameters
	localparam FIFO_DEPTH_POW_2 = 2**$clog2(FIFO_DEPTH);
    
	// Local signals
	reg [$clog2(FIFO_DEPTH)-1:0] wr_ptr = 0;
	reg [$clog2(FIFO_DEPTH)-1:0] rd_ptr = 0;
	
	// RAM
	ram
	#(
		.DATA_WIDTH(DATA_WIDTH),
		.RAM_DEPTH(FIFO_DEPTH_POW_2)
	)
	ram_inst
	(
		.clk(clk),
		.din(din),
		.waddr(wr_ptr),
		.we(ce & we),
		.dout(dout),
		.raddr(rd_ptr),
		.oe(ce & oe)
	);
	
	// Drive flags
	reg [$clog2(FIFO_DEPTH)-1:0] rd_ptr_prev = 0-1'b1;
	always @ (posedge clk) begin
		if (rst) begin
			rd_ptr_prev <= 0-1'b1;
		end else begin
			if (ce && oe && !empty) begin
				rd_ptr_prev <= rd_ptr;
			end
		end
	end
	assign full      = (wr_ptr == rd_ptr_prev) ? 1'b1 : 1'b0; // Cant just use -1 due to roll around at end of FIFO_DEPTH
    assign empty     = (wr_ptr == rd_ptr)      ? 1'b1 : 1'b0;
	assign overflow  = full  && we;
	assign underflow = empty && oe;
	
	// Write pointer
	always @ (posedge clk) begin
        if (rst || (ce && we && (wr_ptr == FIFO_DEPTH-2)))
            wr_ptr <= 0;
        else if (ce && we)
            if (!full)
                wr_ptr <= wr_ptr + 1'b1;
    end
	
	// Read pointer
	always @ (posedge clk) begin
        if (rst || (ce && oe && (rd_ptr == FIFO_DEPTH-2)))
            rd_ptr <= 0;
        else if (ce && oe)
            if (!empty)
                rd_ptr <= rd_ptr + 1'b1;
    end

endmodule


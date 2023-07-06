
`timescale 1ns / 1ps
/////////////////////////////////////////////////////////////////////////
//
//
/////////////////////////////////////////////////////////////////////////

module edge_det
(
	input  clk,
	input  ce,
	input  sig_in,
	output redge_det,
	output fedge_det
);

	// Internal signals
	reg sig_in_1 = 0;
	
	// Capture rising edge of sig_in
	always @ (posedge clk) begin
		if (ce) begin
			sig_in_1 <= sig_in;
		end
	end
	//assign redge_det = ((sig_in_1 == 1'b0) && (sig_in == 1'b1) && ce) ? 1'b1 : 1'b0;
	assign redge_det = ~sig_in_1 && sig_in && ce;
    //assign fedge_det = ((sig_in_1 == 1'b1) && (sig_in == 1'b0) && ce) ? 1'b1 : 1'b0;
    assign fedge_det = sig_in_1 && ~sig_in && ce;	

endmodule


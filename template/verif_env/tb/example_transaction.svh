// This is generation of 'example_transaction' event. Kinda like an ethernet 'packet'
class example_transaction_c;
    
    int transaction_id;
    
    rand bit [31:0] a;
    rand bit [31:0] b;
    bit [31:0] result;
    
    constraint vals_c
    {
        a >= 0;
        a <= 100;
        b >= 0;
        b <= 100;
    }
    
    function new();
    endfunction
    
    function string to_string();
        string msg;
        msg = $sformatf("a=%4d, b=%4d", a, b);
        return msg;
    endfunction
    
    function void display(input string message);
        $display("-------------------------------------------------");
        $display("%s", message);
        $display("\tTransaction ID: %d", transaction_id);
        $display("\ta=%4d b=%4d result=%4d", a, b, result);
        $display("-------------------------------------------------");
    endfunction
    
    function bit compare(example_transaction_c rcvd);
        compare = 1;
        if (this.result != rcvd.result) begin
            compare = 0;
            $display("DATA MISMATCH");
            $display(this.result, " != ", rcvd.result);
            $stop;
        end
    endfunction
    
endclass
typedef example_transaction_c;
class example_checker_c;

    mailbox mbx_in;

    function new (mailbox mbx);
        mbx_in = mbx;
    endfunction
    
    task run;
        example_transaction_c example_transaction;
        $display("example_checker::run() called");
        forever begin
            mbx_out.get(example_transaction);  
        end
    endtask
endclass
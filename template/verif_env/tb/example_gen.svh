typedef example_transaction_c;
class example_gen_c;

    int num_example_transactions = 20; // Number of example_transactions to perform
    mailbox mbx_out; // Mailbox to put example_transactions into which the driver will pull from
    
    function new (mailbox mbx);
        mbx_out = mbx;
    endfunction
    
    task run;
        example_transaction_c example_transaction;
        for (int ii = 0; ii < num_example_transactions; ii++) begin
            example_transaction = new();
            assert(example_transaction.randomize());
            example_transaction.transaction_id = ii;
            mbx_out.put(example_transaction);
        end
    endtask
    
endclass
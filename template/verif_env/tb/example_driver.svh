typedef example_transaction_c;
class example_driver_c;
    
    virtual interface example_if.driver_mp driver_intf;
    mailbox mbx_input; // Read from gen
    
    function new(mailbox mbx, virtual interface example_if.driver_mp driver_intf);
        mbx_input = mbx;
        this.driver_intf = driver_intf;
    endfunction
    
    task run;
        example_transaction_c example_transaction;
        forever begin
            mbx_input.get(example_transaction);
            $display("example_transaction_drv::run: Got example_transaction %s", example_transaction.to_string());
            drive_example_transaction(example_transaction);
        end
    endtask
    
    task drive_example_transaction(example_transaction_c example_transaction);
        bit [3:0] delay = $random;
        repeat (2) @(driver_intf.driver_cb);
        if (driver_intf.driver_cb.resetn) begin
            driver_intf.driver_cb.s_axis_a_tvalid <= 1;
            driver_intf.driver_cb.s_axis_a_tdata <= example_transaction.a;
            driver_intf.driver_cb.s_axis_b_tvalid <= 1;
            driver_intf.driver_cb.s_axis_b_tdata <= example_transaction.b;
            $display("time=%t example_transaction_drv::drive_example_transaction: id=%4d a=%4d, b=%4d", $time, example_transaction.transaction_id, example_transaction.a, example_transaction.b);
            repeat (2) @(driver_intf.driver_cb);
            while (driver_intf.driver_cb.s_axis_a_tready == 0 || driver_intf.driver_cb.s_axis_b_tready == 0) begin
                repeat (2) @(driver_intf.driver_cb);
            end
            driver_intf.driver_cb.s_axis_a_tvalid <= 0;
            driver_intf.driver_cb.s_axis_a_tdata <= 0;
            driver_intf.driver_cb.s_axis_b_tvalid <= 0;
            driver_intf.driver_cb.s_axis_b_tdata <= 0;
            repeat (delay) @(driver_intf.driver_cb);
        end
    endtask
    
    task stall_output();
        forever @(driver_intf.driver_cb) begin
            bit [3:0] delay = $random;
            driver_intf.driver_cb.m_axis_tready <= 1;
            repeat (2) @(driver_intf.driver_cb);
            driver_intf.driver_cb.m_axis_tready <= 0;
            repeat (delay) @(driver_intf.driver_cb);
        end
    endtask
    
endclass
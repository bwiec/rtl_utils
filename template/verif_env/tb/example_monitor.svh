typedef example_transaction_c;
class example_monitor_c;

    virtual interface example_if.monitor_mp monitor_intf;
    mailbox mbx_out;

    function new (mailbox mbx, virtual interface example_if.monitor_mp monitor_intf);
        mbx_out = mbx;
        this.monitor_intf = monitor_intf;
    endfunction
    
    // Sample signals on port and create an example_transaction_c out of it
    task run;
        $display("example_monitor::run() called");
        fork // fork/join here helps with pipelined accesses (i.e. request is in-flight but not received on the output yet when the next input starts
            monitor();
        join
    endtask
    
    task monitor();
        integer transaction_id = 0;
        forever @(monitor_intf.monitor_cb) begin
            example_transaction_c example_transaction;
            example_transaction = new();
            wait ((monitor_intf.monitor_cb.s_axis_a_tvalid && monitor_intf.monitor_cb.s_axis_a_tready) && (monitor_intf.monitor_cb.s_axis_b_tvalid && monitor_intf.monitor_cb.s_axis_b_tready));
                example_transaction.a = monitor_intf.monitor_cb.s_axis_a_tdata;
                example_transaction.b = monitor_intf.monitor_cb.s_axis_b_tdata;
            wait (monitor_intf.monitor_cb.m_axis_tvalid && monitor_intf.monitor_cb.m_axis_tready);
                example_transaction.result = monitor_intf.monitor_cb.m_axis_tdata;
            example_transaction.transaction_id = transaction_id;
            example_transaction.display("DATA FROM MONITOR");
            mbx_out.put(example_transaction);
            transaction_id++;
        end
    endtask
endclass
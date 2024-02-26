package example_tb_env_pkg;

    `include "example_transaction.svh"
    `include "example_gen.svh"
    `include "example_driver.svh"
    `include "example_monitor.svh"
    
    class example_tb_env_c;
        string env_name;
                
        example_gen_c gen;
        example_driver_c driver;
        example_monitor_c monitor;
        //example_scoreboard_c scoreboard;
        
        mailbox mbx_gen_drv;
        mailbox mbx_mon_chk;
        
        virtual interface example_if.driver_mp driver_if;
        virtual interface example_if.monitor_mp monitor_if;
        
        function new(input string name, virtual interface example_if.driver_mp driver_if, virtual interface example_if.monitor_mp monitor_if);
            this.env_name = name;
            this.driver_if = driver_if;
            mbx_gen_drv = new();
            mbx_mon_chk = new();
            gen = new(mbx_gen_drv);
            driver = new(mbx_gen_drv, driver_if);
            monitor = new(mbx_mon_chk, monitor_if);
        endfunction;
        
        task run();
            $display("example_tb_env::run() called");
            fork
                gen.run();
                driver.run();
                driver.stall_output();
                monitor.run();
            join
        endtask
        
    endclass : example_tb_env_c
endpackage: example_tb_env_pkg
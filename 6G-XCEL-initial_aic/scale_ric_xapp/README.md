# scale_ric_xApp
This repository contains the implementation of a simple xApp that works with the scale-RIC. In order to run the xApp, check the ip address of your databus

Once you know the ip address, update the ip address in the `xApp.conf`. Once this is done, run the following command:

```shell
docker-compose up &
```

In order to stop the xApp, run the following command:

```shell
docker-compose down
```

If you want to interact with the xApp, you can attach your terminal to the container by runnng:

```shell
docker attach xapp
```

# Notes
The configuration of the xApp can be found in the `xApp.conf` file. The configuration includes the configuration of the databus ip address and the ports for reading measurements and sending commands.

# Registered BSs
I started working on the implementation of a register for all the BSs. Still no implementation on the BS side, but a testing tool was developed as part of the xApp package called `register_xapp.py`. This communicates with the register.py script on the `scale_ric_databus` side. This implementation should be used as follows:
- the databus runs and the impelemntation of the databus is used for transmiting data (as the name suggests)
- the `register.py` runns as a service that depends on the databus and it will implement a simple database (can be an array for now) that stores the cell_ids (`scale_ric_cell_id`). A separate array can be used to store measurements that are reported for each cell and commands impelmented for each cell.
- the BS will report all these values before it attaches to the databus
- once this is reported the BS will attach to the databus
- an xApp will first communicate with the register to check whether its configuration is feasible (if the measurement it requests are available and the commands as well). Then it will attach to the databus
- the register will ping the BS every 2sec to check whether it is still attached, if not, it will send a command to the xApp to stop it or the xApp can ping the register to check if the cell is still available

The register is using a request response pattern which requires the server that binds to the address (not the one that connects) to receive and then send a message, and the consumer sends a message and then waits for a response.

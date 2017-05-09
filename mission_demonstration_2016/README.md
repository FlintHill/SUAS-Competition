# AUVSI SUAS Competition 2016 - 2017

This folder contains all of the scripts for the Mission Demonstration.

Each folder contains instructions for how to run each individual code component. Below are general instructions on how to run the whole system (which order to run the software components in and on what devices).

## MAVProxy

1) Go to main MAVProxy base directory, then into the ```MAVProxy``` directory
2) Run ```mavproxy.py``` script with the following command:

```
sudo python mavproxy.py --console --master=tcp:127.0.0.1:5760 --out=tcpin:127.0.0.1:14551 --out=tcpin:0.0.0.0:14550
```

This will start up MAVProxy and connect to the UAV over the USB interface.

## Client

To run the Client script, cd into the ```gcs``` directory, then run

```
python client.py
```

Ensure that the version of Python you are using is 2.7.x. If attempting to use Python 3, the program will crash with a Timeout command.

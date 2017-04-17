# MAVProxy

This folder contains all scripts to run MAVProxy at Mission Demonstration. Below are instructions for use.

## Instructions

1) Go to main MAVProxy base directory, then into the ```MAVProxy``` directory
2) Run ```mavproxy.py``` script with the following command:

```
python mavproxy.py --console --master=/dev/ttyUSB0 --out=tcpin:0.0.0.0:14550 --out=tcpin:0.0.0.0:14551
```

This will start up MAVProxy and connect to the UAV over the USB interface.

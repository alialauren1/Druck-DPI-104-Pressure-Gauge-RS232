# DPI 104 Pressure Gauge Logger

Python script to poll the GE Druck DPI 104 pressure gauge over RS232 and log readings to a CSV file.

## Requirements

- USB-to-RS232 adapter (FTDI recommended)
- Python 3
- pyserial library: `pip3 install pyserial`

## How to run

Connect the USB-to-RS232 adapter and verify the port:

```bash
ls /dev/tty.usbserial-*
```

Then run the script:

```bash
python3 "/Users/aliawolken/Desktop/pressure gauge dpi 104/dpi104_log.py"
```

Press **Ctrl+C** to stop logging.

## How the script works

### Serial connection
Opens the USB-to-RS232 adapter at **9600 baud, 8N1, no flow control** — the settings required by the DPI 104 (documented in GE Druck Technical Note TN0719).

### Wake and unit setup
On startup the script sends one dummy read command to wake the gauge (the DPI 104 ignores the first command if it was sleeping), then sends `IU1=01` to force the units to **bar** regardless of what the front panel is set to.


## Output

CSV file is hard coded:

```
/Users/aliawolken/Desktop/pressure gauge dpi 104/dpi104_log.csv
```

Columns: `Timestamp, Pressure_bar`

Example:
```
Timestamp,Pressure_bar
2026-05-01 14:23:01.234,0.0900
2026-05-01 14:23:02.241,0.0900
2026-05-01 14:23:03.249,0.0800
```


To see just the last 20 readings:

```bash
tail -20 "/Users/aliawolken/Desktop/pressure gauge dpi 104/dpi104_log.csv"
```

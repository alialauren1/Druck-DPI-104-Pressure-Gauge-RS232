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

## Requirements
- Python 3
- pyserial: `pip3 install pyserial`
- USB-to-RS232 adapter (FTDI-based recommended) and the DPI 104 RS-232 cable

## Setup on a new computer
1. Plug in the USB-to-RS232 adapter and connect it to the DPI 104.
2. Find the adapter's port name:
   - Mac: `ls /dev/tty.usbserial-*`
   - Linux: `ls /dev/ttyUSB*`
   - Windows: Device Manager → Ports (COM & LPT), e.g. `COM3`
3. Open `dpi104_log.py` and edit the two settings at the top:
   - `PORT` — the port name from step 2
   - `OUTFILE` — full path where the CSV should be saved (the folder must already exist)

## Running
1. Turn on the DPI 104.
2. In a terminal, go to the script's folder and run:
   `python3 dpi104_log.py`
3. The terminal prints each reading as it is logged.
4. Press Ctrl+C to stop. Data is saved after every reading, so nothing is lost.

## Important notes
- **The CSV is overwritten each run.** Rename or move `dpi104_log.csv` before starting a new run.
- Sampling is about once per second (slightly slower than 1 Hz).
- Units are forced to bar on startup, regardless of the gauge's front panel setting.
- Timestamps come from the computer's clock, taken after each reply is received.
- If nothing prints: check the port name, that the gauge is on, and the cable connection.

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

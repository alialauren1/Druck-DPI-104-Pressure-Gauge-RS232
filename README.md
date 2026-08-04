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

### Command format
The DPI 104 uses a framed ASCII protocol. The pressure read command is:

```
#IR1?:60<CR><LF>
```

- `#` — direct mode (single instrument, no daisy-chain addressing)
- `IR1?` — read input channel 1 (pressure)
- `:60` — colon followed by a 2-digit checksum (modulo-100 sum of ASCII codes of all characters)
- `<CR><LF>` — terminator

### Response format
The gauge replies with:

```
!IR1=  0.09:19
```

- `!` — instrument response character
- `IR1=` — channel identifier
- `0.09` — pressure value in bar (may have leading spaces)
- `:19` — checksum (not pressure data, can be ignored)

### Parsing
The `parse_response()` function uses a regex to extract just the numeric value from the response, ignoring the leading spaces and the trailing checksum.

### Main loop
Every second the script:
1. Sends the read pressure command
2. Reads back one line from the gauge
3. Parses the pressure value
4. Grabs the current timestamp from the computer clock
5. Prints to the terminal and writes to the CSV
6. Flushes the CSV to disk so data is not lost on Ctrl+C

## Output

CSV file saved to the same folder as the script:

```
dpi104_log.csv
```

Columns: `Timestamp, Pressure_bar`

Example:
```
Timestamp,Pressure_bar
2026-05-01 14:23:01.234,0.0900
2026-05-01 14:23:02.241,0.0900
2026-05-01 14:23:03.249,0.0800
```

## Viewing data in the terminal

To print the CSV to the terminal while the script is not running:

```bash
cat "/Users/aliawolken/Desktop/pressure gauge dpi 104/dpi104_log.csv"
```

To watch the file update in real time while the script is running (in a second terminal window):

```bash
tail -f "/Users/aliawolken/Desktop/pressure gauge dpi 104/dpi104_log.csv"
```

To see just the last 20 readings:

```bash
tail -20 "/Users/aliawolken/Desktop/pressure gauge dpi 104/dpi104_log.csv"
```

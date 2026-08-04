import serial, re, datetime, time

PORT    = '/dev/tty.usbserial-A403FLOX'
BAUD    = 9600
OUTFILE = '/Users/aliawolken/Desktop/pressure gauge dpi 104/dpi104_log.csv'

READ_PRESSURE = b'#IR1?:60\r\n'
SET_UNITS_BAR = b'#IU1=01:58\r\n'

def parse_response(line):
    m = re.match(r'!IR1=\s*([+-]?\d+\.?\d*):', line)
    if m:
        return float(m.group(1))
    return None

# open a virtual serial port connection, give 1 sec timeout if gauge doesnt respond 
with serial.Serial(PORT, BAUD, bytesize=8, parity='N', stopbits=1, 
                   timeout=1, rtscts=False, xonxoff=False) as ser, \
     open(OUTFILE, 'w') as f:

    f.write('Timestamp,Pressure_bar\n') 

    ser.write(READ_PRESSURE) # asks gauge for a reading
    time.sleep(0.5)
    ser.reset_input_buffer()

    ser.write(SET_UNITS_BAR)
    time.sleep(0.2)
    ser.reset_input_buffer()

    print('Logging to ' + OUTFILE + '  (Ctrl+C to stop)')

    # Gauge doesnt stream data on its own
    # The following asks for data and gauge responds each loop
    while True: 
        ser.write(READ_PRESSURE)
        line = ser.readline().decode('ascii', errors='ignore').strip() # listens on serial port and reads bytes until it sees \n (line terminator that the gauge sends)
        if line:
            val = parse_response(line)
            if val is not None:
                ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                print(f'P = {val:.4f} bar  {ts}')
                f.write(f'{ts},{val:.4f}\n')
                f.flush()
        time.sleep(1.0)

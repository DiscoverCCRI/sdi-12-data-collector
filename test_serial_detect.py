import serial.tools.list_ports  # For listing available serial ports

VID_FTDI = 0x0403;

available_ports = serial.tools.list_ports.comports()
print('\nDetected the following serial ports:')
i=0
for port in available_ports:
    vidn=port.vid if (type(port.vid) is int) else 0
    sern=port.serial_number if (type(port.serial_number) is str) else 'NONE'
    sern=sern[:-1] if ((type(port.vid) is int) and (port.vid==VID_FTDI) and (platform.system()=='Windows')) else sern # Windows OS FTDI driver adds 'A' to the end of the serial number.
    print('%d)\t%s\t(USB VID=%04X)\t Serial#:=%s' % (i, port.device, vidn, sern))
    i=i+1
total_ports = i  # now i= total ports

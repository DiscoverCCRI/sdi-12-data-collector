import serial.tools.list_ports  # For listing available serial ports
import platform # For detecting operating system flavor and computer architecture

VID_FTDI = 0x0403;

available_ports = serial.tools.list_ports.comports()

for port in available_ports:
    #vidn=port.vid if (type(port.vid) is int) else 0
    #sern=port.serial_number if (type(port.serial_number) is str) else 'NONE'
    #sern=sern[:-1] if ((type(port.vid) is int) and (port.vid==VID_FTDI) and (platform.system()=='Windows')) else sern # Windows OS FTDI driver adds 'A' to the end of the serial number.
    #print('%d)\t%s\t(USB VID=%04X)\t Serial#:=%s' % (i, port.device, vidn, sern))
    if port.vid == VID_FTDI:
        print("Found SDI-12 USB Adapter")
        sdi_12_adapter = port.device
        sdi_12_adapter_sern = port.serial_number

    else:
        print("No match found")

print(f"Found the SDI-12 USB Adapter Serial #: {sdi_12_adapter_sern} at {sdi_12_adapter}")

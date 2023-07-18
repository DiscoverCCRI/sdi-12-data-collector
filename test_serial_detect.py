import serial.tools.list_ports  # For listing available serial ports
import platform # For detecting operating system flavor and computer architecture
import time  # For delaying in seconds
from datetime import datetime  # For finding system's real time
import socket # For collecting the system hostname to be added to the conf file.
import sys  # For reading command-line arguments and exiting program with exit code
import re  # For regular expression support
import yaml # For loading config file
import utils # For data scrubbing and file output


def generate_filename(file_path):
    system_hostname = socket.gethostname()
    date = datetime.now.strftime("%Y-%m-%d")

    filename = f"{file_path}{system_hostname}-sdi-12-{date}.csv"
    return filename


def get_sdi_12_port_info():
    # USB VID for the SDI-12 USB Adapter
    VID_FTDI = 0x0403
    available_ports = serial.tools.list_ports.comports()

    for port in available_ports:
        # Check if current port's VID matches the known USB VID for the SDI-12 USB Adapter
        if port.vid == VID_FTDI:
            print(f"[+] Found SDI-12 USB Adapter at {port.device}")
            print(f"[+] Serial #: {port.serial_number}\n")
            return port.device
            
        else:
            print("[-] No match found, checking next port...\n")

    print("[-] No matching USB VID found. Is the SDI-12 USB Adapter plugged in?")


def get_sensor_info(open_serial_port, sensor_addresses):
    for address in sensor_addresses:
        open_serial_port.write(address.encode() + b'I!')
        sensor_info = open_serial_port.readline()
        print('Sensor address:', address, ' Sensor info:', sensor_info.decode('utf-8').strip())


def load_config():
    try:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        return config
    
    except FileNotFoundError:
        print("[-] No config file found; please refer to the GitHub repo for a working example.")
        sys.exit(1)


def read_sdi_12_sensors(open_serial_port, sensor_addresses, sensor_commands):
    # Generate timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Collect hostname
    system_hostname = socket.gethostname()

    # Set up output_data string
    output_data = current_time + ',' + system_hostname

    # This is the flag to break out of the inner loops and continue the next data point loop in case no data is received from a sensor such as the GPS.
    no_data = False
    # Read each sensor and append to output string
    for (cmd_iterator, address) in enumerate(sensor_addresses):
        values = []  # clear before each sensor
        sdi_12_line_buffer = b''  # This stores all data from the same sensor address, including from M!->D0! D1!, M1!->D0!, D1! etc.
        for command in sensor_commands[cmd_iterator]:
            try:
                if command == '0':
                    complete_command = address.encode() + b'M!'
                else:
                    complete_command = address.encode() + b'M' + command.encode() + b'!'
                
                # Start the SDI-12 sensor measurement
                open_serial_port.write(complete_command) 
                sdi_12_response = open_serial_port.readline()

                # Didn't get a response from the sensor? Check for faulty wiring.
                if sdi_12_response == b'':
                    print(f"Sensor {address} failed to respond to command {complete_command}")
                    
                    # End the current iteration of sensors and commands on each sensor and wait for the next iteration.
                    no_data = True 
                    break

                # remove \r and \n since [0-9]$ has trouble with \r
                sdi_12_response = sdi_12_response[:-2]
                
                # This should match a number ([0-9]) that appears at the end of the response ($), which is a 1-digit number of "returned values"
                match_result = re.search(b'[0-9]$', sdi_12_response)

                if (not match_result):
                    # Match evaluates into True. The response is wrong. There should be a number at the end of the response, save \r\n, but it is not in this response.
                    # End the current iteration of sensors and commands on each sensor and wait for the next iteration.
                    no_data = True
                    break

                # Find out how many values are returned
                total_returned_values = int(match_result.group(0))
                
                # Read the service request line
                sdi_12_response = open_serial_port.readline()

                # Read as much data as you can with D0, D1, ... D9 until only the address and \r\n is returned
                for d_command in range(10):
                    complete_command = address.encode() + b'D' + str(d_command).encode() + b'!'
                    # Request data
                    open_serial_port.write(complete_command)
                    # Read the data line
                    next_sdi_12_response = open_serial_port.readline()

                    # only 1\r\n is returned, indicating that the sensor has run out of values to return. It's time to stop asking.
                    if (len(next_sdi_12_response) <= 3):
                        break
                    else:
                        # remove address, \r and \n since [0-9]$ has trouble with \r, stitch all responses from D0! to D9! together for later processing.
                        next_sdi_12_response = next_sdi_12_response[1:-2]
                        # Append results from the Dn! command to data from D0! to Dn-1!
                        sdi_12_line_buffer += next_sdi_12_response
            
            except serial.serialutil.SerialException as err:
                print(err.__str__())
                open_serial_port.close()
                sys.exit(1)

            # extract the returned values from SDI-12 sensor and append to values[]
            for iterator in range(total_returned_values):
                # search a number string with preceding + or - sign and any number of digits and decimal (+).
                match_result = re.search(b'[+-][0-9.]+', sdi_12_line_buffer)

                # if values found is less than values indicated by return from M, report no data found. 
                # This is a simple solution to GPS sensors before they acquire lock. For sensors that have lots of values to return, you need to find a better solution.
                try:
                    # convert into a number. Decode byte string into string first due to MicroPython.
                    values.append(float(match_result.group(0).decode()))
                    sdi_12_line_buffer = sdi_12_line_buffer[len(match_result.group(0)):]
                
                except AttributeError:
                    print(f"No data received from sensor at address {address}\n")
                    no_data = True
                    break

            if no_data:
                break

        output_data = output_data + ',' + address
        for value in values:
            # Output returned values
            output_data = output_data + f",{value}"

    return output_data


def main():
    # Load parameters from config file
    config = load_config()

    # Connect to the SDI-12 USB Adapter
    sdi_12_device = get_sdi_12_port_info()
    
    # Open serial port and wait for arduino bootloader
    sdi_12_adapter = serial.Serial(port=sdi_12_device, baudrate=9600, timeout=10)
    time.sleep(2.5)

    # Establish the currently connected sensor addresses, get relevant info to validate connection.
    get_sensor_info(sdi_12_adapter, config['sdi_12_address'])

    # Generate filename and open CSV file
    data_filename = generate_filename(config['data_output_path'])
    data_file = utils.setup_csv(data_filename, config['header'])  # open config_file_name_yyyymmdd.csv for appending

    # Read and clean up sensor data
    output_data = read_sdi_12_sensors(sdi_12_adapter, config['sdi_12_address'], config['sdi_12_command'])
    formatted_data = utils.format_output(output_data, config['sdi_12_address'], config['connected_devices']) + '\n'
    
    print(f"The following data will be stored in {data_filename}: \n\t{formatted_data}")

    data_file.write(formatted_data)
    data_file.flush()

    sdi_12_adapter.close()
    data_file.close()


if __name__ == "__main__":
    main()

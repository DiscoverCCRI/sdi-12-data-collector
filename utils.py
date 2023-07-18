# Imports
import os
import math
from datetime import datetime  # For finding system's real time
import socket # For collecting the system hostname to be added to the conf file.
import yaml # For loading config file
import sys  # For reading command-line arguments and exiting program with exit code


def format_output(data_str, addresses, connected_devices):
    # Convert data string into list and trim off the last 7 irrelevant data points
    csv_data = data_str.split(",")[:-7]
    
    # Scan through the data to see if there's a match with known SDI-12 devices
    for address in addresses:
        for index in range(len(csv_data)):
            if address == csv_data[index]:
                # If a known SDI-12 address matches with an address in the data, 
                # overwrite the address with a common sensor name
                csv_data[index] = connected_devices[csv_data[index]]
    
    temp_kelvin = voltage_to_kelvin(float(csv_data[-1]))
    csv_data.append("%0.2f" % temp_kelvin)

    # Return newly formatted data as a string
    return ",".join(csv_data)


def generate_filename(file_path):
    system_hostname = socket.gethostname()
    date = datetime.now().strftime("%Y%m%d")

    filename = f"{file_path}{system_hostname}-sdi-12-{date}.csv"
    return filename


def load_config():
    try:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        return config
    
    except FileNotFoundError:
        print("[-] No config file found; please refer to the GitHub repo for a working example.")
        sys.exit(1)


def setup_csv(filepath, header):
    file_exists = os.path.exists(filepath)

    if(file_exists):
        # Open existing file
        file = open(filepath, 'a')
        
    else:
        # Open the new file and write header
        file = open(filepath, 'w')
        file.write(header + '\n')
        
    return file

def voltage_to_kelvin(volts):
    resistance = 100000 * (volts / (5-volts))
    R0 = 100000
    # B value from KOKISO 100k thermistor sales page
    B = 3950

    temp_kelvin = 1 / ( (1 / 298) + (1 / B) * ( math.log(resistance / R0) ) )
    
    return temp_kelvin

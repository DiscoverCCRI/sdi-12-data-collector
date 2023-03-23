# Imports
import os

# Known SDI-12 device addresses
# TODO: Maybe this should go in a config file!
SDI_12_DEVICES = {
    'a' : 'TEROS-12',
    'b' : 'MPS-6',
    'z' : '100K-THERMISTOR'
}

HEADER = "DateTime,Hostname,Sensor1,VWC(m^3),Temp(°C),EC(dS/m),Sensor2,WaterPotential(kPa),Temp(°C),Sensor3,Voltage(V)\n"

def format_output(data_str):
    # Convert data string into list and trim off the last 7 irrelevant data points
    csv_data = data_str.split(",")[:-7]
    
    # Scan through the data to see if there's a match with known SDI-12 devices
    for address in list(SDI_12_DEVICES.keys()):
        for index in range(len(csv_data)):
            if address == csv_data[index]:
                # If a known SDI-12 address matches with an address in the data, 
                # overwrite the address with a common sensor name
                csv_data[index] = SDI_12_DEVICES[csv_data[index]]

    # Return newly formatted data as a string
    return ",".join(csv_data)


def setup_csv(filepath):
    file_exists = os.path.exists(filepath)

    if(file_exists):
        file = open(filepath, 'a')
        
    else:
        # Open the new file and write header
        file = open(filepath, 'w')
        file.write(HEADER)
        
    return file

def voltage_to_kelvin(volts):
    pass

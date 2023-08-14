# sdi-12-data-logger
Data logger to read and store SDI-12 data by interfacing with Dr. Liu's SDI-12 USB Adapter.

Official documentation can be found [here](https://liudresllc.com/gadget/sdi-12-usb-adapter/).


 <img width="384" alt="Screen Shot 2023-08-14 at 3 00 53 PM" src="https://github.com/MichaelChestnut/sdi-12-data-collector/assets/72172361/52265a65-6d54-4e57-a4b4-d9c96df7daf2">


## Initializing SDI-12 Sensor Addresses Using The USB Adapter:

There are a few important details to keep in mind when initializing sensors using the SDI-12 USB adapter. 

 1. Only one ***digital*** sensor may be wired into the USB adapter at a time. If more than one **digital** sensor is wired into the adapter, the sensor intitialization **will not** work.
      - For clarification: You are able to initialize a digital sensor address even if analog sensors are wired into the adapter.
 2. Analog sensors should hold a default sensor address of z.
 3. The script sdi_12_initialization.py has interactive steps to walk through the initialization of the sensors.
 4. Repeat the script as necessary for each sensor, as you can only initialize **one at a time!**


## Wiring Sensors

A few examples of wiring sensors into the SDI-12 USB adapter are shown below

Digital Wiring Reference With MPS-6:

<img width="482" alt="Screen Shot 2023-08-08 at 7 16 59 PM" src="https://github.com/MichaelChestnut/sdi-12-data-collector/assets/72172361/589414aa-0649-4c3a-8196-1d16046cfc1b">


Digital Wiring Reference With TEROS-12:

<img width="499" alt="Screen Shot 2023-08-08 at 7 17 12 PM" src="https://github.com/MichaelChestnut/sdi-12-data-collector/assets/72172361/dcfe6864-ae0d-4bee-9113-159e5c932cc5">


MPS-6 and TEROS-12 In Adapter:

<img width="234" alt="Screen Shot 2023-08-08 at 7 17 23 PM" src="https://github.com/MichaelChestnut/sdi-12-data-collector/assets/72172361/a9028925-15e6-49b0-b513-a8430676f178">

Analog Wiring Reference With Thermistor:

<img width="693" alt="Screen Shot 2023-08-08 at 7 18 39 PM" src="https://github.com/MichaelChestnut/sdi-12-data-collector/assets/72172361/03a84599-383c-43a8-9096-49cc54d81fee">



## Using the SDI-12 Adapter

- Pull this repository to your device:
  ```
  git clone https://github.com/MichaelChestnut/sdi-12-data-collector.git
  ```
- Install pyserial:
  ```
  pip install pyserial
  ```
- 


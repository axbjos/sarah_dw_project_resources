'''
Very crude example of using the "Bleak" Bluetooth Library with Python.

Bleak should run on anything that runs Python.

https://bleak.readthedocs.io/en/latest/

'''
# use asyncio for I/O bound processes
import asyncio

# you must first use pip to install bleak
from bleak import BleakClient

# find this address by running the "ble_scanner.py" python file first
# use it to obtain the UUID of the Arduino and the UUID of the service 
# being offered

# UUID of Arduino
address = "106C2542-49BA-1830-96E4-52DE905C54BF"
# UUID of the "characterisic" aka the value you want to read - the temperature
characteristic_id = "00002101-0000-1000-8000-00805f9b34fb"

# define a main function that can be run asynchronously
async def main(address):
    # prob unfamiliar syntax, but look up what's going on here
    async with BleakClient(address) as client:
        # for grins grab the services being advertised by the Arduino
        # services var should be an object
        services = client.services
        charac = services.get_characteristic(11)
        # grab the "characteristic" being offered, charac should be an object
        #charac = services.characteristics.get(11)
        #charac = services
        print("Services are: ", services, "Characteristics are: ", charac)
        # now loop a few times and get the characteristic from the Arduino
        # which should be the temp in celsius (or close to it)
        for i in range(50):
            # get the data from the bluetooth connection
            data = await client.read_gatt_char(characteristic_id)
            # data read from the bluetooth connection is going to return a byte array of hex
            # so take this data, decode as hex, then convert to an integer
            arduino_value = int(data.hex(),16)

            print("Data from Arduino", arduino_value)
            print("Converted to Fahrenheit: ", (arduino_value*9.0/5.0)+32)

asyncio.run(main(address))
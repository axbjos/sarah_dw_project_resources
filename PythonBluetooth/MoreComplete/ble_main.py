import asyncio
from bleak import BleakClient
import logging
import sys
import paho.mqtt.publish as publish

# use python loggin functionality
logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,  #set logging level
    datefmt="%H:%M:%S",
    #stream=sys.stderr, #use this if you just want logs sent to console
    filename='ble_main.log',  #use this if you want logs sent to file.
)
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True

async def read_ble(address, characteristic_id):

    async with BleakClient(address) as client:
        # get the data from the bluetooth connection
        data = await client.read_gatt_char(characteristic_id)
        # data read from the bluetooth connection is going to return a byte array of hex
        # so take this data, decode as hex, then convert to an integer
        arduino_raw_value = int(data.hex(),16)
        arduino_fahrenheit = (arduino_raw_value*9.0/5.0)+32
        logger.info("Raw Arduino Data: %s", arduino_raw_value)
        logger.info("Converted Fahrenheit Temp: %s", arduino_fahrenheit)

        return arduino_fahrenheit

def publish_mqtt_data(temperature):

    publish.single("bluetooth", payload=temperature, hostname="192.168.68.70")

async def main():

    # UUID of Arduino - Macs use UUID
    address = "106C2542-49BA-1830-96E4-52DE905C54BF"
    # UUID of the "characterisic" aka the value you want to read - the temperature
    characteristic_id = "00002101-0000-1000-8000-00805f9b34fb"
    
    while True:

       #gather data from ble
       temperature = await read_ble(address, characteristic_id)

       #publish data to mqtt
       publish_mqtt_data(temperature)

       await asyncio.sleep(5)

asyncio.run(main())
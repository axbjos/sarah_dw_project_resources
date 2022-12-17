''' 
Use "pip" (Pi) or "pip3" (Mac) to make sure dependencies are installed
pip install bleak
pip install paho-mqtt
pip install asyncio 

Reads data from a BLE Arduino running the code from the ArduinoBluetooth Directory
Arduino is advertising one "characteristic" that is a temperature value 
'''
import asyncio
from bleak import BleakClient
import logging
import paho.mqtt.publish as publish
#import sys #only needed if streaming logs to the console

#### program startup stuff ####
# use the built-in python logging framework
# code below will send logging data a file named ble_main.log in the 
# directory as the code
logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,  #set logging level, set to DEBUG if you want more
    datefmt="%H:%M:%S",
    #stream=sys.stderr, #use this if you just want logs sent to console
    filename='ble_main.log',  #use this if you want logs sent to file.
)
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True

### read config file
config_file = open("ble_main.conf", "r")

first_line = config_file.readline().split(":")
ble_address = first_line[1][:-1]
logger.info("BLE address is %s", ble_address)

second_line = config_file.readline().split(":")
characteristic_id = second_line[1][:-1]
logger.info("Characterisic UUID is %s",characteristic_id)

third_line = config_file.readline().split(":")
mqtt_broker_ip = third_line[1][:-1]
logger.info("MQTT Broker IP is %s",mqtt_broker_ip)

config_file.close()

### functions ###
async def read_ble(address, characteristic_id):

    async with BleakClient(address) as client:
        # get the data from the bluetooth connection
        data = await client.read_gatt_char(characteristic_id)
        # data read from the bluetooth connection is going to return a byte array of hex
        # so take this data, decode as hex, then convert to an integer
        arduino_raw_value = int(data.hex(),16)  #hex value
        arduino_fahrenheit = (arduino_raw_value*9.0/5.0)+32   #fahrenheit integer
        logger.debug("Raw Arduino Data: %s", arduino_raw_value)  #log hex value as a "debug" thing
        logger.info("Converted Fahrenheit Temp: %s", arduino_fahrenheit)  #log fahrenheit as "info" thing

        return arduino_fahrenheit

def publish_mqtt_data(temperature, broker_ip):

    publish.single("bluetooth", payload=temperature, hostname=broker_ip)
    logger.info("Temperature published to MQTT at 192.168.68.70")

async def main():
    
    while True:

       #gather data from ble
       temperature = await read_ble(ble_address, characteristic_id)

       #publish data to mqtt
       publish_mqtt_data(temperature, mqtt_broker_ip)

       await asyncio.sleep(5)

### runner ###
asyncio.run(main())
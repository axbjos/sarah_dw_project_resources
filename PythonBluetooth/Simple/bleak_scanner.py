import asyncio
from bleak import BleakScanner

async def run():
    devices = await BleakScanner.discover()
    for d in devices:
        #print(d.metadata)
        print(d.address)
        print(d.details)
        print(d.name)
        #print(d.rssi)
        print()
            
loop = asyncio.get_event_loop()
loop.run_until_complete(run())
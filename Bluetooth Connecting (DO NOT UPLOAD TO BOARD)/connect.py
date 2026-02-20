import asyncio
from bleak import BleakScanner, BleakClient

char_uuid = "19b10001-e8f2-537e-4f6c-d104768a1214"
dev_name = "Arduino"

async def findArduino():
    devices = await BleakScanner.discover()
    for d in devices:
        if (d.name and dev_name in d.name):
            print(f'{dev_name} found!')
            return d
    print(f'{dev_name} not found!')

async def main():
    arduino = await findArduino()

    async with BleakClient(arduino) as client: # type: ignore
        print(f'{client.name} connected!')
        print(f'Arduino address: {client.address}\n')

        led_char = client.services.get_characteristic(char_uuid)

        print(led_char.properties) # type: ignore

        prev_value = 0

        while True:
            curr_value = await client.read_gatt_char(led_char) # type: ignore
            if curr_value != prev_value:
                print(f'New LED Value: {curr_value}')
            prev_value = curr_value

        
    print(f'{dev_name} disconnected!')

asyncio.run(main())
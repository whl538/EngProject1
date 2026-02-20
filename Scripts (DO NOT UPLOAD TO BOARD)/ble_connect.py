"""
Python program to connect to an Arduino board via BLE and log some data to a text file.

Author: Luna Brooker
Date: 20th February 2026
"""

import asyncio
from bleak import BleakScanner, BleakClient
from datetime import datetime

char_uuid = '19b10001-e8f2-537e-4f6c-d104768a1214'  # Unique ID of the desired characteristic to log
device_name = 'Arduino'  # Device name to search for
path_to_log = '../log.txt'  # Path to the log file
timeout = 5.0  # Timeout value in minutes

async def findArduino(dev_name):
    """Find the Arduino device containing the given name
    Parameters:
      `dev_name` (string): The name of the device to connect to
    """
    devices = await BleakScanner.discover()
    for d in devices:
        if (d.name and dev_name in d.name):
            print(f'{dev_name} found!')
            return d
    print(f'{dev_name} not found!')

async def main():
    arduino = await findArduino(device_name)  # Find the arduino

    async with BleakClient(arduino) as client: # type: ignore  # Connect to arduino
        print(f'{client.name} connected!')
        print(f'Arduino address: {client.address}\n')

        # Open/Create a log file
        try:
            f = open(path_to_log, 'w')
        except:
            print('Error opening log file. Aborting...')
            exit()

        led_char = client.services.get_characteristic(char_uuid)  # Hook into desired characteristic

        # Set defaults for values to update later
        prev_value = 0
        last_updated = datetime.now()

        while True:
            try:
                curr_value = await client.read_gatt_char(led_char) # type: ignore  # Read the value of the characteristic
                curr_value = int.from_bytes(curr_value, byteorder='little', signed=False)  # Convert to int
                # Check current value against previous to see if there is any need to update
                if curr_value != prev_value:
                    last_updated = datetime.now()            # Update the time of the latest data update
                    # Print, log, and update the new value
                    print(f'New LED Value: {curr_value}')
                    f.write(f'{last_updated} - LED value changed to: {curr_value}\n')
                    prev_value = curr_value

                # Break while loop if no updates for specified number of minutes
                if ((datetime.now() - last_updated).total_seconds() // 60.0) >= timeout:
                    print(f'No new data for {int(timeout)} minutes! Aborting program!')
                    break
            except asyncio.exceptions.CancelledError:  # Handle Keyboard Interrupt with CTRL+C
                break

    # On disconnect
    print(f'\n{device_name} disconnected!')
    print('Attempting to save log file...')

    # Save the log file
    try:
        f.close()
        print('Log file saved!')
    except:
        print('Error saving log file!')


asyncio.run(main())  # Run the main loop
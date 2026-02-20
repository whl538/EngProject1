"""
A simple Python script to troubleshoot BLE connectivity.
Displays the names of all BLE peripheral devices available.

Author: Luna Brooker
Date: 20th February 2026
"""

import asyncio
from bleak import BleakScanner

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        name = d.name
        if name:
            print(name)


asyncio.run(main())
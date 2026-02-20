# EngProject1
Programming Repository for Engineering Project 1 at the University of York - Team 14.

Programmed using an Arduino 33 Sense Rev2 microcontroller in Arduino C++ and Python.

**Dependencies:**
Bluetooth Interface: 
  - Python 3.14 or higher
  - Bleak
Arduino:
  - ArduinoBLE 1.5.0 or higher

**Instructions for use:**
- Connect the Arduino to power
- Install Python 3.14 or higher on your machine and navigate to the project folder
- Run `pip3 install bleak` in a terminal to install Bleak into your environment
- Navigate to `Bluetooth Connection (DO NOT UPLOAD TO BOARD)` and run `python3 connect.py` to start the Bluetooth interface
- When finished logging data, press CTRL+C on your keyboard to terminate the process. **(IMPORTANT: This must be done before disconnecting the Arduino)**
- Data will be saved to log.txt in the main folder of the directory.

**Version History:**
- V0.0.2 (Luna): Creates Bluetooth interface in Python for the microcontroller, as well as basic functionality on the Arduino to turn on and off an LED and log its state to a file on a remote system.
- V0.0.1 (Luna): Adds Test.ino and creates repo

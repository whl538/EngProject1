/**
 * Arduino Program to turn the builtin LED on and off and log this change to a remote server using Bluetooth Low Energy
 *
 * Author: Luna Brooker
 * Date: 20th Feb 2026
 *
 */

#include <ArduinoBLE.h>

// BLE Variables
const char* deviceServiceUuid = "19b10000-e8f2-537e-4f6c-d104768a1214";
const char* deviceServiceCharacteristicUuid = "19b10001-e8f2-537e-4f6c-d104768a1214";

BLEService ledService(deviceServiceUuid); 
BLEIntCharacteristic ledCharacteristic(deviceServiceCharacteristicUuid, BLERead | BLENotify);

// Global Variables
int state = 0;                                    // State of the LED
const char* device_name = "Arduino Nano 33 BLE";  // Bluetooth device name

// Magic Numbers
const int serial_baud_rate = 9600;  // Baud Rate of the serial monitor
const int flash_time = 2000;        // Total time between flashes (including response time) in msec
const int response_time = 750;      // Time between receiving instruction to change LED state and actual state change in msec


void setup() {
  Serial.begin(serial_baud_rate);  // Start the serial monitor
  while (!Serial);  
  
  // Initialise LEDs
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  
  digitalWrite(LEDR, HIGH);
  digitalWrite(LEDG, HIGH);
  digitalWrite(LEDB, HIGH);
  digitalWrite(LED_BUILTIN, LOW);

  
  // Start and setup BLE
  if (!BLE.begin()) {
    Serial.println("- Starting Bluetooth® Low Energy module failed!");
    while (1);
  }
  BLE.setLocalName(device_name); 
  BLE.setAdvertisedService(ledService);
  ledService.addCharacteristic(ledCharacteristic);
  BLE.addService(ledService);
  ledCharacteristic.writeValue(0);
  BLE.advertise();

  Serial.println("Nano 33 BLE (Peripheral Device)");
  Serial.println(" ");
    
}

void loop() {
  // Look for a central device
  BLEDevice central = BLE.central();
  Serial.println("- Discovering central device...");
  delay(500);

  if (central) {
    Serial.println("* Connected to central device!");
    Serial.print("* Device MAC address: ");  // Display central device's MAC address
    Serial.println(central.address());
    Serial.println(" ");

    while (central.connected()) {
      state = ledCharacteristic.value();  // Update the LED's state variable
      writeLED(!state);
    }
    
    Serial.println("* Disconnected from central device!");
  }
    
}

void writeLED(int param) {
  delay(flash_time - response_time);
  Serial.println("Characteristic <LED> has changed!");
  
  if (param == 0) {
    Serial.println("Turning LED off...");
  }
  else {
    Serial.println("Turning LED on...");
  }

  delay(response_time);
  digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  ledCharacteristic.writeValue(param);

}

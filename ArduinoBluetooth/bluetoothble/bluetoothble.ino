#include <ArduinoBLE.h>
BLEService sensorService("1101");
BLEUnsignedCharCharacteristic sensorLevelChar("2101", BLERead | BLENotify);

void setup() {
Serial.begin(9600);
while (!Serial);

pinMode(LED_BUILTIN, OUTPUT);
if (!BLE.begin()) 
{
Serial.println("starting BLE failed!");
while (1);
}

BLE.setLocalName("SensorMonitor");
BLE.setAdvertisedService(sensorService);
sensorService.addCharacteristic(sensorLevelChar);
BLE.addService(sensorService);

BLE.advertise();
Serial.println("Bluetooth device active, waiting for connections...");
}

void loop() 
{
BLEDevice central = BLE.central();

if (central) 
{
Serial.print("Connected to central: ");
Serial.println(central.address());
digitalWrite(LED_BUILTIN, HIGH);

while (central.connected()) {

      int sensor = analogRead(A0);
      int sensorLevel = map(sensor, 0, 1023, 0, 100);
      Serial.print("Sensor Level is: ");
      Serial.println(sensorLevel);
      sensorLevelChar.writeValue(sensorLevel);
      delay(1000);

}
}
digitalWrite(LED_BUILTIN, LOW);
Serial.print("Disconnected from central: ");
Serial.println(central.address());
}

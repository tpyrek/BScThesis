#include <Servo.h>
#include "convertReceivedData.h"
#include "storeReceivedData.h"
#include "readData.h"


//Servos pins definitions
enum{
   SERVO1_PIN = 1,
   SERVO2_PIN,
   SERVO3_PIN,
   SERVO4_PIN,
   SERVO5_PIN,
   SERVO6_PIN
};

//Maximum and minimum servo position(in degrees)
enum{
  MIN_SERVO_POSITION = 10,
  MAX_SERVO_POSITION = 170
};

// The table of the Servo class objects 
Servo servoObjectsTable[6];

// Object type StoreReceivedData which stores incoming data
StoreReceivedData dataStorage;

union {
    byte asBytes[4];
    int asInt;
} foo;

void setup() {
  
  // put your setup code here, to run once:

  // Serial baudrate = 9600
  Serial.begin(9600);
  Serial.println("Ready");

  // Attach servo on pin SERVOx_PIN to the servo object
  servoObjectsTable[0].attach(SERVO1_PIN);
  servoObjectsTable[1].attach(SERVO2_PIN);
  servoObjectsTable[2].attach(SERVO3_PIN);
  servoObjectsTable[3].attach(SERVO4_PIN);
  servoObjectsTable[4].attach(SERVO5_PIN);
  servoObjectsTable[5].attach(SERVO6_PIN);

}

void loop() {
  // put your main code here, to run repeatedly:

    if(Serial.available()>=32) {

     readIncomingData(dataStorage);
     
      //Serial.write(foo.asBytes[0]);
      //Serial.write(foo.asBytes[1]);
      //Serial.write(foo.asBytes[2]);
      //Serial.write(foo.asBytes[3]);
      Serial.println(dataStorage.minValue.asInt);
      Serial.println(dataStorage.maxValue.asInt);
      Serial.println(dataStorage.servo1Value.asInt);
      Serial.println(dataStorage.servo2Value.asInt);
      Serial.println(dataStorage.servo3Value.asInt);
      Serial.println(dataStorage.servo4Value.asInt);
      Serial.println(dataStorage.servo5Value.asInt);
      Serial.println(dataStorage.servo6Value.asInt);
    }
}

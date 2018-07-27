#include <Servo.h>
#include "convertReceivedData.h"
#include "storeReceivedData.h"
#include "readData.h"
#include "servoSetup.h"


//Servos pins definitions
enum{
   SERVO1_PIN = 4,
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

// Object type ConvertReceivedData which calculates and stores scale 
// used to converting incoming servo values into degrees 
ConvertReceivedData dataConverter;

// Object type ServoControl which sets servos in proper position in proper time interval
// (dependent on received speedValue param)
ServoSetup servosSetter(servoObjectsTable, &dataStorage);

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

  // Init servos at the beggining - set all servos on 50 degrees
  servosSetter.initServos();

}

void loop() {
  // put your main code here, to run repeatedly:

    if(Serial.available()>=42) {

     readIncomingData(dataStorage);
     dataConverter.setValues(dataStorage.minValue.asInt, dataStorage.maxValue.asInt);
     dataConverter.calculateScale(MIN_SERVO_POSITION, MAX_SERVO_POSITION);
     dataConverter.calculateServosValues(dataStorage);


     Serial.println(dataStorage.minValue.asInt);
     Serial.println(dataStorage.maxValue.asInt);
     Serial.println(dataStorage.speedValue.asInt);
     Serial.println(dataStorage.servo1Value.asInt);
     Serial.println(dataStorage.servo2Value.asInt);
     Serial.println(dataStorage.servo3Value.asInt);
     Serial.println(dataStorage.servo4Value.asInt);
     Serial.println(dataStorage.servo5Value.asInt);
     Serial.println(dataStorage.servo6Value.asInt);
     Serial.write(dataStorage.orderOfServosSetting[0]);
     Serial.write(dataStorage.orderOfServosSetting[1]);
     Serial.write(dataStorage.orderOfServosSetting[2]);
     Serial.write(dataStorage.orderOfServosSetting[3]);
     Serial.write(dataStorage.orderOfServosSetting[4]);
     Serial.write(dataStorage.orderOfServosSetting[5]);


     servosSetter.setServos(33);
    }
}

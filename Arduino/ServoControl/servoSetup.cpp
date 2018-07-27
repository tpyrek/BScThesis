#include "servoSetup.h"

ServoSetup::ServoSetup(Servo servoObj[], StoreReceivedData *storageObj)
{
  servoObjectsTable = servoObj;
  dataStorage = storageObj;
}

void ServoSetup::initServos()
{
  servoObjectsTable[0].write(50);
  servoObjectsTable[1].write(50);
  servoObjectsTable[2].write(50);
  servoObjectsTable[3].write(50);
  servoObjectsTable[4].write(50);
  servoObjectsTable[5].write(50);
}

void ServoSetup::setServos(int speedValue)
{
  // This temporary table enable dynamic changing the order of servos setting (order is in the incoming packet)
  temporaryServosData table[6];

  table[0].servoLastPosition = lastPositions.servo1LastPosition;
  table[0].servoNewPosition = (uint8_t)dataStorage->servo1Value.asInt;
  table[0].servoID = 0;

  table[1].servoLastPosition = lastPositions.servo2LastPosition;
  table[1].servoNewPosition = (uint8_t)dataStorage->servo2Value.asInt;
  table[1].servoID = 1;

  table[2].servoLastPosition = lastPositions.servo3LastPosition;
  table[2].servoNewPosition = (uint8_t)dataStorage->servo3Value.asInt;
  table[2].servoID = 2;

  table[3].servoLastPosition = lastPositions.servo4LastPosition;
  table[3].servoNewPosition = (uint8_t)dataStorage->servo4Value.asInt;
  table[3].servoID = 3;

  table[4].servoLastPosition = lastPositions.servo5LastPosition;
  table[4].servoNewPosition = (uint8_t)dataStorage->servo5Value.asInt;
  table[4].servoID = 4;

  table[5].servoLastPosition = lastPositions.servo6LastPosition;
  table[5].servoNewPosition = (uint8_t)dataStorage->servo6Value.asInt;
  table[5].servoID = 5;

  // minus 1 because of table indexes starting from 0
  shiftServo(table[dataStorage->orderOfServosSetting[0]-1]);
  shiftServo(table[dataStorage->orderOfServosSetting[1]-1]); 
  shiftServo(table[dataStorage->orderOfServosSetting[2]-1]);
  shiftServo(table[dataStorage->orderOfServosSetting[3]-1]);
  shiftServo(table[dataStorage->orderOfServosSetting[4]-1]);
  shiftServo(table[dataStorage->orderOfServosSetting[5]-1]); 

  // Remebmer servos settings
  lastPositions.servo1LastPosition = (uint8_t)dataStorage->servo1Value.asInt;
  lastPositions.servo2LastPosition = (uint8_t)dataStorage->servo2Value.asInt;
  lastPositions.servo3LastPosition = (uint8_t)dataStorage->servo3Value.asInt;
  lastPositions.servo4LastPosition = (uint8_t)dataStorage->servo4Value.asInt;
  lastPositions.servo5LastPosition = (uint8_t)dataStorage->servo5Value.asInt;
  lastPositions.servo6LastPosition = (uint8_t)dataStorage->servo6Value.asInt;
  
}

// servoID - servo index in the servoObjectsTable (1 less than serwo numeration because of table indexes starting from 0)
void ServoSetup::shiftServo(temporaryServosData &temp)
{
  if(temp.servoLastPosition > temp.servoNewPosition)
  {
    for(uint8_t i = temp.servoLastPosition; i >= temp.servoNewPosition; i--)
    {
      servoObjectsTable[temp.servoID].write(i);
      delay(5);
    }     
  }
  else if(temp.servoLastPosition < temp.servoNewPosition)
  {
    for(uint8_t i = temp.servoLastPosition; i <= temp.servoNewPosition; i++)
     {
      servoObjectsTable[temp.servoID].write(i);
      delay(5);
    }     
  }
  
}


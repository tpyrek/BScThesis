#include "servoSetup.h"

ServoSetup::ServoSetup(Servo servoObj[], StoreReceivedData *storageObj)
{
  servoObjectsTable = servoObj;
  dataStorage = storageObj;
  
  // Init servosDataTable
  for(int i = 0; i < 6; i++)
  {
    servosDataTable[i].servoLastPosition = 50;
  }
}

void ServoSetup::initServos()
{
  //Initial values
  servoObjectsTable[0].write(50);
  servoObjectsTable[1].write(50);
  servoObjectsTable[2].write(50);
  servoObjectsTable[3].write(50);
  servoObjectsTable[4].write(50);
  servoObjectsTable[5].write(50);
}

void ServoSetup::setServos()
{
  // Get new servos positions
  servosDataTable[0].servoNewPosition = (uint8_t)dataStorage->servo1Value.asInt;
  servosDataTable[1].servoNewPosition = (uint8_t)dataStorage->servo2Value.asInt;
  servosDataTable[2].servoNewPosition = (uint8_t)dataStorage->servo3Value.asInt;
  servosDataTable[3].servoNewPosition = (uint8_t)dataStorage->servo4Value.asInt;
  servosDataTable[4].servoNewPosition = (uint8_t)dataStorage->servo5Value.asInt;
  servosDataTable[5].servoNewPosition = (uint8_t)dataStorage->servo6Value.asInt;
  
  // Shift servos in accordance with the order sent in the incoming packet
  // minus 1 due to table's indexes starting from 0
  shiftServo(dataStorage->orderOfServosSetting[0]-1);
  shiftServo(dataStorage->orderOfServosSetting[1]-1); 
  shiftServo(dataStorage->orderOfServosSetting[2]-1);
  shiftServo(dataStorage->orderOfServosSetting[3]-1);
  shiftServo(dataStorage->orderOfServosSetting[4]-1);
  shiftServo(dataStorage->orderOfServosSetting[5]-1); 

  // Remember last servos positions  
  servosDataTable[0].servoLastPosition = (uint8_t)dataStorage->servo1Value.asInt;
  servosDataTable[1].servoLastPosition = (uint8_t)dataStorage->servo2Value.asInt;
  servosDataTable[2].servoLastPosition = (uint8_t)dataStorage->servo3Value.asInt;
  servosDataTable[3].servoLastPosition = (uint8_t)dataStorage->servo4Value.asInt;
  servosDataTable[4].servoLastPosition = (uint8_t)dataStorage->servo5Value.asInt;
  servosDataTable[5].servoLastPosition = (uint8_t)dataStorage->servo6Value.asInt;
  
}

// servoID - servo index in the servoObjectsTable (1 less than servo numeration because of table indexes starting from 0)
void ServoSetup::shiftServo(uint8_t servoID)
{
  // In incoming packet speedValue determines the delay of shifting the servo by one degree in ms
  int speedValue = dataStorage->speedValue.asInt;
  
  if(servosDataTable[servoID].servoLastPosition > servosDataTable[servoID].servoNewPosition)
  {
    for(uint8_t i = servosDataTable[servoID].servoLastPosition; i >= servosDataTable[servoID].servoNewPosition; i--)
    {
      servoObjectsTable[servoID].write(i);
      delay(speedValue); //convert to us
    }     
  }
  else if(servosDataTable[servoID].servoLastPosition < servosDataTable[servoID].servoNewPosition)
  {
    for(uint8_t i = servosDataTable[servoID].servoLastPosition; i <= servosDataTable[servoID].servoNewPosition; i++)
     {
      servoObjectsTable[servoID].write(i);
      delay(speedValue); //convert to us
    }     
  }
  
}


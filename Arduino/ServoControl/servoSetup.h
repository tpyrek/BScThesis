#ifndef SERVO_SETUP_H
#define SERVO_SETUP_H

#include <Arduino.h>
#include <Servo.h>
#include "storeReceivedData.h"

// Stores servos last position, new position got from StoreReceivedData object
typedef struct{
  uint8_t servoLastPosition;
  uint8_t servoNewPosition;
}servosData;


class ServoSetup
{
private:

  StoreReceivedData *dataStorage;
  Servo *servoObjectsTable;
  servosData servosDataTable[6];

  void shiftServo(uint8_t servoID);
  
public:

  ServoSetup(Servo servoObj[], StoreReceivedData *storageObj);
  void setServos();
  void initServos();
  
};


#endif //SERVO_SETUP_H

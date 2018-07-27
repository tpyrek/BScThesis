#ifndef SERVO_SETUP_H
#define SERVO_SETUP_H

#include <Arduino.h>
#include <Servo.h>
#include "storeReceivedData.h"

// Stores last servos positions in degrees
typedef struct{
  uint8_t servo1LastPosition;
  uint8_t servo2LastPosition;
  uint8_t servo3LastPosition;
  uint8_t servo4LastPosition;
  uint8_t servo5LastPosition;
  uint8_t servo6LastPosition;
}servosPositions;

typedef struct{
  uint8_t servoLastPosition;
  uint8_t servoNewPosition;
  uint8_t servoID;
}temporaryServosData;


class ServoSetup
{
private:

  servosPositions lastPositions{50,50,50,50,50,50};
  StoreReceivedData *dataStorage;
  Servo *servoObjectsTable;

  void shiftServo(temporaryServosData &temp);
  
public:

  ServoSetup(Servo servoObj[], StoreReceivedData *storageObj);
  void setServos(int speedValue);
  void initServos();
  
};


#endif //SERVO_SETUP_H

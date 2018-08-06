#include "readData.h"

// Packet structure:
// minVaue maxValue speedValue servo1Value servo2Value servo3Value servo4Value servo5Value servo6Value firstServo secondServo thirdServo fourthServo fifthServo sixthServo     
// 4 bytes 4 bytes    4bytes     4 bytes     4 bytes     4bytes      4 bytes     4 bytes     4 bytes     1 byte     1 byte      1 byte      1 byte     1 byte     1 byte
void readIncomingData(StoreReceivedData &dataStorage)
{

  // Read minimum value from received packet (4 bytes)
  for (int i = 0; i < 4; i++) {
    dataStorage.minValue.asBytes[i] = Serial.read(); 
  }

  // Read maximum value from received packet (4 bytes)
  for (int i = 0; i < 4; i++) {
    dataStorage.maxValue.asBytes[i] = Serial.read(); 
  }

  // Read speed value from received packet (4 bytes)
  for (int i = 0; i < 4; i++) {
    dataStorage.speedValue.asBytes[i] = Serial.read(); 
  }

  // Read servo 1 value from received packet (4 bytes)
  for (int i = 0; i < 4; i++) {
    dataStorage.servo1Value.asBytes[i] = Serial.read(); 
  }

  // Read servo 2 value from received packet (4 bytes)
  for (int i = 0; i < 4; i++) {
    dataStorage.servo2Value.asBytes[i] = Serial.read(); 
  }

  // Read servo 3 value from received packet (4 bytes)
  for (int i = 0; i < 4; i++) {
    dataStorage.servo3Value.asBytes[i] = Serial.read(); 
  }

  // Read servo 4 value from received packet (4 bytes)
  for (int i = 0; i < 4; i++) {
    dataStorage.servo4Value.asBytes[i] = Serial.read(); 
  }

  // Read servo 5 value from received packet (4 bytes)
  for (int i = 0; i < 4; i++) {
    dataStorage.servo5Value.asBytes[i] = Serial.read(); 
  }

  // Read servo 6 value from received packet (4 bytes)
  for (int i = 0; i < 4; i++) {
    dataStorage.servo6Value.asBytes[i] = Serial.read(); 
  }
  
  // Read the order of the servos setting from received packet (6 bytes)
  for (int i = 0; i < 6; i++) {
    dataStorage.orderOfServosSetting[i] = Serial.read(); 
  }

}

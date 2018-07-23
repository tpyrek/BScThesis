#include "readData.h"


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
  
}

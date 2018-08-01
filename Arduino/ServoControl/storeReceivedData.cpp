#include "storeReceivedData.h"

// Check if received values are correct
bool StoreReceivedData::dataCorrect()
{
  
  if(minValue.asInt >= maxValue.asInt)
    return false;

  if(minValue.asInt < 0 || maxValue.asInt < 0)
    return false;

  if(speedValue.asInt < 0)
    return false;

  if(servo1Value.asInt > maxValue.asInt || servo1Value.asInt < minValue.asInt)
    return false;

  if(servo2Value.asInt > maxValue.asInt || servo2Value.asInt < minValue.asInt)
    return false;

  if(servo3Value.asInt > maxValue.asInt || servo3Value.asInt < minValue.asInt)
    return false;

  if(servo4Value.asInt > maxValue.asInt || servo4Value.asInt < minValue.asInt)
    return false;

  if(servo5Value.asInt > maxValue.asInt || servo5Value.asInt < minValue.asInt)
    return false;

  if(servo6Value.asInt > maxValue.asInt || servo6Value.asInt < minValue.asInt)
    return false;

  for(int i = 0; i < 6; i++)
  {
    if(orderOfServosSetting[i] > 6 || orderOfServosSetting[i] < 1)
      return false;
  }

  // Check if there are two identical values in the table
  for(int i = 0; i < 5; i++)
  {
    for(int j = (i+1); j < 6; j++)
    {
      if(orderOfServosSetting[i] == orderOfServosSetting[j])
        return false;
    }
  }

  // If all data are correct
  return true;
  
}


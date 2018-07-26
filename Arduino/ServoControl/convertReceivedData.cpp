#include "convertReceivedData.h"

ConvertReceivedData::ConvertReceivedData()
{
	minValue = 0;
	maxValue = 0;
	scale = 0;
}

void ConvertReceivedData::setValues(int _min, int _max)
{
  minValue = _min;
	maxValue = _max;
}

void ConvertReceivedData::calculateScale(int minServoPosition, int maxServoPosition)
{
  /*
  if(minValue<0)
  {
    //if received minValue is negative(range e.g. -1000:1000) convert range to natural numbers(e.g. 0:2000)
    
    maxValue += abs(minValue);
    minValue = abs(minValue);
    
  }
  */
  
	int servoRange = maxServoPosition - minServoPosition;
  int valueRange = maxValue - minValue;
  
  // x degree = 1 value
  scale = (float)servoRange/(float)valueRange;
  
}

void ConvertReceivedData::calculateServosValues(StoreReceivedData &dataStorage)
{
  dataStorage.servo1Value.asInt = round(dataStorage.servo1Value.asInt * scale);
  dataStorage.servo2Value.asInt = round(dataStorage.servo2Value.asInt * scale);
  dataStorage.servo3Value.asInt = round(dataStorage.servo3Value.asInt * scale);
  dataStorage.servo4Value.asInt = round(dataStorage.servo4Value.asInt * scale);
  dataStorage.servo5Value.asInt = round(dataStorage.servo5Value.asInt * scale);
  dataStorage.servo6Value.asInt = round(dataStorage.servo6Value.asInt * scale);
}


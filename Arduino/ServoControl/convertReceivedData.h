#ifndef CONVERT_RECEIVED_DATA_H
#define CONVERT_RECEIVED_DATA_H

#include <Arduino.h>
#include "storeReceivedData.h"

//This class stores received maximum servo's angle
class ConvertReceivedData
{
private:
  int minValue;
  int maxValue;
	float scale;  

public:
	
	ConvertReceivedData();
  
  void setValues(int _min, int _max);
	
	void calculateScale(int minServoPosition, int maxServoPosition);
  void calculateServosValues(StoreReceivedData &dataStorage);

};

#endif //CONVERT_RECEIVED_DATA_H

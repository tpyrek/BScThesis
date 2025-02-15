#ifndef STORE_RECEIVED_DATA_H
#define STORE_RECEIVED_DATA_H

#include <Arduino.h>

typedef union{
		byte	asBytes[4];
		int		asInt;
	}receivedData;

class StoreReceivedData{

public:

	receivedData minValue;
	receivedData maxValue;
  receivedData speedValue;
	receivedData servo1Value;
	receivedData servo2Value;
	receivedData servo3Value;
	receivedData servo4Value;
	receivedData servo5Value;
	receivedData servo6Value;
  uint8_t orderOfServosSetting[6];

  bool dataCorrect();

};

#endif //STORE_RECEIVED_DATA_H

#pragma once
#include "Serial.h"
#include "string"
using namespace std;

class arduinoiox
{
private:
	Serial* SP;
public:

	arduinoiox();
	~arduinoiox();
	arduinoiox(char* portName, int BaudRate, int TIME_OUT, int ARDUINO_WAIT_TIME);
	void open(char* portName, int BaudRate, int  TIME_OUT, int ARDUINO_WAIT_TIME);
	int senddata(char* sendString);
	int receivedata(char* receiveData, int rb);
};
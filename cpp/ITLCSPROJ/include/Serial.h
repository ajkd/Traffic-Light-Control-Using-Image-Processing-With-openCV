#pragma once

#include <windows.h>
#include <iostream>

using namespace std;


class Serial
{
private:
	HANDLE hSerial;
	bool connected;
	COMSTAT status;
	DWORD errors;

public:
	Serial(string portName, int BaudRate, int TIME_OUT, int ARDUINO_WAIT_TIME);
	~Serial();
	int ReadData(char* buffer, unsigned int nbChar);
	int WriteData(const char* buffer, unsigned int nbChar);
	bool IsConnected();
};


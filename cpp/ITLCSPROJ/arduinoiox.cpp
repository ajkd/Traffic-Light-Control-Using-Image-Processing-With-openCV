#include "arduinoiox.h"
using namespace std;


arduinoiox::arduinoiox() {}

arduinoiox::~arduinoiox() {}

arduinoiox::arduinoiox(char* portName, int BaudRate, int TIME_OUT, int ARDUINO_WAIT_TIME)
{
	SP = new Serial(portName, BaudRate, TIME_OUT, ARDUINO_WAIT_TIME);
}

void arduinoiox::open(char* portName, int BaudRate, int TIME_OUT, int ARDUINO_WAIT_TIME)
{
	SP = new Serial(portName, BaudRate, TIME_OUT, ARDUINO_WAIT_TIME);
}

int arduinoiox::senddata(char* sendString) {
	int i = -1;
	if (SP->IsConnected()) {
		unsigned int l = (int)strlen(sendString);
		i = SP->WriteData(sendString, l);
	}
	else
		cout << "Not connected\n";
	return i;

}
int arduinoiox::receivedata(char* receiveData, int rb) {
	int len = -1;
	string x = "";
	if (SP->IsConnected()) {
		len = 0;
		while (true)
		{
			char incomingData[512] = "";
			int readResult = SP->ReadData(incomingData, sizeof(incomingData));
			if (readResult > 0) {
				incomingData[readResult] = 0;
				if (incomingData[readResult - 1] == '\n')
				{
					len += readResult;
					x = x + string(incomingData);
					break;
				}
				else
				{
					len += readResult;
					x = x + string(incomingData);
				}
			}

		}
	}
	else
		x = "#Error - Not connected\n";
	strcpy_s(receiveData, rb, x.c_str());
	return len;

}


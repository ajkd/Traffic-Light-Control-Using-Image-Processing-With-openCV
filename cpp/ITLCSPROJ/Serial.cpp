#include "Serial.h"
#include "atlstr.h"
using namespace std;

Serial::Serial(string portName, int BaudRate, int TIME_OUT, int ARDUINO_WAIT_TIME)
{
	//We're not yet connected
	this->connected = false;
	CString PortSpecifier = portName.c_str();
	//Try to connect to the given port throuh CreateFile
	this->hSerial = CreateFile(PortSpecifier,
		GENERIC_READ | GENERIC_WRITE,
		0,
		NULL,
		OPEN_EXISTING,
		FILE_ATTRIBUTE_NORMAL,
		NULL);

	//Check if the connection was successfull
	if (this->hSerial == INVALID_HANDLE_VALUE)
	{
		//If not success full display an Error
		if (GetLastError() == ERROR_FILE_NOT_FOUND)
		{
			//Print Error if neccessary
			cout << "ERROR When Openning Serial Port - Handle was not attached. Reason: not available. - " << portName;

		}
		else
		{
			cout << "ERROR When Openning Serial Port - " << portName;
		}

	}
	else
	{
		//If connected we try to set the comm parameters
		DCB dcbSerialParams = { 0 };
		//Try to get the current
		if (!GetCommState(this->hSerial, &dcbSerialParams))
		{
			//If impossible, show an error
			printf("failed to get current serial parameters!");
		}
		else
		{
			//Define serial connection parameters for the arduino board
			dcbSerialParams.BaudRate = BaudRate;
			dcbSerialParams.ByteSize = 8;
			dcbSerialParams.StopBits = ONESTOPBIT;
			dcbSerialParams.Parity = NOPARITY;
			//Setting the DTR to Control_Enable ensures that the Arduino is properly
			//reset upon establishing a connection
			dcbSerialParams.fDtrControl = DTR_CONTROL_ENABLE;

			//Set the parameters and check for their proper application
			if (!SetCommState(hSerial, &dcbSerialParams))
			{
				printf("ALERT: Could not set Serial Port parameters");
			}
			else
			{
				//If everything went fine we're connected
				this->connected = true;
				//Flush any remaining characters in the buffers 
				PurgeComm(this->hSerial, PURGE_RXCLEAR | PURGE_TXCLEAR);
				//We wait 2s as the arduino board will be reseting
				Sleep(ARDUINO_WAIT_TIME);
			}
		}
	}

}

Serial::~Serial()
{
	//Check if we are connected before trying to disconnect
	if (this->connected)
	{
		//We're no longer connected
		this->connected = false;
		//Close the serial handler
		CloseHandle(this->hSerial);
	}
}

int Serial::ReadData(char* buffer, unsigned int nbChar )
{
	//Number of bytes we'll have read
	DWORD bytesRead = -1;
	//Number of bytes we'll really ask to read
	unsigned int toRead;
	//Use the ClearCommError function to get status info on the Serial port
	ClearCommError(this->hSerial, &this->errors, &this->status);
	//Check if there is something to read
	if (this->status.cbInQue > 0)
	{
		//If there is we check if there is enough data to read the required number
		//of characters, if not we'll read only the available characters to prevent
		//locking of the application.
		if (this->status.cbInQue > nbChar)
		{
			toRead = nbChar;
		}
		else
		{
			toRead = this->status.cbInQue;
		}

		//Try to read the require number of chars, and return the number of read bytes on success
		ReadFile(this->hSerial, buffer, toRead, &bytesRead, NULL);


	}
	//If nothing has been read, or that an error was detected return 0
	return bytesRead;
}

int Serial::WriteData(const char* buffer, unsigned int nbChar)
{
	DWORD bytesSend = -1;

	//Try to write the buffer on the Serial port
	if (!WriteFile(this->hSerial, (void*)buffer, nbChar, &bytesSend, 0))
	{
		//In case it don't work get comm error and return false
		ClearCommError(this->hSerial, &this->errors, &this->status);
	}
	else
	return bytesSend;
}

bool Serial::IsConnected()
{
	//Simply return the connection status
	return this->connected;

}

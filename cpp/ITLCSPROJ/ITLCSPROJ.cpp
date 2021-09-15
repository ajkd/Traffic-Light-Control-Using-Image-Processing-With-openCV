// ITLCSPROJ.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#include "string"
#include <iostream>
#include "string"
#include "arduinoiox.h"
#include "chkcam.h"
#include "tlcmain.h"
#include <opencv2/core/utility.hpp>
using namespace cv;
using namespace std;



int main(int argc, char** argv)
{

	const string keys =
		"{sit||System Initialization Table Id - to activate tlc system}"
		"{cid||Cam Id ( number ) - to check Cam ( ex. 0 )}"
		"{file||file name - to check cam capture data}"
		"{sid||Analog pin Id ( String ) - analog pin id of the Arudino Board where analog sensor to be checked connected to  ( ex. A0 )}"
		"{lid||Digital pin Id ( Number ) - Digital pin id of the Arudino Board where led to be checked connected to  ( ex. 2 )}"
		"{port|COM1|port ( String ) - this is needed for arudino related checkings, Serial port ( ex. COM1 ) arudino board connected to this system}";

	cv::CommandLineParser parser(argc, argv, keys);
	parser.about("One of the sit, camid, sid parameters must be specified");

	if (parser.has("sit"))
	{
				string sit = parser.get<string>("sit");
				tlcmain cm;
				cm.prcs(&sit[0]);
	}
	else
		if (parser.has("cid"))
		{
						chkcam cc;
						string fl = parser.get<string>("file");
						cc.dimg(parser.get<int>("cid"), &fl[0] );
		}
		else
			if (parser.has("sid") || parser.has("lid"))
				if (parser.has("port"))
				{
					string cp = parser.get<string>("port");
					string s1 = "";
					if (parser.has("sid"))
					{
						string sid = parser.get<string>("sid");
						s1 = "#1#" + sid + ",1,50,#\n";
					}
					else
					{
						string lid = parser.get<string>("lid");
						s1 = "#0#" + lid + ",B,0,1000,3000,#\n";
					}
					arduinoiox card = arduinoiox(&cp[0], 9600, 30, 2000);
				
					while (true)
					{
						int i = card.senddata(&s1[0]);
						cout << "Serial Write : " << i << endl;
						if (i >= 0)
						{
							char incomingData[512];
							i = card.receivedata(&incomingData[0], 512);
							cout << "Serial Read : " << i << "  " << incomingData << endl;
						}
						else
							break;
						Sleep(10);
					}
					return 0;
				}
				else
					parser.printMessage();

			else
				parser.printMessage();
	return 0;
}






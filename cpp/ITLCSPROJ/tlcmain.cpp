
#include <fstream>
#include <iostream>
#include <vector>
#include <time.h> 
#include <ctime>
#include <chrono>
#include "string"
#include "tlcmain.h"
#include "arduinoiox.h"
#include <map>
using namespace std;
#include "nlohmann/json.hpp"
using json = nlohmann::json;
#include "opencv2/opencv.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"
using namespace cv;



map<string, json> mlx;
map<string, arduinoiox*> mard;
map<string,Mat> framea;
map<string, VideoCapture*> capa;
vector<string> vm;
vector<string> vp;

void start();
int prcscam(int maxt, char* debug, json* parms);
int prcssensor(int maxt, char* debug, json* parms);
void onofftl(json js);
int getio(json* vmj, int ctmaxt);
int getprty(json* prty);

tlcmain::tlcmain() {};
tlcmain::~tlcmain() {};

void tlcmain::prcs(char* sit) {

	ifstream insit(sit);
	if (!insit)
	{
		cout << "ERROR - Cannot open the File : " << sit << endl;
		exit(EXIT_FAILURE);
	}
	json jsit;
	insit >> jsit;
	insit.close();

	string vmfn = jsit["videom"];
	ifstream invm(vmfn.c_str());
	if (!invm)
	{
		cout << "ERROR - Cannot open the File : " << vmfn << endl;
		exit(EXIT_FAILURE);
	}
	string str;
	while (getline(invm, str)) {
		if (str.size() > 0)
			vm.push_back(str);
	}
	invm.close();

	string vpfn = jsit["videop"];
	ifstream invp(vpfn.c_str());
	if (!invp)
	{
		cout << "ERROR - Cannot open the File : " << vpfn << endl;
		exit(EXIT_FAILURE);
	}
	while (getline(invp, str))
	{
		if (str.size() > 0)
			vp.push_back(str);
	}
	invp.close();

	json arc = jsit["comps"];
	for (auto& el : arc.items())
	{
		string port = el.value()[0];
		int br = el.value()[1];
		int to = el.value()[2]*1000;
		int slt = el.value()[3]*1000;
		arduinoiox* ardx = new arduinoiox(&port[0], br, to, slt);
		mard[ el.key()] = ardx;
	}

	string tlcfn = jsit["tlc"];
	ifstream intlc(tlcfn.c_str());
	if (!intlc)
	{
		cout << "ERROR - Cannot open the File : " << tlcfn << endl;
		exit(EXIT_FAILURE);
	}
	json jtlc;
	intlc >> jtlc;
	intlc.close();
	for (json::iterator it = jtlc.begin(); it != jtlc.end(); ++it) {
		string lane = (*it)["lane"].dump();
		if (lane.compare("99") == 0)
		{
			for (auto& el : (*it)["red"].items()) {
				json js = el.value();
				onofftl(js);
			}
		}
		else
		{
			json r = (*it)["red"];
			json g = (*it)["green"];
			mlx["lr" + lane] = r;
			mlx["lg" + lane] = g;
		}
	}
	start();
}

void start()
{
	map<string, int> skip;
	skip["dummy"] = 0;

	int i = 0;
	while (true) {
		json vmj = json::parse(vm.at(i));
		int lane = vmj["lane"].get<int>();

		map<string, int>::iterator it;
		it = skip.find("l" + to_string(lane));
		if (it == skip.end())
		  skip["l" + to_string(lane)] = vmj["skipc"].get<int>();
		if (skip.find("l" + to_string(lane))->second > 0)
		{
	        skip["l" + to_string(lane)] -= skip["l" + to_string(lane)];
			i++;
			if (i == vm.size())
				i = 0;
			continue;
		}

		cout << "Processing Lane - " << lane << endl;
		skip["l" + to_string(lane)] = vmj["skipc"].get<int>();
		string debug = vmj["debug"];
		if (getio(&vmj, 0) > 0) {
			json js = mlx["lg" + to_string(lane)];
			for (auto& el : js.items()) {
				json js1 = el.value();
				onofftl(js1);
			}
			int j = 0;
			while (true) {
				int mt = vmj["maxt"].get<int>();
				try {
					json prty = vmj["prtyid"];
					mt = mt + getprty(&prty);
				}
				catch (const exception& e) {}
				if (getio(&vmj, mt) > 0) {
					j = i + 1;
					if (j == vm.size())
						j = 0;
					bool f = false;
					while (true) {
						json vmj1 = json::parse(vm.at(j));
						if (getio(&vmj1, 0) > 0) {
							json js = mlx["lr" + to_string(lane)];
							for (auto& el : js.items()) {
								json js1 = el.value();
								onofftl(js1);
							}
							i = j;
							f = true;
							break;
						}
						else
						{
							j++;
							if (j == vm.size())
								j = 0;
							if (j == i)
								break;
						}
					}
					if (f)
						break;
				}
				else
				{
					json js = mlx["lr" + to_string(lane)];
					for (auto& el : js.items()) {
						json js1 = el.value();
						onofftl(js1);
					}
					i++;
					break;
				}
			}
		}
		else
			i++;
		if (i == vm.size())
			i = 0;
	}
}


int getprty(json* js) {
	int r = 0;
	for (auto& el : (*js).items()) {
		string p = el.value();
		for (int i = 0; i < vp.size(); i++)
		{
			json jp = json::parse(vp.at(i));
			if (p.compare(jp["prtyid"]) == 0)
			{
				int mt = jp["maxt"].get<int>();
				if (getio(&jp, mt) > 0)
				{
					r = jp["pt"].get<int>();
					break;
				}
			}
		}
		if (r > 0)
			break;
	}
	return r;
}

int getio(json* vmj, int mt) {
	string type = (*vmj)["type"];
	string debug = (*vmj)["debug"];
	json parms = (*vmj)["parms"].get<json>();
	int rv;
	if (type[0] == 'c')
	{
		rv = prcscam(mt, &debug[0], &parms);
		if (debug[0] == 'Y')
			cout << "Cam Output - " << parms["camid"] << " - " << rv << endl;
	}
	else
	{
		rv = prcssensor(mt, &debug[0], &parms);
		if (debug[0] == 'Y')
			cout << "Sensor Output - " << parms["sensor"] << " - " << rv << endl;
	}
	return rv;
}

int prcscam(int maxt, char* debug, json* parms)
{
	int cam = (*parms)["cam"].get<int>();
	string camid = (*parms)["camid"];
	string camtype = (*parms)["camtype"];
	int viewcam = (*parms)["viewcam"].get<int>();
	int rdelay = (*parms)["rdelay"].get<int>();
	int rtime = (*parms)["rtime"].get<int>();
	int	mincarea = (*parms)["mincarea"].get<int>();
	int	maxcarea = (*parms)["maxcarea"].get<int>();
	json arc = (*parms)["detectarea"].get<json>();
	int sx = arc[0];
	int sy = arc[1];
	int sw = arc[2];
	int sh = arc[3];

	VideoCapture* cap;
	Mat frame1;

	map<string, VideoCapture*>::iterator it;
	it = capa.find("cap" + camid);
	if (it != capa.end())
	{
 	  cap = capa.find("cap" + camid)->second;
	  frame1 = framea.find("frame" + camid)->second;
    }
	else
	{
	  cap = new VideoCapture(cam);
	  capa["cap" + camid] = cap;
	  if (cap->isOpened())
	  {
 	    cap->read(frame1);
		framea["frame" + camid] = frame1;
	  }
	  else
	  {
		  cv::destroyAllWindows();
		  cap->release();
		  cout << "ERROR - Openning Camera - " << camid << endl;
		  return -1;
	  }
	}
	
	int	noc = 0;
	int	r = 0;
	time_t st;
	time(&st);

	for (;;)
	{
		time_t st1;
		time(&st1);
		++noc;
		int nof = 0;
		bool OK = false;
		for (;;)
		{
			time_t st2;
			time(&st2);
			if (st2 - st1 > rtime)
				break;

			Mat src, fgMask, thresh;
			cap->read(src);
			++nof;
			Mat frame2 = src.clone();
			cv::absdiff(frame1, frame2, fgMask);
			cv::cvtColor(fgMask, fgMask, cv::COLOR_BGR2GRAY);
			cv::threshold(fgMask, thresh, 50, 255, cv::THRESH_BINARY);
			cv::rectangle(src,
				Point(sx, sy),
				Point(sx + sw, sy + sh),
				Scalar(0, 255, 255),
				2);
			vector<vector<Point> > conts;
			cv::findContours(thresh, conts, cv::RETR_LIST, cv::CHAIN_APPROX_SIMPLE);
			for (size_t i = 0; i < conts.size(); i++)
			{
				double ca = cv::contourArea(conts[i]);
				if ((mincarea > 0 and ca < mincarea) || (maxcarea > 0 and ca > maxcarea))
					continue;
				Rect r = cv::boundingRect(conts[i]);
				bool OOK = false;
				if ((r.x > sx) && ((r.x + r.width) < (sx + sw)))
					OOK = true;

				if (OOK)
				{
					OOK = false;
					if ((r.y > sy) && (r.y < (sy + sh)))
						OOK = true;
					else
						if ((r.y < sy) && ((r.y + r.height) > sy))
							OOK = true;
				}
				if (OOK)
				{
					cv::rectangle(src, Point(r.x, r.y),
						Point(r.x + r.width, r.y + r.height), Scalar(0, 255, 0), 2);
					OK = true;

				}
			}
			if (viewcam > 0)
			{
				cv::imshow("CAM" + camid, src);
				if (waitKey(30) >= 0)
					break;
			}

			if (OK)
			{
				if (debug[0] == 'Y')
 	 			  cout << "Cycle No - " << noc << "  Frame No - " << nof << " Object/s Detected"<<endl;
				break;
			}
			else
				if (debug[0] == 'Y')
					cout << "Cycle No - " << noc << "  Frame No - " << nof << " Object/s Not Detected"<<endl;
			Sleep(rdelay);
		}

		if (OK)
		{
				time_t st3;
				time(&st3);
				if (st3 - st > maxt)
				{
					r = 1;
					break;
				}
		}
		else
	 	  break;
		
	}
	return r;
}

int prcssensor(int maxt, char* debug, json* parms)
{
	string sensor = (*parms)["sensor"];
	string sensorid = (*parms)["sensorid"];
	int rdelay = (*parms)["rdelay"].get<int>();
	int rtime = (*parms)["rtime"].get<int>();
	int srtm = (*parms)["srtm"].get<int>();
	string comport = (*parms)["comport"];

	arduinoiox* card = mard.find(comport)->second;
	int	cc = 0;
	int	r = 0;
	time_t st;
	time(&st);
	while (true)
	{
		cc++;
		string sr = "#1#" + sensor + "," + to_string(rdelay) + "," + to_string(rtime) + "," +
			        to_string(srtm) + ",#\n";
		int i = card->senddata(&sr[0]);
		if (debug[0] == 'Y')
			cout << "Send To Sensor - " << sensor << " - Cycle " << cc << " - " << i <<
			" - " << sr << endl;
		if (i >= 0)
		{
			char incomingData[1024];
			i = card->receivedata(&incomingData[0],1024);
			if (i > 0)
			{
				if (debug[0] == 'Y')
					cout << "Read From Sensor - \"" << sensor << "\" - Cycle " << cc 
					<< " - " << incomingData << endl;
				if (incomingData[0] == '#')
				{
					if (incomingData[1] == '0')
						break;
				}
				else
				  cout << "ERROR - Invalid Message Read From Sensor - " << sensor << endl;
			}
			else
			  cout << "ERROR - No Data Read From Sensor - " << sensor << endl;
		}
		else
			cout << "ERROR - Get From Sensor - \"" << sensor << "\" Failed" << endl;
		time_t ct;
		time(&ct);
		double diff = ct - st;
		if (diff > maxt)
		{
			r = 1;
			break;
		}
	}
	return r;
}

void onofftl(json js) 
{
	int i = 0;
	String bid = "";
	String s = "";
	for (auto& el : js.items() )
	{
		if (i == 0)
			bid = el.value();
		else
		{
			json tlr = el.value();
			int j = 0;
			for (auto& el1 : tlr.items())
			{   
				if (j == 1)
					s = s + tlr[j].get<string>() + ",";
				else
					s = s + to_string(tlr[j].get<int>()) + ",";
				j++;
			}
			s = s + "#";
		}
		i++;
	}
	s = "#0#" + s + "\n";
	arduinoiox* card = mard.find(bid)->second;
	i = card->senddata(&s[0]);
	if (i >= 0)
	{
		char incomingData[256];
		i = card->receivedata(&incomingData[0], 256);
	}
}

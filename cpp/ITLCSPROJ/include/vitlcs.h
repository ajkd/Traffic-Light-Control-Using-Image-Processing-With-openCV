#pragma once

const int t_width = 30;
const int t_height = 30;
const int t_space = 50;
const int t_x = 0;
const int t_y = 15;
const int t_r = 10;
const int max_items = 5;

#include <windows.h>
#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <fstream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include "nlohmann/json.hpp"
using json = nlohmann::json;
using namespace cv;
using namespace std;


class vitlcs {

private:
	map < string, string > tmap;
	Mat image;
	Scalar df = Scalar(0, 0, 0);
	Scalar wbg = Scalar(220, 220, 220);
	Scalar tbg = Scalar(128, 128, 128);
	Scalar off = Scalar(169, 169, 169);
	map < string, cv::Scalar> lc = { {"R",Scalar(0,0,255)}, {"Y",Scalar(0,255,255)}, {"G",Scalar(0,128,0)} };
public:
	vitlcs();
	~vitlcs();
	string createtl(json tlr);
	string onoff(json tlr);

};


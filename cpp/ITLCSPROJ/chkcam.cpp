#include <iostream>
#include "chkcam.h"
#include "opencv2/opencv.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"
using namespace std;
using namespace cv;

	chkcam::chkcam() {}

	chkcam::~chkcam() {}

	int chkcam::dimg(int camid)
	{

		int sx = 90;
		int	sy = 290;
		int sw = 425;
		int sh = 130;

		int mincarea = 1400;
		int maxcarea = 20000;

		VideoCapture cap(camid); // open the default camera
		if (!cap.isOpened())  // check if we succeeded
			return -1;
		Mat frame1;
		cap >> frame1;
		for (;;)
		{
			Mat src, fgMask, thresh;
			cap >> src;  
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
				bool OK = false;
				if ((r.x > sx) && ((r.x + r.width) < (sx + sw)))
					OK = true;

				if (OK)
				{
					OK = false;
					if ((r.y > sy) && (r.y < (sy + sh)))
						OK = true;
					else
						if ((r.y < sy) && ((r.y + r.height) > sy))
							OK = true;
				}
				if (OK)
					cv::rectangle(src, Point(r.x, r.y), Point(r.x + r.width, r.y + r.height), Scalar(0, 255, 0), 2);
			}
			cv::imshow("Contours", src);
			if (waitKey(30) >= 0) break;
		}
		cv::destroyAllWindows();
		cap.release();
		return 0;
	}

#include "vitlcs.h"

map < string, cv::Scalar> lc;

vitlcs::vitlcs() {}

vitlcs::~vitlcs() {}

string vitlcs::createtl(json tlr)
{
	String o = "";
	int l = tlr.size() * t_width * 3 + t_space * (tlr.size() + 1);
	image = Mat(t_height * 2, l, CV_8UC3, wbg );
	int x = t_x;
	for (auto& el : tlr.items())
	{
		json js = el.value();
		int i = 0;
		x += t_space;

		cv::putText(
			image,
			"Lane - " + to_string(js[0]),
			Point(x, t_y - 5),
			FONT_HERSHEY_COMPLEX_SMALL,
			.6,
			Scalar(0, 0, 0), 1,
			cv::LINE_AA, false);

		while (i < js[1].size())
		{
			cv::rectangle(image, Point(x, t_y), Point(x + t_width, t_y + t_height), tbg, FILLED);
			circle(image, Point(x + t_width / 2, t_y + t_height / 2), t_r, off, FILLED, 2);
			string lidr = js[1][i];
			int ix = lidr.find("-");
			String tlc = lidr.substr(0, ix);
			String tlid = lidr.substr(++ix, lidr.size());
			tmap["x#" + tlid] = to_string(x + t_width / 2);
			tmap["y#" + tlid] = to_string(t_y + t_height / 2);
			tmap["c#" + tlid] = tlc;
			x += t_width;
			i++;
		}

	}

	imshow("Traffic Light Display Window", image);
	if (waitKey(30) >= 0) return " ";
	return o;
}

string vitlcs::onoff(json js)
{
	String o = "";
	int i = 0;
	String bid = "";
	String s = "";
	for (auto& el : js.items())
	{
		if (i == 0)
			bid = el.value();
		else
		{
			json tlr = el.value();
			int j = 0;
			string s[max_items];
			for (auto& el1 : tlr.items())
			{
				if (j == 1)
					s[j] = tlr[j].get<string>();
				else
					s[j] = to_string(tlr[j].get<int>());
				j++;
			}

			string sx = "x#" + s[0];
			string sy = "y#" + s[0];

			if (s[1].at(0) == 'O')
			{
				String sc = tmap["c#" + s[0]];
				circle(image,
					Point(stoi(tmap[sx]), stoi(tmap[sy])), t_r, lc[sc], FILLED, 2);
				imshow("Traffic Light Display Window", image);
				if (waitKey(30) >= 0)
					break;
				Sleep(stoi(s[2]));
			}
			else
				if (s[1].at(0) == 'F')
				{
					circle(image, Point(stoi(tmap[sx]), stoi(tmap[sy])), t_r, off, FILLED, 2);
					imshow("Traffic Light Display Window", image);
					if (waitKey(30) >= 0)
						break;
					Sleep(stoi(s[2]));
				}
				else
					if (s[1].at(0) == 'B')
					{
						time_t st1;
						time(&st1);
						String sc = tmap["c#" + s[0]];
						while (true)
						{
							circle(image,
								Point(stoi(tmap[sx]), stoi(tmap[sy])), t_r, lc[sc], FILLED, 2);
							imshow("Traffic Light Display Window", image);
							if (waitKey(30) >= 0)
								break;
							Sleep(stoi(s[3]));
							circle(image,
								Point(stoi(tmap[sx]), stoi(tmap[sy])), t_r, off, FILLED, 2);
							imshow("Traffic Light Display Window", image);
							if (waitKey(30) >= 0)
								break;
							Sleep(stoi(s[3]));

							time_t st3;
							time(&st3);

							if ((st3 - st1) * 1000 > stoi(s[4]))
								break;
						}
						Sleep(stoi(s[2]));
					}
					else
						o = "#Invalid Function Code";

		}
		i++;
	}

	return o;
}

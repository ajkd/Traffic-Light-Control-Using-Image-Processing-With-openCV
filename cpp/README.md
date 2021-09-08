## Trafic Light Control Using Image Processing With openCV 

ITLCSPROJ binary is generated using microsoft visual studio 2019 for windows 10 home for X64

#### To generate application from source 
 - download JSON for Modern C++  https://github.com/nlohmann/json and include its include folder to your project
 - download opencv https://github.com/opencv/opencv/releases/tag/4.2.0 and extract pre-built library 
   - include opencv include folder to your project ( \opencv\build\include )
   - add opencv lib to your project library refrence list ( \opencv\build\x64\vc15\lib )
   - link opencv lib to your project ( \opencv_world420d.lib )
   - add opencv bin folder to pathc (\opencv\build\x64\vc15\bin )
   - refer article  https://subwaymatch.medium.com/adding-opencv-4-2-0-to-visual-studio-2019-project-in-windows-using-pre-built-binaries-93a851ed6141 to install opencv in visual studio

### Run application
  - ITLCSPROJ --sit=sit1.txt  --> test four lane traffic
  - ITLCSPROJ --sit=sit2.txt  --> test three lane traffic with pedestraian crossing
  
  
### Check componenets
   - check cam  --> ITLCSPROJ --cid=0 --file=chkcam.txt
   - check sensor --> ITLCSPROJ --port=com3 --sid=A0
   - check led --> ITLCSPROJ --port=com3 --lid=2 

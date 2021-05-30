# Reactive-library-Tello-EDU-Arnouts-Jarne

This repository contains a reactive library for controlling a DJI Tello EDU drone written in python using RxPY. 
It further contains an application implementing the functionality of this library as an example of t's usage. 
the implementation uses fragments of the SDK realeased by the original manufacturer, this SDK can be found here. 
For any questions relation to operating the drone that are not answered here, please refer to the documention of the original SKD.

# Installation
For installation of the necessary dependencies, please use the install.bat file that correspnds to your system. If these do not work please refer to the manual installation that follows, taken from the documentation of the original SDK. This is for windows only:

a: install a python version, this SDk was originally made in Python 2.7 but was adapted to 3.8, please use 3.8 or higher. For all steps using the

b.Then you can install these four dependencies through pip, ('way to install pip' please google by yourself)
   numpy,opencv-python,pillow,matplotib。The installation instructions are:
   numpy:           python -m pip install numpy
   matplotlib:      python -m pip install matplotlib
   opencv-python:   python -m pip install -v opencv-python==3.4.2.17
   pillow:          python -m pip install pillow
   
c.Next, you need to download and install boost in order to get a dynamic link library called boost_python27-vc120-mt-x**-1_68.dll
   boost download link:
   win64: https://nchc.dl.sourceforge.net/project/boost/boost-binaries/1.68.0/boost_1_68_0-msvc-12.0-64.exe 
   win32: https://excellmedia.dl.sourceforge.net/project/boost/boost-binaries/1.68.0/boost_1_68_0-msvc-12.0-32.exe  
   After the download is complete, double-click the installation package to install. After the installation is complete, find the 
   boost_python27-vc120-mt-x**-1_68.dll file (the '**' depends on the number of your windows system) and place it in 
   .\Python27\Lib\site-packages path.
   
d.Next, you need to download ffmpeg, the purpose is to get multiple dll files including avcodec-58.dll,etc.
   ffmpeg download link:
   win64: https://ffmpeg.zeranoe.com/builds/win64/shared/ffmpeg-20180825-844ff49-win64-shared.zip
   win32: https://ffmpeg.zeranoe.com/builds/win32/shared/ffmpeg-20180825-844ff49-win32-shared.zip
   After the download is complete, extract the files,enter ./bin directory and place all the .dll files under the .\Python27\Lib\site-packages path.
   
e.Next, you need to download the vs2013 compiler.
   vs2013 compiler download link：
   win64: https://download.microsoft.com/download/2/E/6/2E61CFA4-993B-4DD4-91DA-3737CD5CD6E3/vcredist_x64.exe
   win32: https://download.microsoft.com/download/2/E/6/2E61CFA4-993B-4DD4-91DA-3737CD5CD6E3/vcredist_x86.exe
   After the download is complete, run the installation package and install.
   
f.Finally Copy the libh264decoder from the Tello-Python package to the .\Python27\Lib\site-packages directory.
   h264decoder.pyd path: (adapt this path for your python 3.8 or above path) 
   win64: .\Tello-Python\Tello_Video\h264decoder\Windows\x64\libh264decoder.pyd
   win32: .\Tello-Python\Tello_Video\h264decoder\Windows\x86\libh264decoder.pyd
   
 For any problems with the installation of these files, please once again refer to the documentaion of the original SDk. Detailed explanations are available there. 
   
To start the application, run the BasicApplication class in the BasicApplication.py file in the main directory. Before running, please make sure to give the ip adress of your device as the "local_ip" parameter to the drone, as well as giving a portnumber as "local_port". This way the connection to the drone can be made. 
  

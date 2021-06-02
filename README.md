# Reactive-library-Tello-EDU-Arnouts-Jarne

This repository contains a reactive library for controlling a DJI Tello EDU drone written in python and using RxPY. It further contains an application implementing the functionality of this library as an example of t's usage created in Tkinter. the implementation uses fragments of an official SDK realeased by the original manufacturer: Ryzen robotics, this SDK can be found here: https://github.com/dji-sdk/Tello-Python. For any questions relation to operating the drone that are not answered here, please refer to the documention of the original SKD.

#Installation
There are a rather large amount of dependencies that must be installed before being able to use the complete functionality of the library. The original SDK uses installation scripts to install these dependencies. These have again been included in this repositroy but since these were for Python 2.7 and this project uses Python 3.8, the scripts might not work properly. Below, a series of instructions for windows 10 are placed. There is no such thing for OSx and Linux, as this library was written without acces to either of these available. 

a.Install a python version of 3.8 or higher. A virtual python environment can also be used. 

b.Install these four dependencies through pip: 
numpy
opencv-python
pillow
matplotib

The installation instructions are: 
numpy: python -m pip install numpy 
matplotlib: python -m pip install matplotlib 
opencv-python: python -m pip install -v opencv-python==3.4.2.17 
pillow: python -m pip install pillow

c.Next, unzip the tello_video_ddl zip file. This contains files necessary for running this project. First run the application vcredist_x64.exe. Next, copy all the remaining files to the \lib\site-packages filder of your python installation. This is only for windows. 

d.To run the actual application, first run the bat file "getModels.bat" in the file "official_sdk_files/model/". Then open the BasicApplication file and run it. It will automatically start the application GUI. 

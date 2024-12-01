This file is mainly used to provide background services such as face recognition, comparison, and sound playback to support the user interface in the set_web.py.
set_web.py
    This file uses the Streamlit library, a Python library for creating data applications. The main features of the file include:

1. Page configuration: Set the layout of the application to "wide" to make the page wider.
2. Face library management: Provides an interface for managing face libraries, including functions such as uploading files, creating new folders, deleting folders, and renaming folders.
3. Real-time detection: It provides face detection functions in real-time video streams, including face comparison, alarm sound playback and other functions.
4. Console: Provides a console interface for setting and configuring various parameters, such as camera ID, detection interval, split region, etc.
    This file is primarily used to create an application that integrates face library management, real-time detection, and console functionality.

service.py
1. This file mainly contains the service functions that are used with the set_web.py file. The main features of the file include:
2. Face recognition: Use OpenCV and face_recognition libraries for face recognition and detection.
3. Face comparison: Compare the detected face with the known face database to identify whether it is a known person.
4. Sound playback: It can play the preset warning sound.

To use both programs, you need to first make sure that they are properly installed and configured in your environment. Here are the general steps to guide you on how to use both programs:
Install and configure the environment
Install Streamlit: If you don't already have Streamlit installed, you can install it via pip.

***pip install streamlit***

Install additional dependencies: Depending on the dependencies in the set_web.py and service.py files, you may need to install additional libraries such as face_recognition and simpleaudio.
Profiles: Both programs use some profiles, such as camera ID, detection interval, split region, etc. You'll need to create these profiles and set the appropriate parameters.
Use set_web.py
Run the application: Run the set_web.py file on the command line.

***streamlit run set_web.py***

Face Gallery Management: In the left sidebar of the app, you can see the "Face Gallery Management" option. Click on it and you can upload new face pictures, manage folders and files.
Real-time detection: In the left sidebar of the app, click on the "Real-time detection" option, and you will enter the live video streaming interface. Here, you can do face comparison and set alarm sounds.
Console: In the left sidebar of the app, tap on the "Console" option and you will be taken to the console interface. Here, you can configure and set various parameters.
Use service.py
Background service: service.py is a background service program that needs to run continuously to provide face recognition and comparison capabilities. You can use a service management tool (e.g., systemd, supervisord, etc.) to start and stop the service.
Monitor video streams: When the service.py is running, it continuously monitors the video stream and takes appropriate actions when it detects faces.
Please note that both programs need to be appropriately configured and adapted to your specific needs. Also, make sure that you have all the required libraries and dependencies installed in your environment. If you run into any problems, you can refer to the official documentation for Streamlit and OpenCV, as well as the code notes for both programs, for more help and guidance.

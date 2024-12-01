***Face-detector***

### `set_web.py`
这个文件使用了Streamlit库，一个用于创建数据应用程序的Python库。文件的主要功能包括：
1. **页面配置**：设置了应用程序的布局为“wide”，使得页面更宽。
2. **人脸库管理**：提供了一个界面，用于管理人脸库，包括上传文件、新建文件夹、删除文件夹和重命名文件夹等功能。
3. **实时检测**：提供了实时视频流中的人脸检测功能，包括人脸比对、警报声音播放等功能。
4. **控制台**：提供了一个控制台界面，用于设置和配置各种参数，如摄像头ID、检测间隔、分割区域等。
这个文件主要用于创建一个集成了人脸库管理、实时检测和控制台功能的应用程序。
### `service.py`
这个文件主要包含了与`set_web.py`文件配合使用的服务功能。文件的主要功能包括：
1. **人脸识别**：使用OpenCV和face_recognition库进行人脸识别和检测。
2. **人脸比对**：将检测到的人脸与已知人脸库进行比对，以识别是否为已知人物。
3. **声音播放**：能够播放预设的警示声音。
4. **主循环**：包含了应用程序的主循环，负责持续监控视频流，检测人脸，并与人脸库进行比对。
这个文件主要用于提供后台服务，如人脸识别、比对和声音播放等功能，以支持`set_web.py`中的用户界面。
这两个文件结合使用，可以创建一个功能丰富的人脸识别和监控系统。

要使用这两个程序，您需要先确保它们在您的环境中正确安装和配置。以下是一般步骤，用于指导您如何使用这两个程序：
安装和配置环境
安装Streamlit：如果尚未安装Streamlit，您可以通过pip进行安装。
pip install streamlit
安装其他依赖：根据set_web.py和service.py文件中的依赖项，您可能需要安装额外的库，例如face_recognition和simpleaudio。
配置文件：两个程序都使用了一些配置文件，如摄像头ID、检测间隔、分割区域等。您需要创建这些配置文件，并设置相应的参数。
使用set_web.py
运行应用程序：在命令行中运行set_web.py文件。
streamlit run set_web.py
人脸库管理：在应用程序的左侧栏中，您可以看到“人脸库管理”选项。点击它，您可以上传新的人脸图片，管理文件夹和文件。
实时检测：在应用程序的左侧栏中，点击“实时检测”选项，您将进入实时视频流界面。在这里，您可以进行人脸比对和设置警报声音。
控制台：在应用程序的左侧栏中，点击“控制台”选项，您将进入控制台界面。在这里，您可以配置和设置各种参数。
使用service.py
后台服务：service.py是一个后台服务程序，它需要持续运行以提供人脸识别和比对功能。您可以使用一个服务管理工具（如systemd、supervisord等）来启动和停止这个服务。
监控视频流：当service.py运行时，它会持续监控视频流，并在检测到人脸时执行相应的操作。
请注意，这两个程序需要根据您的具体需求进行适当的配置和调整。此外，确保您的环境中已经安装了所有必需的库和依赖项。如果您遇到任何问题，可以参考Streamlit和OpenCV的官方文档，以及这两个程序的代码注释，以获取更多帮助和指导。


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

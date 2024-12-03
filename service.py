import numpy as np
import cv2
import json
import time
import os
import io
from datetime import datetime
from PIL import Image
try:
    print(time.time(),"尝试导入face_recognition")
    import face_recognition
    print(time.time(),"成功导入face_recognition")
except:
    print(time.time(),"无法导入face_recognition")
ls_t = 0
try:
    print(time.time(),"尝试导入simpleaudio")
    import simpleaudio as sa
    print(time.time(),"成功导入simpleaudio")
    
except:
    print(time.time(),"无法导入simpleaudio")
try:
    print(time.time(),"尝试导入warning.wav")
    wave_warning = sa.WaveObject.from_wave_file("warning.wav")
    print(time.time(),"成功导入warning.wav")
except:
    print(time.time(),"无法导入warning.wav")
try:
    print(time.time(),"尝试导入warning2.wav")
    wave_warning2 = sa.WaveObject.from_wave_file("warning2.wav")
    print(time.time(),"成功导入warning2.wav")
except:
    print(time.time(),"无法导入warning2.wav")
# 读取配置文件
def read_config(file_path):
    print(time.time(),'读取配置文件：' + file_path)
    with open(file_path, 'r') as file:
        return json.load(file)

# 检查当前时间是否在指定时间段内
def is_time_in_interval(intervals):
    print(time.time(),'检查当前时间是否在指定时间段内')
    now_hour = datetime.now().hour
    now_minute = datetime.now().minute
    now = now_hour * 60 + now_minute
    for interval in intervals:
        start, end = interval
        start = start[0] * 60 + start[1]
        end = end[0] * 60 + end[1]
        if start <= now <= end:
            return True
    return False
# 人脸比对
def getFaceEncoding(src):
    image = src
    face_locations = face_recognition.face_locations(image)
    img_  = image[face_locations[0][0]:face_locations[0][2],face_locations[0][3]:face_locations[0][1]]#人脸范围
    face_encoding = face_recognition.face_encodings(image, face_locations)[0]
    return face_encoding
def simcos(A,B):
    A=np.array(A)
    B=np.array(B)
    dist = np.linalg.norm(A - B) # 二范数
    sim = 1.0 / (1.0 + dist) #
    return np.square(sim)
def face_comparison(src1,FaceEncoding):
    xl1=getFaceEncoding(src1)
    xl2=FaceEncoding
    face_distances = face_recognition.face_distance([xl1], xl2)
    value=simcos(xl1,xl2)
    return value
# 播放警示音
def play_alert_sound():
    print(time.time(),'播放警示音')
    try:
        play_obj = wave_warning.play()
        play_obj.wait_done()
    except:
        print(time.time(),"无法播放警示音")
def play_alert2_sound():
    print(time.time(),'播放警示音2')
    try:
        play_obj = wave_warning2.play()
        play_obj.wait_done()
    except:
        print(time.time(),"无法播放警示音2")
# 检测人脸
def detect_faces(image, polygon_points,scaleFactor=1.05, minNeighbors=10,minSize=(30,30),maxSize=(500,500)):
    global ls_t
    print(time.time(),'检测人脸')
    s_t = time.time()
    # 创建掩码
    mask = np.zeros_like(image)
    cv2.fillConvexPoly(mask, np.array(polygon_points), (255, 255, 255))
    masked_image = cv2.bitwise_and(image, mask)
    # # 保存图片
    # cv2.imwrite('masked_image.jpg', masked_image)
    # 加载人脸识别模型
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # masked_image = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(masked_image, scaleFactor, minNeighbors,maxSize=maxSize,minSize=minSize)
    print(time.time(),"检测结束，用时:",round(time.time()-s_t,3),'秒，检测人脸数',len(faces))
    if os.path.exists(".faces"):
        ls_t = time.time()
        dict_faces = {}
        n = 0
        for (x, y, w, h) in faces:
            dict_faces[str(n)] = [int(x),int(y), int(w), int(h)]
            # 截取图片为face_image
            face_image = masked_image[x-int(w*0.5):x+int(w*1.5), y-int(h*0.5):y+int(h*1.5)]
            if is_enable_faces_comparison:
                compare_value = compare_faces(face_image)
                if compare_value != None:
                    dict_faces[str(n)].append(compare_value[0])
                    dict_faces[str(n)].append(compare_value[1])
                else:
                    dict_faces[str(n)].append("")
                    dict_faces[str(n)].append("")
            else:
                dict_faces[str(n)].append("dis")
                dict_faces[str(n)].append("dis")
            n += 1
        with open("faces.json", "w") as file:
            json.dump(dict_faces, file)
        os.remove(".faces")
    if os.path.exists(".spend_time"):
        ls_t = time.time()
        with open("spend_time.txt", "w") as file:
            file.write(str(round(time.time()-s_t,3)))
        os.remove(".spend_time")
    return faces
def compare_faces(Frame):
    global faces_library
    print(time.time(),'比对人脸')
    s_t = time.time()
    ls_dir = os.listdir("faces")
    ls_dir.sort()
    max_v = 0
    name = 0
    if len(ls_dir) == 0:
        print(time.time(),'没有可比对的人脸')
        return
    else:
        for face_key in faces_library:
            try:
                v = face_comparison(Frame,faces_library[face_key])
                if max_v < v:
                    max_v = v
                    name = face_key
            except:
                print(time.time(),"比对人脸","faces"+"\\"+face_key,"失败")
        print(time.time(),"比对人脸结束，用时:",round(time.time()-s_t,3),'秒，姓名:',name,' 相似度:',max_v)
        return [max_v, name]
is_enable_faces_comparison = False
faces_library = {}
# 主循环
def main_loop():
    global ls_t, is_enable_faces_comparison,faces_library
    faces = []
    with open("camera.txt") as file:
        camera_id = int(file.read())
    with open("wait.txt") as file:
        wait_time = int(file.read())
    with open("detection_interval.txt") as file:
        text = file.read()
        if "." in text:
            detection_interval = float(text)
        else:
            detection_interval = int(text)
    intervals = read_config("intervals.json")
    polygon_points = read_config("split.json")
    polygon_points2 = []
    for point in polygon_points:
        polygon_points2.append([int(polygon_points[point]["x"]),int(polygon_points[point]["y"])])
    polygon_points = polygon_points2
    face_size_limits = read_config("l.json")
    scaleFactor_minNeighbors = read_config("scaleFactor_minNeighbors.json")
    scaleFactor = scaleFactor_minNeighbors["scaleFactor"]
    minNeighbors = scaleFactor_minNeighbors["minNeighbors"]
    with open("enable_faces_comparison.txt","r") as file:
        is_enable_faces_comparison = eval(file.read())
    if os.path.exists("comparison_threshold.txt"):
        with open("comparison_threshold.txt","r") as file:
            threshold = float(file.read())
    else:
        threshold = 0.7
    faces_library = {}
    ls_face_library = os.listdir("faces")
    print(time.time(),"开始人脸库编码, 共",len(ls_face_library),"个:")
    for i in ls_face_library:
        s_t3 = time.time()
        faces_library[i] = getFaceEncoding(np.array(Image.open("faces"+"\\"+i)))
        print(time.time(),"    编码 faces\\"+i+"，耗时:",time.time()-s_t3,"秒")
    cap = cv2.VideoCapture(camera_id)
    time.sleep(2)
    while True:
        if is_time_in_interval(intervals):
            ret, frame = cap.read()
            if not ret:
                print(time.time(),"摄像头读取失败，等待5秒后重试")
                s_t2 = time.time()
                while time.time()-s_t2<5:
                    if os.path.exists(".show"):
                        break
                    if os.path.exists(".change"):
                        break
                    time.sleep(0.5)
                cap.release()
                cap = cv2.VideoCapture(camera_id)
                continue
            if time.time() - ls_t >10:
                faces = detect_faces(frame, polygon_points,scaleFactor, minNeighbors,minSize=(face_size_limits["min"],face_size_limits["min"]),maxSize=(face_size_limits["max"],face_size_limits["max"]))
                for (x, y, w, h) in faces:
                    if face_size_limits["min"] <= max(w, h) <= face_size_limits["max"]:
                        print(time.time(),"检测到符合标准的人脸,释放摄像头")
                        cap.release()
                        if is_enable_faces_comparison:
                            compare_value = compare_faces(frame[x-int(w*0.5):x+int(w*1.5), y-int(h*0.5):y+int(h*1.5)])
                            if not compare_value == None:
                                if compare_value[0] >= threshold:
                                    print(time.time(),compare_value[1],"比对成功")
                                    if not os.path.exists(".show"):
                                        play_alert2_sound()
                                else:
                                    if not os.path.exists(".show"):
                                        play_alert_sound()
                            else:
                                if not os.path.exists(".show"):
                                    play_alert_sound()
                        else:
                            if not os.path.exists(".show"):
                                play_alert_sound()
                        s_t2 = time.time()
                        while time.time()-s_t2<wait_time:
                            if os.path.exists(".show"):
                                break
                            if os.path.exists(".change"):
                                break
                        time.sleep(0.5)
                        cap = cv2.VideoCapture(camera_id)
                        break
            if os.path.exists(".show"):
                ls_t = time.time()
                ret, frame = cap.read()
                if not ret:
                    print(time.time(),"摄像头读取失败")
                    os.remove(".show")
                    continue
                faces = detect_faces(frame, polygon_points,scaleFactor, minNeighbors,minSize=(face_size_limits["min"],face_size_limits["min"]),maxSize=(face_size_limits["max"],face_size_limits["max"]))
                #将图片保存到本地
                show = frame.copy()
                #绘制多边形
                for point in polygon_points:
                    cv2.circle(show, point, 5, (0, 0, 255), -1)
                    #绘制多边形
                    cv2.polylines(show, [np.array(polygon_points)], True, (0, 255, 0), 2)
                #绘制人脸边框
                for (x, y, w, h) in faces:
                    #判断人脸大小是否在限制范围内
                    if face_size_limits["min"] <= max(w, h) <= face_size_limits["max"]:
                        cv2.putText(show, str(w)+","+str(h), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                        cv2.rectangle(show, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    else:
                        cv2.putText(show, str(w)+","+str(h), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                        cv2.rectangle(show, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.imwrite('frame.jpg', show)
                os.remove(".show")
            time.sleep(detection_interval)
        else:
            s_t2 = time.time()
            while time.time()-s_t2<30:
                if os.path.exists(".show"):
                    break
                if os.path.exists(".change"):
                    break
                time.sleep(0.5)
            try:cap.release()
            except:pass
            print(time.time(),"不在时间段内,释放摄像头")
        #判断设置文件是否更改
        if os.path.exists(".change"):
            ls_t = time.time()
            print(time.time(),"检测到设置文件更改命令，重新读取配置文件")
            with open("camera.txt") as file:
                camera_id = int(file.read())
            with open("wait.txt") as file:
                wait_time = int(file.read())
            with open("detection_interval.txt") as file:
                text = file.read()
                if "." in text:
                    detection_interval = float(text)
                else:
                    detection_interval = int(text)
            intervals = read_config("intervals.json")
            polygon_points = read_config("split.json")
            polygon_points2 = []
            for point in polygon_points:
                polygon_points2.append([int(polygon_points[point]["x"]),int(polygon_points[point]["y"])])
            polygon_points = polygon_points2
            face_size_limits = read_config("l.json")
            scaleFactor_minNeighbors = read_config("scaleFactor_minNeighbors.json")
            scaleFactor = scaleFactor_minNeighbors["scaleFactor"]
            minNeighbors = scaleFactor_minNeighbors["minNeighbors"]
            with open("enable_faces_comparison.txt","r") as file:
                is_enable_faces_comparison = eval(file.read())
            if os.path.exists("comparison_threshold.txt"):
                with open("comparison_threshold.txt","r") as file:
                    threshold = float(file.read())
            else:
                threshold = 0.7
            faces_library = {}
            ls_face_library = os.listdir("faces")
            print(time.time(),"开始人脸库编码, 共",len(ls_face_library),"个:")
            for i in ls_face_library:
                s_t3 = time.time()
                faces_library[i] = getFaceEncoding(np.array(Image.open("faces"+"\\"+i)))
                print(time.time(),"    编码 faces\\"+i+"，耗时:",time.time()-s_t3,"秒")
            try:
                cap.release()
            except:
                pass
            time.sleep(2)
            cap = cv2.VideoCapture(camera_id)
            try:
                print(time.time(),"尝试导入warning.wav")
                wave_warning = sa.WaveObject.from_wave_file("warning.wav")
                print(time.time(),"成功导入warning.wav")
            except:
                print(time.time(),"无法导入warning.wav")
            os.remove(".change")


main_loop()
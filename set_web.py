import streamlit as st
import os
import time
import json
import pandas as pd
import shutil

def read_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
st.set_page_config(layout="wide")
if st.session_state.get("restart") == True:
    with st.spinner("正在等待配置应用..."):
        s_t_4 = time.time()
        while True:
            time.sleep(0.01)
            if time.time() - s_t_4 > 10 and (not os.path.exists(".change")):
                st.error("配置应用超时，请重试")
                break
            elif not os.path.exists(".change"):
                st.info("配置应用成功")
                break
    st.session_state["restart"] = False
    st.rerun()
else:
    if st.session_state.get("face_library_management") == True:
        st.title(":blue[人脸库管理]")
        if st.sidebar.button("返回"):
            st.session_state["face_library_management"] = False
            st.rerun()
        else:
            is_rerun = False
            datadir = "faces"
            def get_folder_structure(root_folder):
                # 初始化结果字典
                result = {}
                path = root_folder
                listdir = os.listdir(root_folder)
                for f in listdir:
                    if os.path.isdir(os.path.join(path, f)):
                        result[f] = get_folder_structure(os.path.join(path, f))
                        # 递归调用

                    else:
                        result[f] = None
                        # 文件路径
                return result
            def select_file(data_tree,path=".",n=0):
                list_data_tree = list(data_tree.keys())
                list_data_tree.insert(0,".")
                selected_file = st.sidebar.selectbox(" ", list_data_tree,key="file_select_"+str(n))
                if selected_file == ".":
                    return path
                elif data_tree[selected_file] == None:
                    return path+os.sep+selected_file
                elif data_tree[selected_file] == {}:
                    return path+os.sep+selected_file
                else:
                    return select_file(data_tree[selected_file],path+os.sep+selected_file,n=n+1)
            def is_dir(path,data_tree):
                path = path.split(os.sep)
                path.pop(0)
                last = ""
                while len(path)>0:
                    if not path[0] == None:
                        if path[0] in list(data_tree.keys()):
                            data_tree = data_tree[path[0]]
                            last = path[0]
                            path.pop(0)
                        else:
                            return False
                    else:
                        return False
                if data_tree == None:
                    return False
                else:
                    return True
            data_dir = datadir
            data_tree = get_folder_structure(data_dir)
            select_file_or_dir = select_file(data_tree)
            select_file_or_dir_abs = select_file_or_dir.replace(".",data_dir,1)
            if is_dir(select_file_or_dir,data_tree):
                if select_file_or_dir != ".":
                    st.info(select_file_or_dir.replace(os.sep," > "))
                    file_upload_tab,new_dir_tab,delete_file_tab,rename_dir_tab = st.tabs(["上传文件","新建文件夹","删除文件夹","重命名文件夹"])
                    with file_upload_tab:
                        is_overwrite = st.checkbox("覆盖已有文件",key="is_overwrite")
                        upload_file = st.file_uploader("上传文件",key="upload_file",accept_multiple_files=True)
                        if upload_file:
                            if st.button("上传",key="upload_file_button"):
                                with st.spinner("上传中..."):
                                    for file in upload_file:
                                        if is_overwrite:
                                            with open(select_file_or_dir_abs+os.sep+file.name,"wb") as f:
                                                f.write(file.read())
                                            st.success(file.name+ " 上传成功")
                                        else:
                                            if os.path.exists(select_file_or_dir_abs+os.sep+file.name):
                                                st.warning(file.name+ " 已存在")
                                            else:
                                                with open(select_file_or_dir_abs+os.sep+file.name,"wb") as f:
                                                    f.write(file.read())
                                                st.success(file.name+ " 上传成功")
                                upload_file = None
                                st.info("上传完成")
                                is_rerun = True
                            else:
                                st.success("请点击上传按钮以上传文件")
                        else:
                            st.success("请选择文件")

                    with new_dir_tab:
                        new_dir_name = st.text_input("请输入文件夹名称",key="new_dir_name")
                        if new_dir_name != "":
                            new_dir = st.button("新建文件夹",key="new_folder")
                            if new_dir:
                                not_in_name = ["\\","/",">","<",":","*","?","\"","|"]
                                can_be_name = True
                                for i in not_in_name:
                                    if i in new_dir_name:
                                        can_be_name = False
                                if can_be_name:
                                    if os.path.exists(select_file_or_dir_abs+os.sep+new_dir_name):
                                        st.warning("文件夹已存在, 新建文件夹失败")
                                    else:
                                        os.mkdir(select_file_or_dir_abs+os.sep+new_dir_name)
                                        st.info("新建文件夹成功")
                                        is_rerun = True
                                else:
                                    st.warning("文件夹名称不合法")
                                new_dir = False
                            else:
                                st.success("请点击新建文件夹按钮以新建文件夹")
                        else:
                            st.success("请输入文件夹名称")

                    with delete_file_tab:
                        delete_file = st.button("删除文件夹",key="delete_dir")
                        if delete_file:
                            if os.path.isdir(select_file_or_dir_abs):
                                shutil.rmtree(select_file_or_dir_abs)
                                st.info("删除文件夹成功")
                                is_rerun = True
                            else:
                                st.warning("删除文件夹失败")
                            delete_file = False
                    with rename_dir_tab:
                        new_dir_name = st.text_input("请输入更名后的文件夹名称",key="rename_dir_name")
                        if new_dir_name != "":
                            rename_dir = st.button("重命名文件夹",key="rename_folder")
                            if rename_dir:
                                not_in_name = ["\\","/",">","<",":","*","?","\"","|"]
                                if os.path.isdir(select_file_or_dir_abs):
                                    can_be_name = True
                                    for i in not_in_name:
                                        if i in new_dir_name:
                                            can_be_name = False
                                    if can_be_name:
                                        renamed = (os.sep).join(select_file_or_dir_abs.split(os.sep)[:-1])+os.sep+new_dir_name
                                        print(renamed)
                                        if os.path.exists(renamed):
                                            st.warning("文件夹已存在")
                                        else:
                                            os.rename(select_file_or_dir_abs,renamed)
                                            st.info("重命名文件夹成功")
                                            is_rerun = True
                                    else:
                                        st.warning("文件夹名称不合法")
                                else:
                                    st.warning("重命名文件夹失败")
                                rename_dir = False
                            else:
                                st.success("请点击重命名文件夹按钮以重命名文件夹")
                        else:
                            st.success("请输入文件夹名称")
                else:
                    st.info(select_file_or_dir.replace(os.sep," > "))
                    file_upload_tab, = st.tabs(["上传文件"])
                    with file_upload_tab:
                        is_overwrite = st.checkbox("覆盖已有文件",key="is_overwrite2")
                        upload_file = st.file_uploader("上传文件",key="upload_file2",accept_multiple_files=True)
                        if upload_file:
                            if st.button("上传",key="upload_file_button"):
                                with st.spinner("上传中..."):
                                    for file in upload_file:
                                        if is_overwrite:
                                            with open(select_file_or_dir_abs+os.sep+file.name,"wb") as f:
                                                f.write(file.read())
                                            st.success(file.name+ " 上传成功")
                                        else:
                                            if os.path.exists(select_file_or_dir_abs+os.sep+file.name):
                                                st.warning(file.name+ " 已存在")
                                            else:
                                                with open(select_file_or_dir_abs+os.sep+file.name,"wb") as f:
                                                    f.write(file.read())
                                                st.success(file.name+ " 上传成功")
                                upload_file = None
                                st.info("上传完成")
                                is_rerun = True
                            else:
                                st.success("请点击上传按钮以上传文件")
                        else:
                            st.success("请选择文件")

            else:
                st.info(select_file_or_dir.replace(os.sep," > "))
                with st.expander("查看文件"):
                    if st.checkbox("显示文件内容",key="show_file_content"):
                        # 如果文件大小小于100M，则显示文件内容
                        if os.path.getsize(select_file_or_dir_abs) < 100*1024*1024:
                            if select_file_or_dir_abs.endswith(".txt"):
                                with open(select_file_or_dir_abs,"r",encoding="utf-8") as f:
                                    st.text(f.read())
                            elif select_file_or_dir_abs.endswith(".jpg"):
                                st.image(select_file_or_dir_abs)
                            elif select_file_or_dir_abs.endswith(".png"):
                                st.image(select_file_or_dir_abs)
                            elif select_file_or_dir_abs.endswith(".gif"):
                                st.image(select_file_or_dir_abs)
                            elif select_file_or_dir_abs.endswith(".mp4"):
                                st.video(select_file_or_dir_abs)
                            elif select_file_or_dir_abs.endswith(".mp3"):
                                st.audio(select_file_or_dir_abs,format="audio/mp3")
                            elif select_file_or_dir_abs.endswith(".wav"):
                                st.audio(select_file_or_dir_abs,format="audio/wav")
                            else:
                                st.warning("无法显示文件内容")
                        else:
                            st.warning("文件过大，无法显示文件内容")
                download,rename_dir_tab,delete_file_tab = st.tabs(["下载文件","重命名文件","删除文件"])
                with download:
                    if st.checkbox("创建下载链接",key="download_link"):
                        with open(select_file_or_dir_abs,"rb") as f:
                            st.download_button(label="下载文件",data=f,file_name=select_file_or_dir.split(os.sep)[-1])
                with delete_file_tab:
                    delete_file = st.button("删除文件",key="delete_file")
                    if delete_file:
                        if os.path.isfile(select_file_or_dir_abs):
                            with st.spinner("删除中..."):
                                os.remove(select_file_or_dir_abs)
                                st.success("删除成功")
                                is_rerun = True
                        else:
                            st.warning("无法删除文件")
                with rename_dir_tab:
                    new_dir_name = st.text_input("请输入更名后的文件名称",key="rename_dir_name")
                    if new_dir_name != "":
                        rename_dir = st.button("重命名文件",key="rename_folder")
                        if rename_dir:
                            not_in_name = ["\\","/",">","<",":","*","?","\"","|"]
                            can_be_name = True
                            for i in not_in_name:
                                if i in new_dir_name:
                                    can_be_name = False
                            if can_be_name:
                                renamed = (os.sep).join(select_file_or_dir_abs.split(os.sep)[:-1])+os.sep+new_dir_name
                                print(renamed)
                                if os.path.exists(renamed):
                                    st.warning("文件已存在")
                                else:
                                    os.rename(select_file_or_dir_abs,renamed)
                                    st.info("重命名文件成功")
                                    is_rerun = True
                            else:
                                st.warning("文件名称不合法")
                            rename_dir = False
                        else:
                            st.success("请点击重命名文件按钮以重命名文件")
                    else:
                        st.success("请输入文件名称")
            if is_rerun:
                st.rerun()
    else:
        if st.session_state.get("RealTimeDdetection") == True:
            st.title(":blue[实时检测]")
            open(".faces","w").close()
            open(".spend_time","w").close()
            open(".show","w").close()
            s_t = time.time()
            if not "r_t" in st.session_state:
                status = st.success("正在连接,请稍后")
            else:
                status = st.info("正在响应,响应时间:"+str(round(st.session_state["r_t"],3))+"s")
            while (os.path.exists(".faces") or os.path.exists(".spend_time") or os.path.exists(".show")) and time.time()-s_t<5:
                time.sleep(0.001)
            time.sleep(0.001)
            if (os.path.exists(".faces") or os.path.exists(".spend_time") or os.path.exists(".show")):
                status.error("连接超时")
                if "r_t" in st.session_state:
                    del st.session_state["r_t"]
                time.sleep(4)
                st.rerun()
            else:
                st.session_state["r_t"] = time.time() - s_t
                st.image("frame.jpg",caption="实时画面",use_column_width=True)
                with open("faces.json","r") as f:
                    faces = json.load(f)
                with open("spend_time.txt","r") as f:
                    spend_time = float(f.read())
                col1,col2 = st.columns([1,5])
                with col1:
                    st.sidebar.metric(label="识别响应时间",value=spend_time)
                with col2:
                    st.sidebar.caption("检测到的人脸")
                    st.sidebar.dataframe(pd.DataFrame(faces,index=["x","y","w","h","SSIM","name"]))
            if st.sidebar.button("退出实时检测模式"):
                st.session_state["RealTimeDdetection"] = False
                st.rerun()
            time.sleep(1)
            st.rerun()
        st.title("控制台")
        tab0, tab1, tab2 = st.tabs(["概览", "实时检测","配置"])
        def parse_time(time_str):
            """Parse time string 'HH:MM' into a tuple (HH, MM)"""
            h, m = time_str.split(':')
            return int(h), int(m)

        def string_to_list(time_str):
            """Convert the formatted string back to the original list format"""
            intervals = []
            for line in time_str.split('\n'):
                times = line.split(',')
                start = parse_time(times[0])
                end = parse_time(times[1])
                intervals.append([start, end])
            return intervals
        with tab0:
            st.write("概览")
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
            face_size_limits = read_config("l.json")
            scaleFactor_minNeighbors = read_config("scaleFactor_minNeighbors.json")
            scaleFactor = scaleFactor_minNeighbors["scaleFactor"]
            minNeighbors = scaleFactor_minNeighbors["minNeighbors"]
            if not os.path.exists("enable_faces_comparison.txt"):
                with open("enable_faces_comparison.txt","w") as file:
                    file.write("False")
            with open("enable_faces_comparison.txt","r") as file:
                is_enable_faces_comparison = eval(file.read())
            st.caption("摄像头与检测")
            col1,col2,col3,col4 = st.columns(4)
            with col1:
                st.metric(label="摄像头ID", value=str(camera_id))
            with col2:
                st.metric(label="等待时间", value=str(wait_time))
            with col3:
                st.metric(label="检测间隔", value=str(detection_interval))
            with col4:
                if is_enable_faces_comparison:
                    if os.path.exists("comparison_threshold.txt"):
                        with open("comparison_threshold.txt","r") as file:
                            threshold = float(file.read())
                    else:
                        threshold = 0.7
                    st.metric(label="人脸比对阈值", value=threshold)
                else:
                    st.metric(label="人脸比对", value="禁用")
            col4,col5,col6 = st.columns(3)

            ls = []
            for i in intervals:
                start = str(i[0][0]) + ":" + str(i[0][1])
                end = str(i[1][0]) + ":" + str(i[1][1])
                ls.append([start, end])
            df_intervals = pd.Series(ls,name="监测时间")
            with col4:st.dataframe(df_intervals)
            st.caption("分割区域")
            df_polygon_points = pd.DataFrame(polygon_points,index=["x","y"])
            st.dataframe(df_polygon_points.T)
            with col5:st.dataframe(pd.Series(face_size_limits,name="人脸大小限制"))
            with col6:st.dataframe(pd.Series(scaleFactor_minNeighbors,name="人脸检测参数"))
        with tab1:
            if st.button("进入实时检测"):
                st.session_state["RealTimeDdetection"] = True
                st.rerun()
        with tab2:
            update = False
            tab7,tab8,tab9,tab10,tab11,tab13,tab12 = st.tabs(["摄像头","检测时间段","检测间隔","分割区域","人脸识别设置","人脸比对设置","警告音设置"])
            with tab7:
                u_camera_id = st.number_input("摄像头ID",min_value=0,max_value=100,value=camera_id)
                if u_camera_id != camera_id:
                    with open("camera.txt","w") as file:
                        file.write(str(u_camera_id))
                    st.info("已保存")
                    update = True
            with tab8:
                s = '\n'.join([','.join([f"{start[0]:02d}:{start[1]}" for start in interval0]) for interval0 in intervals])
                s1 = st.text_area(label="监测时间",value=s,height=200)
                try:
                    if s != s1:
                        new_list = string_to_list(s1)
                        with open("intervals.json","w") as file:
                            json.dump(new_list,file)
                        st.info("已保存")
                        update = True
                except:
                    st.error("格式错误")
            with tab9:
                u_wait_time = st.number_input("最小报警间隔",min_value=0,max_value=60000,value=wait_time)
                u_c_wait_time = st.number_input("探测间隔",min_value=0.1,max_value=10.0,step=0.1,value=detection_interval)
                if u_wait_time != wait_time:
                    with open("wait.txt","w") as file:
                        file.write(str(u_wait_time))
                    st.info("已保存")
                    update = True
                if detection_interval != u_c_wait_time:
                    with open("detection_interval.txt","w") as file:
                        file.write(str(u_c_wait_time))
                    st.info("已保存")
                    update = True
            with tab10:
                df_polygon_points = pd.DataFrame(polygon_points,index=["x","y"]).T
                edited_df = st.data_editor(df_polygon_points,num_rows="dynamic")
                if not edited_df.equals(df_polygon_points):
                    with open("split.json","w") as file:
                        json.dump(edited_df.T.to_dict(),file)
                        st.info("已保存")
                    update = True
            with tab11:
                u_face_size_min = st.number_input("最小人脸大小",min_value=15,max_value=1999,value=face_size_limits["min"])
                u_face_size_max = st.number_input("最大人脸大小",min_value=16,max_value=2000,value=face_size_limits["max"])
                u_scaleFactor = st.number_input("缩放比例",min_value=1.01,max_value=1.9,step=0.01,value=scaleFactor)
                u_minNeighbors = st.number_input("最小邻居数",min_value=1,max_value=100,value=minNeighbors)
                if u_scaleFactor != scaleFactor or u_minNeighbors != minNeighbors:
                    with open("scaleFactor_minNeighbors.json","w") as file:
                        json.dump({"scaleFactor":u_scaleFactor,"minNeighbors":u_minNeighbors},file)
                        st.info("已保存")
                    update = True
                if u_face_size_min != face_size_limits["min"] or u_face_size_max != face_size_limits["max"]:
                    with open("l.json","w") as file:
                        json.dump({"min":u_face_size_min,"max":u_face_size_max},file)
                    st.info("已保存")
                    update = True
            with tab12:
                file = st.file_uploader("上传提示音",type=["mp3","wav"])
                file2 = st.file_uploader("上传报警音",type=["mp3","wav"])
                if file is not None:
                    with open("audio.wav","wb") as f:
                        f.write(file.read())
                    shutil.copy("audio.wav","warning.wav")
                    update = True
                    st.info("已保存")
                if file2 is not None:
                    with open("audio2.wav","wb") as f:
                        f.write(file2.read())
                    shutil.copy("audio2.wav","warning2.wav")
                    update = True
                    st.info("已保存")
                if os.path.exists("audio.wav"):
                    if st.checkbox("调节音量"):
                        import pydub
                        audio = pydub.AudioSegment.from_file("audio.wav")
                        #调节音量
                        audio = audio + st.number_input("提示音量",min_value=-100,max_value=100,value=0)
                        audio.export("warning.wav",format="wav")
                        audio2 = pydub.AudioSegment.from_file("audio2.wav")
                        #调节音量
                        audio2 = audio2 + st.number_input("报警音量",min_value=-100,max_value=100,value=0)
                        audio2.export("warning2.wav",format="wav")
                        update = True
                        st.info("已保存")
                    else:
                        if not os.path.exists("warning.wav"):
                            shutil.copy("audio.wav","warning.wav")
                        if not os.path.exists("warning2.wav"):
                            shutil.copy("audio2.wav","warning2.wav")
            with tab13:
                if not os.path.exists("enable_faces_comparison.txt"):
                    with open("enable_faces_comparison.txt","w") as file:
                        file.write("False")
                with open("enable_faces_comparison.txt","r") as file:
                    is_enable_faces_comparison = eval(file.read())
                if st.checkbox("启用人脸比对",value=is_enable_faces_comparison):
                    if is_enable_faces_comparison == False:
                        with open("enable_faces_comparison.txt","w") as file:
                            file.write("True")
                        update = True
                    is_enable_faces_comparison = True
                    if os.path.exists("comparison_threshold.txt"):
                        with open("comparison_threshold.txt","r") as file:
                            threshold = float(file.read())
                    else:
                        threshold = 0.7
                    threshold2 = st.number_input("阈值",min_value=0.0,max_value=1.0,step=0.01,value=threshold)
                    if threshold2 != threshold:
                        threshold = threshold2
                        with open("comparison_threshold.txt","w") as file:
                            file.write(str(threshold))
                            update = True
                        st.info("已保存")
                    if st.button("进入人脸比对库"):
                        st.session_state["face_library_management"] = True
                        st.rerun()
                else:
                    if is_enable_faces_comparison == True:
                        with open("enable_faces_comparison.txt","w") as file:
                            file.write("False")
                            update = True
                    is_enable_faces_comparison = False

            if st.button("重启"):
                open(".change","w").close()
                st.session_state["restart"] = True
                st.rerun()


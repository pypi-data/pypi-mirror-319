"""
hyy制作
Toolbox 版本: 1.0
Toolbox 翻译: 工具箱.
Toolbox 的一些功能是从网络上搜集的.
"""
#导入模块
import requests
import os
import ctypes
import sys
import cv2
import pygame
from bs4 import BeautifulSoup
import time
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import random

# Toolbox 介绍
print('Hello! YourToolbox1: 1.0 HYY Python:',sys.version,'Welcome to use the YourToolbox1.')

#爬虫函数:发送方式get，要爬取的下载链接url，下载完成后的名字destination，保存位置Savelocation
def download_file_get(url, destination,Savelocation):
    try:
        os.chdir(Savelocation)
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功

        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # 过滤掉保持活动连接的空chunk
                    file.write(chunk)

        print(f"Downloaded successfully to {destination}")
    except Exception as e:
        print(f"Failed to download the file due to error: {e}")

#爬虫函数:发送方式post，要爬取的下载链接url，下载完成后的名字destination，保存位置Savelocation
def download_file_post(url, destination,Savelocation):
    try:
        os.chdir(Savelocation)
        response = requests.post(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功

        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # 过滤掉保持活动连接的空chunk
                    file.write(chunk)

        print(f"Downloaded successfully to {destination}")
    except Exception as e:
        print(f"Failed to download the file due to error: {e}")

#获取管理员权限
def Obtain_administrator_privileges():
    print('Obtaining administrator privileges.')
    #判断是否有administrator（管理员）权限
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    #如果没有administrator（管理员）权限那就用administrator（管理员）权限重新打开程序.
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        print('Successfully obtained administrator privileges.')
        sys.exit()

#播放视频的函数—— Key_position 按下 Key_position 变量指定的键停止播放—— Video_path 播放的视频路径
def Play_Video(Video_path,Key_position):
    # 定义视频路径
    video_path = Video_path
    # 创建 VideoCapture 对象
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("错误：无法打开视频. ")
    else:
        # 循环读取每一帧图像直到结束
        while True:
            ret, frame = cap.read()

            if not ret:
                break
            # 展示当前帧
            cv2.imshow('Playing Video', frame)
            # 如果按下 Key_position 变量指定的键停止播放
            if cv2.waitKey(25) & 0xFF == ord(Key_position):
                break
        # 清理资源
        cap.release()
        cv2.destroyAllWindows()

#播放MP3文件的函数，file_path要播放的MP3文件的路径
def play_mp3_with_pygame(file_path):
    pygame.init()
    # 加载 MP3 文件
    pygame.mixer.music.load(file_path)
    # 开始播放音频
    pygame.mixer.music.play()
    # 循环等待直到音乐结束
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.quit()

#激活Windows专业版系统
def Activation_Windows专业版():
    #获取管理员权限
    Obtain_administrator_privileges()
    #通过命令行激活
    os.system('slmgr /ipk W269N-WFGWX-YVC9B-4J6C9-T83GX')
    os.system('slmgr /skms kms.03k.org')
    os.system('slmgr /ato')
    print('激活时长：'+os.system('slmgr /xpr'))

#激活Windows企业版系统
def Activation_Windows企业版():
    #获取管理员权限
    Obtain_administrator_privileges()
    #通过命令行激活
    os.system('slmgr /ipk NPPR9-FWDCX-D2C8J-H872K-2YT43')
    os.system('slmgr /skms kms.03k.org')
    os.system('slmgr /ato')
    print('激活时长：'+os.system('slmgr /xpr'))

#激活Windows家庭版系统
def Activation_Windows家庭版():
    #获取管理员权限
    Obtain_administrator_privileges()
    #通过命令行激活
    os.system('slmgr /ipk TX9XD-9SN7V-6WMQ6-BX7FG-H8Q99')
    os.system('slmgr /skms kms.03k.org')
    os.system('slmgr /ato')
    print('激活时长：'+os.system('slmgr /xpr'))

#爬取必去网小说(http://www.ibiquw.info)
def BiquNetwork_novel_downloader(Book_number):
    print('')
    print('必去小说网下载小说 (http://www.ibiquw.info) ')
    time.sleep(0.5)
    print('==================================================================================================')
    if not os.path.exists(os.getcwd()+"/xiao_shuo"):
        print('')
        print('当前没有‘xiao_shuo’文件夹，已自动创建。')
        print('')
        os.makedirs('xiao_shuo')
        os.chdir(os.getcwd()+"/xiao_shuo")
        time.sleep(0.5)
        print('==================================================================================================')
        print('')
        print('已将路径设为‘xiao_shuo’文件夹。')
        print('')
        print('==================================================================================================')
        print('')
        print('书号为进入你想下载的那本书，点击上面的网址 http://www.biquw.com/book/ () / ， 括号部分为书号')
        print('')
        print('==================================================================================================')
        time.sleep(0.5)

    else:
        print('')
        print('当前已有‘xiao_shuo’文件夹，已将路径设为‘xiao_shuo’文件夹。')
        print('')
        os.chdir(os.getcwd()+"/xiao_shuo")
        time.sleep(0.5)
        print('==================================================================================================')
        print('')
        print('书号为进入你想下载的那本书，点击上面的网址 http://www.biquw.com/book/ () / ， 括号部分为书号')
        print('')
        print('==================================================================================================')
        time.sleep(0.5)

    def book_page_list(book_id):
        url = 'http://www.biquw.com/book/{}/'.format(book_id)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
        response = requests.get(url, headers)
        response.encoding = response.apparent_encoding
        response = BeautifulSoup(response.text, 'lxml')
        booklist = response.find('div', class_='book_list').find_all('a')
        return booklist


    def book_page_text(bookid, booklist):
        try:
            for book_page in booklist:
                page_name = book_page.text.replace('*', '')
                page_id = book_page['href']
                time.sleep(2)
                url = 'http://www.biquw.com/book/{}/{}'.format(bookid,page_id)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
                response_book = requests.get(url, headers)
                response_book.encoding = response_book.apparent_encoding
                response_book = BeautifulSoup(response_book.text, 'lxml')
                book_content = response_book.find('div', id="htmlContent")
                with open("./{}/{}.txt".format(bookid,page_name), 'a') as f:
                    f.write(book_content.text.replace('\xa0', ''))
                    print("当前下载章节：{}".format(page_name))
                    print('')
        except Exception as e:
            while True:
                print("\033[31mPROGRAM: There is a problem with the program!\033[0m")
                print("\033[31mPROGRAM: Unable to access novel resources . No novel found!\033[0m")
                print(e)
                bookid = input("获取目录失败，请确保书号输入正确！")
                time.sleep(1)
                #if __name__ == '__main__':
                bookid = Book_number
                    # 如果书号对应的目录不存在，则新建目录，用于存放章节内容
                if not os.path.isdir('./{}'.format(bookid)):
                        os.mkdir('./{}'.format(bookid))
                try:
                        booklist = book_page_list(bookid)
                        print(f"获取目录成功！已成功在'xiao_shuo'文件夹创建 {bookid} 文件夹")
                        time.sleep(0.5)
                        print('')
                        print("正在获取章节资源...")
                        print('')
                        time.sleep(3)
                        book_page_text(bookid, booklist)
                except Exception as e:
                            print("\033[31mPROGRAM: There is a problem with the program!\033[0m")
                            print("\033[31mPROGRAM: Unable to access novel resources . No novel found!\033[0m")
                            print(e)
                            input("获取目录失败，请确保书号输入正确！")
                            time.sleep(1)

    #if __name__ == '__main__':
        bookid = Book_number
        # 如果书号对应的目录不存在，则新建目录，用于存放章节内容
        if not os.path.isdir('./{}'.format(bookid)):
            os.mkdir('./{}'.format(bookid))
        try:
            booklist = book_page_list(bookid)
            print(f"获取目录成功！已成功在'xiao_shuo'文件夹创建 {bookid} 文件夹")
            time.sleep(0.5)
            print('')
            print("正在获取章节资源...")
            print('')
            time.sleep(2)
            book_page_text(bookid, booklist)
        except Exception as e:
            while True:
                print("\033[31mPROGRAM: There is a problem with the program!\033[0m")
                print("\033[31mPROGRAM: Unable to access novel resources . No novel found!\033[0m")
                print(e)
                bookid = input("获取目录失败，请确保书号输入正确！")
                time.sleep(1)
                #if __name__ == '__main__':
                bookid = Book_number
                    # 如果书号对应的目录不存在，则新建目录，用于存放章节内容
                if not os.path.isdir('./{}'.format(bookid)):
                        os.mkdir('./{}'.format(bookid))
                try:
                        booklist = book_page_list(bookid)
                        print(f"获取目录成功！已成功在'xiao_shuo'文件夹创建 {bookid} 文件夹")
                        time.sleep(0.5)
                        print('')
                        print("正在获取章节资源...")
                        print('')
                        time.sleep(3)
                        book_page_text(bookid, booklist)
                except Exception as e:
                            print("\033[31mPROGRAM: There is a problem with the program!\033[0m")
                            print("\033[31mPROGRAM: Unable to access novel resources . No novel found!\033[0m")
                            print(e)
                            input("获取目录失败，请确保书号输入正确！")
                            time.sleep(1)

#一些做成的成品代码
def Model_3D():#3D模型
    def generate_tree_data(height=20, width=10):
        x = []
        y = []
        z = []

        for h in range(0, height):  # Height levels from bottom to top.
            radius = (height - h) * (width / height)

            num_points_per_circle = int(math.pi * 2 * radius)
            theta = np.linspace(-np.pi, np.pi, num_points_per_circle)

            for t in theta:
                x.append(radius * math.cos(t))
                y.append(radius * math.sin(t))
                z.append(h)

        return np.array(x), np.array(y), np.array(z)


    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    x, y, z = generate_tree_data()

    scatter = ax.scatter(
        x,
        y,
        z,
        c=z,
        cmap=cm.coolwarm,
        marker="o",
        s=[random.randint(5, 50) for _ in range(len(x))]
    )

    # Add star on top
    star_x, star_y, star_z = [0], [0], [max(z)+2]
    ax.scatter(star_x, star_y, star_z, color='yellow', s=200, label='Star')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.title("Dynamic 3D Christmas Tree Animation")

    for angle in range(0, 360):
        ax.view_init(30, angle)
        plt.draw()
        plt.pause(.001)

    plt.show()

# 在桌面创建快捷方式
def Desktop_快捷方式(target,name):
    import winshell
    from win32com.client import Dispatch

    def create_shortcut(targets, shortcut_name):
        desktop = winshell.desktop()  # 获取桌面路径
        shortcut_path = f"{desktop}\\{shortcut_name}.lnk"

                # 创建快捷方式
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = targets  # 指向目标文件的路径
        shortcut.WorkingDirectory = os.path.dirname(targets)
        shortcut.save()

        if __name__ == "__main__":
            target_file = target  # 目标文件路径
            shortcut_name = name  # 快捷方式名称
            create_shortcut(target_file, shortcut_name)

if __name__ == '__main__':
    print('You, Hello!')
    input('Bye Bye! ')
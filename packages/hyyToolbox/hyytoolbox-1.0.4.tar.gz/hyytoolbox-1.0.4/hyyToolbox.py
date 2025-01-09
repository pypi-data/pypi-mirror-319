"""
hyy制作
hyyToolbox 版本: 1.0
hyyToolbox 翻译: 工具箱
---------------------------------功能
hyyToolbox 的一些功能是从网络上搜集的.
hyyToolbox 的other可以解密,加密文件
hyyToolbox 的download功能可以下载Web上面的东西
hyyToolbox 自身可以获取管理员权限,有一些游戏
"""
#导入模块
"""如果报错则转到下面的代码安装库"""
try:
    import requests ,os ,ctypes ,sys ,cv2 ,pygame
    import time ,math ,random ,winshell
    from bs4 import BeautifulSoup
    import numpy as np
    from matplotlib import cm
    import matplotlib.pyplot as plt
    import tkinter.filedialog as filedialog
    import download
    import Windows
    import other

#安装库
except ImportError:
    
    import pip
    pip.main(["install", "--user", "requests","beautifulsoup4","matplotlib","pygame","winshell","pywin32"])
    
    import requests ,os ,ctypes ,sys ,cv2 ,pygame
    import time ,math ,random ,winshell
    from bs4 import BeautifulSoup
    import numpy as np
    from matplotlib import cm
    import matplotlib.pyplot as plt
    from win32com.client import Dispatch
    import tkinter.filedialog as filedialog
    import download
    import Windows
    import other

# Toolbox 介绍
print('Hello! hyyToolbox: 1.0.4 HYY Python:',sys.version,'Welcome to use the hyyToolbox.')
# 输入汉字单行文本
def hyywrite(filename, contents, encoding='utf-8'):
    with open(filename, 'w', encoding=encoding) as fh:
        fh.write(contents)

# 获取管理员权限
def Administrator():
    print('Obtaining administrator privileges.')
    # 判断是否有administrator（管理员）权限
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
def play_music_mp3(file_path):
    pygame.init()
    # 加载 MP3 文件
    pygame.mixer.music.load(file_path)
    # 开始播放音频
    pygame.mixer.music.play()
    # 循环等待直到音乐结束
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.quit()

#下载 - 填post 或 get，就是两种发送方式，要爬取的下载链接url，下载完成后的名字destination，保存位置Savelocation - 用自制的download模块
def Download(select_By, url, destination,Savelocation):
    if select_By == 'get' or 'Get' or 'GET':
        download.download_get(url=url, destination=destination,Savelocation=Savelocation)
    
    elif select_By == 'post' or 'Post' or 'POST':
        download.download_post(url=url, destination=destination,Savelocation=Savelocation)
    
    else:
        print("Not 'get' or 'post'.")
        print("hyyToolbox doesn't know how to deal with it.")

#爬取必去网小说(http://www.ibiquw.info)
def BiquNetwork_novel_downloader(Book_number):
    """必去小说下载器(http://www.ibiquw.info)"""
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
    """3D的模型,视角可转动,有颜色变化"""
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

#加密文件
def Encryption(Encrypt_files,key_name,Save_name):#Encrypt_files指定加密的文件,key_name密钥保存名字,Save_name加密后的名字
    #使用另一自制文件 - other
    other.Encryption(Encrypt_files,key_name,Save_name)

#解密文件
def decrypt(Encrypt_files,key_name,Save_name):#Encrypt_files指定解密的文件,key_name读取的密钥名字,Save_name解密后的名字
    #使用另一自制文件 - other
    other.decrypt(Encrypt_files,key_name,Save_name)

path = path_variable = os.getenv('PATH') or "Environment variable PATH is not set."

def twine(install_requires,name,version):
    print('正在生成...')
    line = [
    'from setuptools import setup, find_packages',

        'setup(',
        f'name={name},',
        f'version={version},',
        'packages=find_packages(),',
        'install_requires=[',
            f'{install_requires}', 
        '],',
    ')',
]   
    try:
        with open('setup.py', 'w', encoding='utf-8') as fh:
            for lin in line:
                fh.write(lin + '\n')
    except Exception as e:
        print('生成失败!',e)
        
    print('生成完毕！')

# 在桌面创建快捷方式
def DesktopShortcuts(target,name):
    def create_shortcut(targets, shortcut_name):
        desktop = winshell.desktop()  # 获取桌面路径
        shortcut_path = f"{desktop}\\{shortcut_name}.lnk"

                # 创建快捷方式
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = targets  # 指向目标文件的路径
        shortcut.WorkingDirectory = os.path.dirname(targets)
        shortcut.save()

        target_file = target  # 目标文件路径
        shortcut_name = name  # 快捷方式名称
        create_shortcut(target_file, shortcut_name)

#创建快捷方式-用自制的Windows模块
def Shortcuts(target,name,poaition):#target目标文件路径-name快捷方式的名称-poaition快捷方式创建的位置
    Windows.Shortcuts(target=target,name=name,poaition=poaition)

#计算器-用自制的Windows模块
def Calculator(Calculator_selenction):

    if Calculator_selenction == 1:
        Windows.__add__()

    elif Calculator_selenction == 2:
        Windows.__guiadd__()

    else:
        print('Error - hyyToolbox - Windows module')

#opens打开
def open(title,file,limitation):
    global opens
    opens = filedialog.askopenfilename(title=title, filetypes=[(file,limitation),])

"""直接运行则触发 if __name__ == '__main__':"""
if __name__ == '__main__':
    print('You, Hello! - hyyToolbox')
    print(path)
    Calculator(Calculator_selenction=2)

#否则 else:
else:
    print('hyy(hyyToolbox): Welcome to play with my components!')
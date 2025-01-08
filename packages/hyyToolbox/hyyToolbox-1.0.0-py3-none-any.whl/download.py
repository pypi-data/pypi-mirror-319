try:
    #尝试安装模块
    import os
    import requests
    import urllib

except ImportError:
    """安装模块"""
    import pip
    pip.main(["install", "--user", "requests"])

#爬虫函数:发送方式get，要爬取的下载链接url，下载完成后的名字destination，保存位置Savelocation
def download_get(url, destination,Savelocation):
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
def download_post(url, destination,Savelocation):
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

def download_Video(url,name):
    """url=下载视频的url,name=下载出来的名字"""

    # 下载视频

    url_video = url

    urllib.request.urlretrieve(url_video,name+'.mp4')

def download_html(url,name):
    """url=下载网站的url,name=下载出来的名字"""

    # 下载网页

    url_page = url

    if name == '':
        urllib.request.urlretrieve(url_page,'auto-toolbox.html')
    else:
        urllib.request.urlretrieve(url_page,name+'.html')

def download_picture(url):
    """url=下载图片的url"""
    # 下载图片
    import urllib
    import re
    
    def getHtml(urls):
        page = urllib.urlopen(urls)
        html = page.read()
        return html
    
    def getImg(html):
        reg = r'src="(.+?\.jpg)" pic_ext'
        imgre = re.compile(reg)
        imglist = re.findall(imgre,html)
        x = 0
        for imgurl in imglist:
            urllib.urlretrieve(imgurl,'%s.jpg' % x)
            x+=1
    
    
    html = getHtml(url)
    
    print (getImg(html))

print('auto-toolbox 1.0 - download')
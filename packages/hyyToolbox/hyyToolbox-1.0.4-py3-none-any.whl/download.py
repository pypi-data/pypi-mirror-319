try:
    #尝试安装模块
    import os
    import requests
    import urllib
    import csv
    import re
    import time
    import requests
    import csv
    import pandas as pd
    import matplotlib.pyplot as plt
    import warnings
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd

except ImportError:
    """安装模块"""
    import pip
    pip.main(["install", "--user", "requests","pandas","matplotlib","beautifulsoup4"])

    import os
    import requests
    import urllib
    import csv
    import re
    import time
    import requests
    import csv
    import pandas as pd
    import matplotlib.pyplot as plt
    import warnings
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd

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

def download_tieba_tiezi(url):
    """下载艺恩娱数的一些票房数据"""
    warnings.filterwarnings('ignore')
    plt.rcParams['font.sans-serif'] = ['SimHei'] #解决中文显示
    plt.rcParams['axes.unicode_minus'] = False   #解决符号无法显示
    
    def main():
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',}
        data = {
            'r': '0.9936776079863086',
            'top': '50',
            'type': '0',
        }
        resp = requests.post('https://ys.endata.cn/enlib-api/api/home/getrank_mainland.do', headers=headers, data=data)
        data_list = resp.json()['data']['table0']
        for item in data_list:
            rank = item['Irank']  # 排名
            MovieName = item['MovieName']  # 电影名称
            ReleaseTime = item['ReleaseTime']  # 上映时间
            TotalPrice = item['BoxOffice']   # 总票房(万)
            AvgPrice = item['AvgBoxOffice']   # 平均票价
            AvgAudienceCount = item['AvgAudienceCount']  # 平均场次
            # 写入csv文件
            csvwriter.writerow((rank,MovieName,ReleaseTime,TotalPrice,AvgPrice,AvgAudienceCount))
            print(rank,MovieName,ReleaseTime,TotalPrice,AvgPrice,AvgAudienceCount)
    
    def data_analyze():
        # 读取数据
        data = pd.read_csv('07.csv')
        # 从上映时间中提取出年份
        data['年份'] = data['上映时间'].apply(lambda x: x.split('-')[0])
        # 各年度上榜电影总票房占比
        df1 = data.groupby('年份')['总票房(万)'].sum()
        plt.figure(figsize=(6, 6))
        plt.pie(df1, labels=df1.index.to_list(), autopct='%1.2f%%')
        plt.title('各年度上榜电影总票房占比')
        plt.show()
        # 各个年份总票房趋势
        df1 = data.groupby('年份')['总票房(万)'].sum()
        plt.figure(figsize=(6, 6))
        plt.plot(df1.index.to_list(), df1.values.tolist())
        plt.title('各年度上榜电影总票房趋势')
        plt.show()
        # 平均票价最贵的前十名电影
        print(data.sort_values(by='平均票价', ascending=False)[['年份', '电影名称', '平均票价']].head(10))
        # 平均场次最高的前十名电影
        print(data.sort_values(by='平均场次', ascending=False)[['年份', '电影名称', '平均场次']].head(10))
    
    
    if __name__ == '__main__':
        # 创建保存数据的csv文件
        with open('07.csv', 'w', encoding='utf-8',newline='') as f:
            csvwriter = csv.writer(f)
            # 添加文件表头
            csvwriter.writerow(('排名', '电影名称', '上映时间', '总票房(万)', '平均票价', '平均场次'))
            main()
        # 数据分析
        data_analyze()

print('auto-toolbox 1.0 - download')

def download_博客园():
    # 获取网址
    url_root = 'https://www.cnblogs.com/sitehome/p/'
    headers = {
        "Referer":"https://www.cnblogs.com/",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    # 构建链接
    n = range(2,10)                         
    urls = [url_root+f'{i}' for i in n]     # 构建网页

    # 取单个链接里面的文章信息：url、标题、作者、点赞数量、评论数量等
    def get_single_article_info(url):

        re = requests.get(url,headers=headers)      # 返回信息
        if re.status_code != 200:                   # 判断是否爬取成功
            print('error!')
        soup = BeautifulSoup(re.text,"html.parser")         # 创建一个 BeautifulSoup 对象进行数据解析

        articles = soup.find('div',id = 'post_list',class_ = 'post-list') .find_all('article',class_ = 'post-item')     # 找到文章 article

        data = []                                               # 创建一个装数据的列表
        for article in articles:
            author,comment,recomment,views = '',0,0,0           # 创建初始值

            infos = article.find_all('a')
            for info in infos:
                if 'post-item-title' in str(info):
                    href = info['href']
                    title = info.get_text()
                if 'post-item-author' in str(info):
                    author = info.get_text().strip()
                if 'icon_comment' in str(info):
                    comment = info.get_text().strip()
                if 'icon_digg' in str(info):
                    recomment = info.get_text().strip()
                if 'icon_views' in str(info):
                    views = info.get_text().strip()

            data.append([href,title,author,comment,recomment,views])        # 将需要的信息放入data里

        return data

    # 循环每个url，获取信息
    data = []
    i = 0
    for url in urls:
        i += 1
        print(f'正在爬取: {i},url:{url}')
        single_data = get_single_article_info(url)
        for single in single_data:
            data.append(single)

    # 打印日志
    print(f'爬取完成，共爬取{len(urls)}个页面')

    # 写入 Excel
    df = pd.DataFrame(data,columns=['href','title','author','comment','recomment','views'])
    df.to_excel('文章信息爬取结果.xlsx',index=True)  # index=True 加上索引

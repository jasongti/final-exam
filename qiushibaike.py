# coding:utf-8

import requests
import re
import threading

# 获取图片地址
def get_the_pic(page):
    result_lst = []
    url = 'https://www.qiushibaike.com/imgrank/page/%d/' % page
    content = requests.get(url).text
    # 匹配html中以//开头以class=illustration结尾的字符串，组成列表
    lst = re.findall(r"//.*illustration", content)
    for j in lst:
        try:
            # 匹配图片地址，组成列表
            result_lst.append(re.findall(r"(//.*\.jpeg|//.*\.png|//.*\.jpg|//.*\.gif|//.*\.pdf)", j)[0])
        except:
            return []
    return result_lst

# 下载图片
def download_the_pic(lst):
    for i in lst:
        # 去图片名称作为文件名称
        file_name = i.split('/')[-1]
        url = 'http:' + i
        r = requests.get(url)
        # 以二进制格式打开文件并写入，存在则覆盖
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content():
                if chunk:
                    f.write(chunk)
            print '%s 下载完成' % file_name.encode('utf8')

if __name__=='__main__':
    while True:
        try:
            startpage = input("请输入要抓取图片的起始页码：")
            endpage = input("请输入要抓取图片的截止页码：")
            break
        except:
            print '请输入正确的页码'
            continue
    print '开始下载'
    # 创建进程列表
    thread_list = []
    for i in range(startpage,endpage+1):
        pic_lst = get_the_pic(i)
        # 创建进程
        downloading = threading.Thread(target=download_the_pic, args=(pic_lst,))
        # 将进程加入进程列表
        thread_list.append(downloading)
        # 启动进程
        downloading.start()
    # 等待所有子进程结束后进入主进程
    for i in thread_list:
        i.join()
    print '\n完成'
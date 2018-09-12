import requests
from bs4 import BeautifulSoup
import re
from queue import Queue
import csv

queue = Queue()

headers = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
     "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}


start_url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,数据分析,2,{}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
urls = [start_url.format(p) for p in range(1,100)]

def get_info(url):
    url = queue.get()
    url1 = eval(url)  #使用eval（）函数去除href字符串两端的引号
    try:
        html = requests.get(url1,headers=headers).content.decode("gbk")
        soup = BeautifulSoup(html,'lxml')
        title = soup.find('div',class_='tCompanyPage').find('div',class_='tCompany_center clearfix').find(
            'div',class_='tHeader tHjob').find('div',class_='in').find('div',class_='cn').find('h1').text
        tit = title.strip()
        company = soup.find('div',class_='tCompanyPage').find('div',class_='tCompany_center clearfix').find(
            'div',class_='tHeader tHjob').find('div',class_='in').find('div',class_='cn').find('a').text
        com = company.strip()
        salary = soup.find('div',class_='tCompanyPage').find('div',class_='tCompany_center clearfix').find(
            'div',class_='tHeader tHjob').find('div',class_='in').find('div',class_='cn').find('strong').text
        sal = salary.strip()
        responsibility = soup.find('div',class_='bmsg job_msg inbox').text
        res = responsibility.replace("微信", "").replace("分享", "").replace("邮件", "").replace("\t", "").strip()
        with open('info.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([tit, com, sal, res])
    except:
        print('当前页面爬取失败')
    queue.task_done()


for url in urls:  #循环遍历第1页到第n页的url
    html = requests.get(url,headers=headers).content.decode("gbk")
    soup = BeautifulSoup(html,'lxml')
    divs = soup.find('div',class_='dw_wp').find('div',class_='dw_table').find_all('div',class_='el')
    divs = str(divs)
    result = re.findall(r'<a href=(.*?)onmousedown', divs)
    for href in result:   #将前面循环遍历所提取的url加入到队列中
        queue.put(href)
        get_info(href)






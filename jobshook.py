import sys
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import xlrd, xlwt, re, codecs, time
import importlib
import threading

from statistic_CH_EN import Statistic

importlib.reload(sys)


class LagouSpider():

    def __init__(self):
        # 大数据
        # self.url = 'https://www.lagou.com/jobs/list_%E5%A4%A7%E6%95%B0%E6%8D%AE%E5%BC%80%E5%8F%91?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput='
        # 计算机视觉
        # self.url = 'https://www.lagou.com/jobs/list_%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89?labelWords=&fromSearch=true&suginput='
        # NLP
        self.url = 'https://www.lagou.com/jobs/list_%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput='
        self.browser = webdriver.Chrome("./chromedriver")
        self.wait = WebDriverWait(self.browser, 10)

    def run(self):

        self.browser.get(self.url)
        while True:
            text = self.browser.page_source
            #  提取具体页面的url
            self.parse_page(text)
            #  提取下一页的按钮，注意class的值中有空格不可用。
            next_btn = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="pager_container"]/span[last()]')))
            #  判断是否是最后一页，如果是，退出while循环
            if 'pager_next pager_next_disabled' in next_btn.get_attribute('class'):
                break
            else:
                next_btn.click()
                time.sleep(1)

    #  提取具体页面的url
    def parse_page(self, text):

        html = etree.HTML(text)
        #  判断所需元素是否加载出来
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="position_link"]')))
        detial_urls = html.xpath('//a[@class="position_link"]/@href')
        for detial_url in detial_urls:
            #  请求详情页
            self.request_detial_url(detial_url)
            time.sleep(1)
            #  提取之后，把当前的页面关闭

    #  请求详情页
    def request_detial_url(self, detial_url):

        #  解析具体页面的字段信息时候，打开了另一个页面，覆盖原来的页面，我们这里做的是利用while True循环来获取全部页面的字段信息
        #  所以第一个页面的窗口不能关闭
        self.browser.execute_script("window.open('%s')" % detial_url)  #  打开另一个窗口
        self.browser.switch_to.window(self.browser.window_handles[1])  #  切换到另一个窗口
        source = self.browser.page_source
        #  解析详情页的具体字段
        self.parse_detial_url(source)
        #  请求完之后关闭当前详情页的页面
        self.browser.close()
        #  切换回第一页
        self.browser.switch_to.window(self.browser.window_handles[0])  #  切换到首页
        #  解析详情页的具体字段

    def parse_detial_url(self, source):

        text = etree.HTML(source)

        #  判断所需元素是否加载出来
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="name"]')))
        desc = ''.join(text.xpath('//dd[@class="job_bt"]//text()')).strip()
        print(desc)

        # city = text.xpath('//dd[@class="job_request"]/p[1]/span[2]/text()')[0]
        # city = re.sub(r'[\s/]', '', city)

        f = open('job.txt', 'a')
        f.write(desc)
        f.close()


class SpiderThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        spider = LagouSpider()
        spider.run()


class StatisticThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while(1):
            time.sleep(3)
            statistic = Statistic()
            statistic.run()



def main():
    SpiderThread().start()
    StatisticThread().start()


if __name__ == '__main__':
    main()

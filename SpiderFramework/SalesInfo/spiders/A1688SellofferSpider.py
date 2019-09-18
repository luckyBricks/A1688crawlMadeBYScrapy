# -*- coding: utf-8 -*-


import scrapy
from bs4 import BeautifulSoup

from SalesInfo.items import SalesinfoItem

KEYWORD = "basf"
PAGE = '20'


class A1688SellofferSpider(scrapy.Spider):
    name = 'test1688Spider'
    allowed_domains = ['www.1688.com']  # 爬虫允许爬取的网址域名。
    start_urls = ['https://www.1688.com/']  # 需要爬取的链接的列表，response对象默认传递给 self.parse 函数处理。

    def start_requests(self):
        for page in range(1, int(PAGE) + 1):
            url = 'https://s.1688.com/selloffer/offer_search.htm?keywords=%s&beginPage=%s' % (KEYWORD, page)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 实例化一个数据模型
        item = SalesinfoItem()
        for tag in response.css('.sw-dpl-offer-item').extract():
            try:
                # 从response中利用css选择器提取出来的标签是文本形式，需要利用 BeautifulSoup 转换成BeautifulSoup.Tag 对象进行进一步提取。
                soup = BeautifulSoup(tag, 'lxml')
                item['title'] = soup.select(".sw-dpl-offer-photo img")[0].attrs['alt'].strip()
                item['company'] = soup.select(".sw-dpl-offer-companyName")[0].attrs['title'].strip()
                item['price'] = soup.select(".sw-dpl-offer-priceNum")[0].attrs['title'].strip()
                item['sell'] = soup.select(".sm-offer-tradeBt")[0].attrs['title'].strip()
                item['rebuy'] = soup.select(".sm-widget-offershopwindowshoprepurchaserate span")[2].string.strip()
                item['method'] = soup.select(".sm-widget-offershopwindowshoprepurchaserate i")[0].string.strip()


                # if soup.select(".sm-offer-location")[0].attrs['title']:
                #     address = soup.select(".sm-offer-location")[0].attrs['title']
                # else:
                #     address = " "
                item['address'] = "fakeAddress"
                if soup.select(".sm-offer-subicon a"):
                    subicon = []
                    for i in soup.select(".sm-offer-subicon a"):
                        subicon.append(i.attrs['title'] + ',')
                    print(subicon)
                    item['subicon'] = str(subicon)
                else:
                    item['subicon'] = " "
                yield item
            except Exception as Error:
                yield item

                print("错误信息:", Error)
                continue

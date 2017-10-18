# -*- coding: utf-8 -*-
import os
import scrapy
from scrapy import Request


class JiaxingSpider(scrapy.Spider):
    name = "jiaxing"
   # allowed_domains = ["http://www.tcmap.com.cn/zhejiangsheng/jiaxing.html"]
    start_urls = ['http://www.tcmap.com.cn/zhejiangsheng/jiaxing.html']

    def parse(self, response):
        tds = response.css('table')[1].css('tr')
        for index in range(1,len(tds)):
            print('>>>>>>>>')
            tmpname = tds[index].css('td')[0].css('a::text').extract_first()
            streetnames = tds[index].css('td')[3].css('div a::text').extract()
            self.store_area(tmpname,streetnames)

            streetsurl = tds[index].css('td')[3].css('div a::attr("href")').extract()

            #self.generate_new_url(streetnames, streetsurl)#
            #print(streetnames, streetsurl)
            for index in range(1, len(streetsurl)):
                path = 'http://www.tcmap.com.cn/zhejiangsheng/' + streetsurl[index]
                print(path)
                yield Request(path, self.store_street, meta={'area': streetnames[index], 'path': path})

    def store_street(self,response):
        print(response.meta['area'] + "  " + response.meta['path'])
        items = response.css('div[id="page_left"] div.f12::text').extract()
        for item in items:
            print(item,">>>>>>>>>>>")
            file = open('街道/{0}.txt'.format(response.meta['area']), 'a', encoding='utf-8')
            file.write('{0}\n'.format(item.strip().split(' ', 2)[2]))
            file.close()

    def store_area(self,tmpname,streetnames):
        file = open('区/{0}.txt'.format(tmpname), 'a', encoding='utf-8')
        for streetname in streetnames:
            file.write('{0}\n'.format(streetname))
        file.close()

    # def generate_new_url(self,streetnames,streetsurl):
    #     print(streetnames,streetsurl)
    #     for index in range(1, len(streetsurl)):
    #         path = 'http://www.tcmap.com.cn/zhejiangsheng/' + streetsurl[index]
    #         print(path)
    #         yield Request(path, self.store_street, meta={'area': streetnames[index], 'path': path})




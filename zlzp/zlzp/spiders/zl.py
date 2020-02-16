# -*- coding: utf-8 -*-
import sys
import scrapy
from zlzp.items import ZwItem

class ZlSpider(scrapy.Spider):
    # 他决定运行爬虫使用的名字
    name = 'zl'
    # 允许的域名
    allowed_domains = ['zhaopin.com']
    # 开始链接
    # start_urls = ['http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&kw=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&p=1&isadv=0/']
    def parse(self, response):
        zw_list=[u'数据分析',u'数据挖掘',u'Python',u'爬虫']
        urls = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&kw={}&p=1&isadv=0/'
        for key in zw_list:
            href=urls.format(key)
            print href
            # yield scrapy.Request(url=href,callback=self.parse_list(),dont_filter=True)
    # 默认执行的方法
    def parse_list(self, response):
        print '*'*100
        # response 下载器返回的结果
        # 1）职位列表数据抓取
        # a建立选择器
        sel=scrapy.Selector(response)
        # b完成每一个职位数据的获取(extract变成列表,不加就是一个对象)
        zw_tr=sel.xpath('//table[@class="newlist"]/tr')
        print len(zw_tr)
        # i=0
        for item in zw_tr:
            item_1=ZwItem()
            zwmc=item.xpath('string(td[@class="zwmc"])').extract()
            gsmc = item.xpath('string(td[@class="gsmc"])').extract()
            # print zwmc[0].strip()
        #     for item in gsmc:
        #         print item
        #         i+=1
        # print i
            zwyx=item.xpath('td[@class="zwyx"]/text()').extract()
            gsdd=item.xpath('td[@class="gzdd"]/text()').extract()
            fbsj=item.xpath('td[@class="gxsj"]/span/text()').extract()
            href=item.xpath('td[@class="zwmc"]/div/a/@href').extract()
            # 一般非空的判断，都是由管道去做的
            if zwmc:
                item_1['zwmc']=zwmc[0]
            else:
                item_1['zwmc']=''

            if gsmc:
                item_1['gsmc']=gsmc[0]
            else:
                item_1['gsmc']=''

            if zwyx:
                item_1['zwyx']=zwyx[0]
            else:
                item_1['zwyx']='-'

            if gsdd:
                item_1['gsdd']=gsdd[0]
            else:
                item_1['gsdd']=''

            if fbsj:
                item_1['fbsj']=fbsj[0]
            else:
                item_1['fbsj']=''
            if href:
                item_1['href']=href[0]
            yield item_1
        next_page=sel.xpath('//li[@class="pagesDown-pos"]/a/@href').extract()
        if next_page:
            next_page_href=next_page[0]
            # callback 请求完将结果交给谁，dont_filter是否验证域名
            # 此处也可以使用return
            yield(scrapy.Request(url=next_page_href,callback=self.parse,dont_filter=True))


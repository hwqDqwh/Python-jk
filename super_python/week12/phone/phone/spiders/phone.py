# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from phone.config import spider_config
from phone.items import *

class PhoneSpider(scrapy.Spider):
    name = 'phone'
    allowed_domains = ['smzdm.com']
    
    def start_requests(self):
        yield scrapy.Request(
            url='https://www.smzdm.com/fenlei/zhinengshouji/h5c4s0f0t0p1/#feed-main/',
            callback=self.parse,
            headers=spider_config.HEADERS
         )

    # 解析函数
    def parse(self, response):
        """
        爬取手机信息页面的前 10 条咨询
        """

        try:
            print(f'{response.url} ---------------------------------')

            divs = Selector(response=response).xpath('//*[@id="feed-main-list"]/li')

            items = []

            for i in range(1):

                item = PhoneItem()
                item['name'] = divs[i].xpath('./div/div[2]/h5/a/text()').extract_first()
                item['worth'] = divs[i].xpath('./div/div[2]/div[4]/div[1]/span/a[1]/span[1]/span/text()').extract_first()
                item['no_worth'] = divs[i].xpath('./div/div[2]/div[4]/div[1]/span/a[2]/span[1]/span/text()').extract_first()
                yield item
                
                jump_url = divs[i].xpath('./div/div[2]/h5/a/@href').extract_first().strip()
                print(jump_url)

                if (jump_url):
                    yield scrapy.Request(
                        url=jump_url,
                        callback=self.detail_parse,
                        headers=spider_config.HEADERS,
                        meta={'phone_name':item['name']}
                    )

            print('end')

        except Exception as excep:
            print(excep)


    def detail_parse(self, response):
        """
        爬取详情页的评论信息
        """

        print(f'{response.url} ---------------------------------')

        phone_name = response.meta['phone_name']

        comments = Selector(response=response).xpath('//*[@id="commentTabBlockNew"]/ul[1]/li[@class="comment_list"]')

        # 每页最多 30 条评论
        for i in range(1):
            try:

                comment_item = CommentItem()
                comment_item['phone_name'] = phone_name
                comment_item['user_name'] = comments[i].xpath('./div[2]/div[1]/a/span/text()').extract_first()
                # 无二级评论 //*[@id="li_comment_172433968"]/div[2]/div[2]/div[1]/p/span
                # 有二级评论 //*[@id="li_comment_172434136"]/div[2]/div[3]/div[1]/p/span
                comment_con_wrap = comments[i].xpath('./div[2]/div[@class="comment_conWrap"]')
                comment_item['comment_content'] = comment_con_wrap.xpath('./div[@class="comment_con"]/p/span/text()').extract_first()
                comment_item['comment_time'] = comments[i].xpath('./div[2]/div[1]/div[@class="time"]/text()').extract_first()
                comment_item['agree'] = comment_con_wrap.xpath('./div[@class="comment_action"]/a[2]/span/text()').extract_first().strip('(').strip(')')
                comment_item['opposition'] = comment_con_wrap.xpath('./div[@class="comment_action"]/a[3]/span/text()').extract_first().strip('(').strip(')')
                
                yield comment_item

                try:
                    next_page_url = comments[i].xpath('//*[@id="commentTabBlockNew"]/ul[2]/li[@class="pagedown"]/a/@href').extract_first().strip()

                    if (next_page_url):
                        print(next_page_url)
                        
                        yield scrapy.Request(
                            url=next_page_url,
                            callback=self.detail_parse,
                            headers=spider_config.HEADERS,
                            meta={'phone_name':phone_name}
                        )
                    else:
                        print('no next')

                except AttributeError as excep:
                    # AttributeError: 'NoneType' object has no attribute 'strip'
                    print('没有下一页了')
            except IndexError as rangExcep:
                # IndexError: list index out of range
                print('已到达页末尾')

        print('end!')
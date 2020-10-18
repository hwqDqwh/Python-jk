# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PhoneItem(scrapy.Item):
    collection_name = 'phone'

    name = scrapy.Field()
    worth = scrapy.Field()
    no_worth = scrapy.Field()
    comment_lists = scrapy.Field()
    phone_name = scrapy.Field()
    user_name = scrapy.Field()
    comment_content = scrapy.Field()
    comment_time = scrapy.Field()
    agree = scrapy.Field()
    opposition = scrapy.Field()

class CommentItem(scrapy.Item):
    collection_name = 'comment'
    
    phone_name = scrapy.Field()
    user_name = scrapy.Field()
    comment_content = scrapy.Field()
    comment_time = scrapy.Field()
    agree = scrapy.Field()
    opposition = scrapy.Field()
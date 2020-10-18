# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter
import pandas as pd
from snownlp import SnowNLP
from phone.config import db_mysql
from phone.items import *

class MyPipiline:
    """
    public parent pipeline class
    deal common open and close mysql link operate
    """
    def __init__(self):
        self.db_conn =pymysql.connect(
            host=db_mysql.DB_CONN['host'],
            port=db_mysql.DB_CONN['port'],
            db=db_mysql.DB_CONN['db'],
            user=db_mysql.DB_CONN['user'],
            passwd=db_mysql.DB_CONN['password'],
            charset='utf8'
        )
        self.db_cur = self.db_conn.cursor()
    
    def __del__(self):
        self.db_cur.close()
        self.db_conn.commit()
        self.db_conn.close()


class PhonePipeline(MyPipiline):
    """
    save phone list
    inherit the class MyPipiline
    """

    def process_item(self, item, spider):
        if item.collection_name == 'phone':
            print('phone pipeline')
        elif item.collection_name == 'comment':
            print ('comment pipeline')

        if isinstance(item, PhoneItem):
            print('save item:::::::::::::::::::')
            print(item)
            # return item
            
            sql = f'SELECT count(*) FROM phone_information WHERE `name` = "{item["name"]}"'
            self.db_cur.execute(sql)
            exists_res = self.db_cur.fetchall()[0][0]
            print(f'sql exists_res : {exists_res}')
            # print(f'sql exists_res2 : {exists_res2}')

            if exists_res:
                update_sql = f'UPDATE phone_information SET `worth` = "{item["worth"]}", `no_worth` = "{item["no_worth"]}" WHERE `name` = "{item["name"]}"'
                self.db_cur.execute(update_sql)
                update_res2 = self.db_cur.fetchall()

            else:
                insert_sql = f'INSERT INTO phone_information (`name`,`worth`,`no_worth`)VALUES("{item["name"]}","{item["worth"]}","{item["no_worth"]}")'
                self.db_cur.execute(insert_sql)
                insert_res2 = self.db_cur.fetchall()

        return item



class CommentPipeline(MyPipiline):
    """
    save phone comment list
    inherit the class MyPipiline
    """

    def process_item(self, item, spider):
        if item.collection_name == 'phone':
            print('phone pipeline')
        elif item.collection_name == 'comment':
            print ('comment pipeline')
            

        if isinstance(item, CommentItem):
            print('save comment item:')
            print(item)

            sql = f'SELECT id FROM phone_information WHERE `name` = "{item["phone_name"]}"'
            self.db_cur.execute(sql)
            
            try:
                sql_return = self.db_cur.fetchall()
                print(f' sql return {sql_return}')
                information_id = sql_return[0][0] # 查询结果为空时获得空元组 IndexError: tuple index out of range
            except IndexError as excep:
                information_id = None
                print(f' sql {sql}')

            if not information_id:
                print('找不到对应的手机资讯')
                return item

            # 利用 SnowNLP 进行情感分析
            try:
                s = SnowNLP(item['comment_content'])
                print(f'情感分析: {s.sentiments}, for {item["comment_content"]}')
            except Exception as e:
                print('情感分析出错,跳过保存')
                print(e)
                return item
            
            sql = f'SELECT count(*) FROM phone_comments WHERE `information_id` = "{information_id}" and `user_name` = "{item["user_name"]}"'
            self.db_cur.execute(sql)
            exists_res = self.db_cur.fetchall()[0][0]

            if exists_res:
                update_sql = f'UPDATE phone_comments SET `phone_name` = "{item["phone_name"]}", `comment_content` = "{item["comment_content"]}", \
                `comment_time` = "{item["comment_time"]}", `agree` = "{item["agree"]}", `opposition` = "{item["opposition"]}", `sentiment` = "{s.sentiments}" \
                WHERE `information_id` = "{information_id}" and `user_name` = "{item["user_name"]}"'
                self.db_cur.execute(update_sql)
                update_res2 = self.db_cur.fetchall()
                # print(f'sql update_res : {update_res}')

            else:
                insert_sql = f'INSERT INTO phone_comments (`information_id`,`phone_name`,`user_name`,`comment_content`,`comment_time`,`agree`,`opposition`,`sentiment`)\
                VALUES("{information_id}","{item["phone_name"]}","{item["user_name"]}","{item["comment_content"]}","{item["comment_time"]}","{item["agree"]}",\
                    "{item["opposition"]}","{s.sentiments}")'
                self.db_cur.execute(insert_sql)
                insert_res2 = self.db_cur.fetchall()
                # print(f'sql insert_res : {insert_res}')

        return item
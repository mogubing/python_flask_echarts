# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 数据清洗、过滤、存储
from scrapy.exceptions import DropItem
import time
import datetime
import pymysql
class ZlzpPipeline(object):
    def process_item(self, item, spider):
        return item

class DataCleanPipeline(object):
    def process_item(self,item,spider):
        # 去除职位名称和公司名称两边的空格
        item['zwmc']=item['zwmc'].strip()
        if item['zwmc']!='':
            item['gsmc']=item['gsmc'].strip()
            zwyx_list=item['zwyx'].split('-')
            if len(zwyx_list)>1:
                item['zwyx_low']=zwyx_list[0]
                item['zwyx_high']=zwyx_list[1]
            else:
                if zwyx_list[0] is not int:
                    item['zwyx_low']=0
                    item['zwyx_high']=0
                else:
                    item['zwyx_low']=item['zwyx_high']=zwyx_list[0]
           # 公司地点信息的切割
            item['gsdd']=item['gsdd'].split('-')[0]
            return item
        else:
            raise DropItem('zwmc is null')

class DataTimePipeline():
    def process_item(self,item,spider):
#         刚刚、几小时前、今天，昨天，前天
        if item['fbsj']==u'前天':
            # 使用time
            now_timetmp=time.time()
            last_day_timetmp=now_timetmp-60*60*24*2
            last_day_tuple=time.localtime(last_day_timetmp)
            item['fbsj']=time.strftime('%Y-%m-%d',last_day_tuple)
        elif item['fbsj']==u'昨天':
            item['fbsj']=str(datetime.date.today()-datetime.timedelta(days=1))
        elif item['fbsj']==u'今天'or item['fbsj']==u'刚刚'or u'小时前' in item['fbsj']:
            item['fbsj'] = str(datetime.date.today())
        else:
            year= time.strftime('%Y',time.localtime())
            item['fbsj']=year+'-'+item['fbsj']
        return item

# 针对一次爬虫的去重
class DuplicatesPipeline(object):
    def __init__(self):
        # 定义一个空集合
        self.name_seen=set()
    def process_item(self,item,spider):
        if item['zwmc']+item['gsmc'] in self.name_seen:
            raise DropItem('Duplicate item found %s'%item)
        else:
            self.name_seen.add(item['zwmc']+item['gsmc'])
            return item

# 数据存储
class MysqlPipeline(object):
#     建立初始化方法
    def __init__(self,mysql_host,mysql_user,mysql_passwd,mysql_db):
        self.MYSQL_HOST=mysql_host
        self.MYSQL_USER=mysql_user
        self.MYSQL_PASSWD=mysql_passwd
        self.MYSQL_DB=mysql_db


    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST','localhost'),
            mysql_user=crawler.settings.get('MYSQL_USER','mysql_user'),
            mysql_passwd=crawler.settings.get('MYSQL_PASSWD','mysql_passwd'),
            mysql_db=crawler.settings.get('MYSQL_DB','mysql_db')

        )

#     在爬虫启动的时候打开数据库的链接
    def open_spider(self,spider):
        self.conn=pymysql.connect(host=self.MYSQL_HOST,user=self.MYSQL_USER,passwd=self.MYSQL_PASSWD,db=self.MYSQL_DB,charset='utf8')
#     在爬虫关闭的时候断开数据库的链接
    def close_spider(self,spider):
        self.conn.commit()
        self.conn.close()
    def process_item(self,spider):
        cur=self.conn.cursor()
        cur.execute('delete from ca_list')
        cur.execute('delete from ca_dd')
        cur.execute('delete from ca_zwmc')
        cur.execute('delete from ca_gsmc')
        self.conn.commit()
#     数据存储
    def process_item(self,item,spider):
        cur=self.conn.cursor()
        cur.execute('select * from ca_gsdd where gsdd_name=%s',(item['gsdd'],))
        result_gsdd=cur.fetchone()
        if result_gsdd:
            gsdd_id=result_gsdd[0]
        else:
            cur.execute('insert into ca_gsdd value(null,%s)',(item['gsdd'],))
            cur.execute('select * from ca_gsdd where gsdd_name=%s', (item['gsdd'],))
            result_gsdd = cur.fetchone()
            gsdd_id = result_gsdd[0]

        cur = self.conn.cursor()
        cur.execute('select * from ca_zwmc where zwmc_name=%s', (item['zwmc'],))
        result_zwmc = cur.fetchone()
        if result_zwmc:
            zwmc_id = result_zwmc[0]
        else:
            cur.execute('insert into ca_zwmc value(null,%s)', (item['zwmc'],))
            cur.execute('select * from ca_zwmc where zwmc_name=%s', (item['zwmc'],))
            result_zwmc = cur.fetchone()
            zwmc_id = result_zwmc[0]

        cur = self.conn.cursor()
        cur.execute('select * from ca_gsmc where gsmc_name=%s', (item['gsmc'],))
        result_gsmc = cur.fetchone()
        if result_gsmc:
            gsmc_id = result_gsmc[0]
        else:
            cur.execute('insert into ca_gsmc value(null,%s)', (item['gsmc'],))
            cur.execute('select * from ca_gsmc where gsmc_name=%s', (item['gsmc'],))
            result_gsmc = cur.fetchone()
            gsmc_id = result_gsmc[0]

        cur=self.conn.cursor()
        cur.execute('select * from ca_list where zwmc_id=%s and gsmc_id=%s and gsdd_id=%s',(zwmc_id,gsmc_id,gsdd_id))
        result_list=cur.fetchone()
        if result_list:
            print ('Having')
        else:
            cur.execute('insert into ca_list value(null,%s,%s,%s,%s,%s,%s,%s)',(zwmc_id,gsdd_id,gsmc_id,item['zwyx_low'],item['zwyx_high'],item['fbsj'],item['href']))
        return item

















#coding:utf-8
"""
@author:ghh
@file:index.py
@time:2017/7/23 9:32
"""
# flask入口方法
from flask import Flask
# 调用页面
from flask import render_template
# json的解析模块
from flask import jsonify
import  pymysql
# 1、连接数据库
conn=pymysql.connect(host='localhost',user='root',passwd='root',db='ca',charset='utf8')
# 2、实例化flask
# 指定当前文件即模块，为主模块
app=Flask(__name__)
# 3、新建路径、编写js
@app.route('/dd/xz')
def dd_xz_view():
    return render_template('xzdt.html')
# 4、绑定路由
@app.route('/dd_xz')
# 5、提取数据、处理数据
def dd_xz():
# (1)读取数据库
# a、生成操作游标（一个窗口）
    cur=conn.cursor()
# b、编写sql
    sql='select round(avg(zwyx),2) as 平均薪资,province,count(ca_list.Id) from ca_list inner join ca_dd on ca_list.dd_id=ca_dd.Id GROUP BY province'
 #    sql='select round(avg(zwyx),2) as 平均薪资,province from ca_list inner join ca_dd on ca_list.dd_id=ca_dd.Id GROUP BY dd_id'
# c、执行sql
    cur.execute(sql)
# d、取出结果集
# fetchall能够得到全部结果集
    ca_list=cur.fetchall()
# (2)数据处理
    avg_zwyx={}
    for item in ca_list:
        dd_name=item[1]
#判断现有字典中是否存在dd_name对应的字符串的键
# 判断平均薪资是否存在这个地点
#         if not avg_zwyx.has_key(dd_name):
# 不存在则创建记录并存入对应的值
#             avg_zwyx[dd_name]={'name':dd_name,'value':item[0],'count':item[2]}
        avg_zwyx[dd_name]={'name':dd_name,'value':item[0]}
# 存在则重新计算平均薪资
#         else:
#             avg_zwyx[dd_name]={'name':dd_name,'value':(item[0]+avg_zwyx[dd_name]['value'])/2}
            # avg_zwyx[dd_name]={'name':dd_name,'value':item[0]*item[2]+(avg_zwyx[dd_name]['value']*avg_zwyx[dd_name]['count'])/(item[2]+avg_zwyx[dd_name]['count'])}
# d.重新规整数据，以字典形式转换成list形式
    return_avg_zwyx=[]
    for item in avg_zwyx:
        return_avg_zwyx.append(avg_zwyx[item])
# (3)将数据以json形式传递给前台
    returnData={}
    returnData['avg_zwyx']=return_avg_zwyx
    return jsonify(returnData)
if __name__=='__main__':
    app.run(debug=True)



#coding:utf-8
"""
@author:ghh
@file:index2(zf).py
@time:2017/7/23 14:33
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
@app.route('/dd/hh')
def dd_xz_view():
    return render_template('hh.html')
# 4、绑定路由
@app.route('/dd_hh')
# 5、提取数据、处理数据
def show_hh():
# (1)读取数据库
# a、生成操作游标（一个窗口）
    cur=conn.cursor()
# b、编写sql
    sql='select count(ca_list.Id) as count_zw,avg(ca_list.zwyx) as avg_zwyx,ca_xl.xl_name,max(ca_list.zwyx),min(ca_list.zwyx)\
from ca_list inner join ca_xl on ca_list.xl_id=ca_xl.Id group by ca_xl.Id order by count_zw desc'
# c、执行sql
    cur.execute(sql)
# d、取出结果集
# fetchall能够得到全部结果集
    xl_zwyx_list=cur.fetchall()
# (2)数据处理
    returnData={}
    count_zw=[]
    avg_xz=[]
    xl_list=[]
    max_xz=[]
    min_xz=[]
    for item in xl_zwyx_list:
        count_zw.append(item[0])
        avg_xz.append(round(item[1],2))
        xl_list.append(item[2])
        max_xz.append(item[3])
        min_xz.append(item[4])
    returnData['count_zw']=count_zw
    returnData['avg_xz'] = avg_xz
    returnData['xl_list']=xl_list
    returnData['max_xz'] = max_xz
    returnData['min_xz'] = min_xz
    return jsonify(returnData)
if __name__ == '__main__':
    app.run(debug=True)





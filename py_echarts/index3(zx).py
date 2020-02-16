#coding:utf-8
"""
@author:ghh
@file:index3(zx).py
@time:2017/7/24 17:25
"""
from flask import Flask
from flask import render_template
from flask import jsonify
import pymysql
conn=pymysql.connect(host='localhost',user='root',passwd='root',db='ca',charset='utf8')

app=Flask(__name__)
@app.route('/dd/zx')
def view():
    return render_template('zx.html')
@app.route('/dd_zx')
def show():
    cur = conn.cursor()
    sql='select ca_type.name,count(ca_list.id) as count,avg(ca_list.zwyx),max(ca_list.zwyx),min(ca_list.zwyx)\
from ca_list inner join ca_type on ca_list.type_id=ca_type.id group by ca_list.type_id order by count desc'

    cur.execute(sql)
    ca_list=cur.fetchall()
    type_list=[]
    count_zw=[]
    avg_zwyx=[]
    max_zwyx=[]
    min_zwyx=[]
    returnData={}
    for item in ca_list:
        type_list.append(item[0])
        count_zw.append(item[1])
        avg_zwyx.append(round(item[2],2))
        max_zwyx.append(item[3])
        min_zwyx.append(item[4])
    returnData['type_list']= type_list
    returnData['count_zw'] = count_zw
    returnData['avg_zwyx'] = avg_zwyx
    returnData['max_zwyx'] = max_zwyx
    returnData['min_zwyx'] = min_zwyx
    return jsonify(returnData)
if __name__=='__main__':
    app.run(debug=True)








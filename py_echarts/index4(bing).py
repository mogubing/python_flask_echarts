#coding:utf-8
"""
@author:ghh
@file:index4(bing).py
@time:2017/7/25 20:08
"""
from flask import Flask
from flask import render_template
from flask import jsonify
import pymysql

conn=pymysql.connect(host='localhost',user='root',passwd='root',db='ca',charset='utf8')
app=Flask(__name__)
@app.route('/dd/bing')
def view():
    return render_template('bing.html')
@app.route('/dd_bing')
def show():
    cur=conn.cursor()
    sql='select count(ca_list.id) as count,avg(ca_list.zwyx),ca_gsgm.gsgm_name'\
        'from ca_list inner join ca_gsgm on ca_list.gsgm_id=ca_gsgm.id group by ca_gsgm.id order by count desc'
    cur.execute(sql)
    ca_gsgm_list=cur.fetchall()
    returnData={}
    count_zw=[]
    avg_zwyx=[]
    gsgm_name=[]
    for item in ca_gsgm_list:
        count_zw.append(item[0])
        avg_zwyx.append(item[1])
        gsgm_name.append(item[2])
    returnData['count_zw']=count_zw
    returnData['avg_zwyx']=avg_zwyx
    returnData['gsgm_name']=gsgm_name
    return jsonify('returnData')
if __name__=='__main__':
    app.run(debug=True)

# -*- codeing = utf-8 -*-
# @Time : 2021/12/23 11:57
# @Author : tl
# @File : testSqlite.py
# @Software : PyCharm

import sqlite3
conn = sqlite3.connect("test.db")   #打开或创建数据库文件
print("成功打开数据库")
c = conn.cursor()   #获取游标
sql = '''
    create table company 
    (id int primary key not null,
    name text not null,
    age int not null,
    address char(50),
    salary real);
'''
c.execute(sql)  #执行sql语句
conn.commit()   #提交数据库操作
conn.close()    #关闭数据库连接

print("成功建表")
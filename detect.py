# -*- coding: utf-8 -*-
import time
import requests
import uuid
import os
import sys
import re
#import commands
import datetime
import threading
import subprocess
import pymysql
import socket
import fcntl
import struct


def get_mac_address(): 
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
    return mac
  
def get_ip_address():
    try :
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(( '8.8.8.8' , 80 ))
        (addr, port) = csock.getsockname()
        csock.close()
        return addr
    except socket.error:
        return "127.0.0.1"


def startWatch(m,s):
    timeLeft=60*m+s
    while timeLeft>0:
        time.sleep(1)
        timeLeft-=1
        print(str(timeLeft))
    playvoice()






def playvoice():
    try:
        os.system('omxplayer -o local jinbao.mp3')
    except os.error as e:
        print(str(e))
       
def playvoice1():
    os.system('omxplayer -o local helmetandvest.mp3')
    
    #helmet
def playvoice2():
    os.system('omxplayer -o local helmet.mp3')
def playvoice3():
    os.system('omxplayer -o local vest.mp3')
def threadsingle1():
    length=len(threading.enumerate())
    if length<2:
        t1=threading.Thread(target=playvoice1)
        t1.start()
def threadsingle2():
    length=len(threading.enumerate())
    if length<2:
        t2=threading.Thread(target=playvoice2)
        t2.start()
    
def threadsingle3():
    length=len(threading.enumerate())
    if length<2:
        t3=threading.Thread(target=playvoice3)
        t3.start()


def cameraphotos():
    t0=time.time()
    node=uuid.getnode()
    mac=uuid.UUID(int=node).hex[-12:]
    
    a=subprocess.getoutput("fswebcam --no-banner -r 640x480 "+mac+".jpg")
    
    print(a)
    path=r'/home/pi/dist/'+mac+'.jpg'
    
    if os.path.exists(path):
        url = "http://10.186.162.179:8080/test/"
        path_file0="/home/pi/dist/"+mac+".jpg"
        files = {'file0':open(path_file0,'rb')}
        try:
            result = requests.post(url=url,files=files)
            count=result.text.count("helmet")
            print(count)
            vestcount=result.text.count("reflectivecloth")
            print(vestcount)
            existstr="no_helmet" in result.text
            if existstr:
                if count>vestcount:
                    threadsingle1()
                else:
                    threadsingle2()
            else:
                if count>vestcount:
                    threadsingle3()
                    
            print('Done. (%.3fs)' % (time.time()-t0))
        except:
            print("Something error.")
        


class MysqldbHelper(object): # 继承object类所有方法
 
    '''
    构造方法：
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': 'root',
        'charset':'utf8',
        'cursorclass':pymysql.cursors.DictCursor
        }
    conn = pymysql.connect(**config)
    conn.autocommit(1)
    cursor = conn.cursor()
    '''
    def __init__(self , config):
 
        self.host = config['host']
        self.username = config['user']
        self.password = config['passwd']
        self.port = config['port']
        self.con = None
        self.cur = None
 
        try:
            self.con = pymysql.connect(**config)
            self.con.autocommit(1)
            # 所有的查询，都在连接 con 的一个模块 cursor 上面运行的
            self.cur = self.con.cursor()
        except:
            print("DataBase connect error,please check the db config.")
 
    # 关闭数据库连接
    def close(self):
        if not  self.con:
            self.con.close()
        else:
            print("DataBase doesn't connect,close connectiong error;please check the db config.")
 
    # 创建数据库
    def createDataBase(self,DB_NAME):
        # 创建数据库
        self.cur.execute('CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci' % DB_NAME)
        self.con.select_db(DB_NAME)
        print('creatDatabase:' + DB_NAME)
 
    # 选择数据库
    def selectDataBase(self,DB_NAME):
        self.con.select_db(DB_NAME)
 
    # 获取数据库版本号
    def getVersion(self):
        self.cur.execute("SELECT VERSION()")
        return self.getOneData()
 
    # 获取上个查询的结果
    def getOneData(self):
        # 取得上个查询的结果，是单个结果
        data = self.cur.fetchone()
        return data
 
    # 创建数据库表
    def creatTable(self, tablename, attrdict, constraint):
        """创建数据库表
            args：
                tablename  ：表名字
                attrdict   ：属性键值对,{'book_name':'varchar(200) NOT NULL'...}
                constraint ：主外键约束,PRIMARY KEY(`id`)
        """
        if self.isExistTable(tablename):
            print("%s is exit" % tablename)
            return
        sql = ''
        sql_mid = '`id` bigint(11) NOT NULL AUTO_INCREMENT,'
        for attr,value in attrdict.items():
            sql_mid = sql_mid + '`'+attr + '`'+' '+ value+','
        sql = sql + 'CREATE TABLE IF NOT EXISTS %s ('%tablename
        sql = sql + sql_mid
        sql = sql + constraint
        sql = sql + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'
        print('creatTable:'+sql)
        self.executeCommit(sql)
 
    def executeSql(self,sql=''):
        """执行sql语句，针对读操作返回结果集
            args：
                sql  ：sql语句
        """
        try:
            self.cur.execute(sql)
            records = self.cur.fetchall()
            return records
        except pymysql.Error as e:
            error = 'MySQL execute failed! ERROR (%s): %s' %(e.args[0],e.args[1])
            print(error)
 
    def executeCommit(self,sql=''):
        """执行数据库sql语句，针对更新,删除,事务等操作失败时回滚
        """
        try:
            self.cur.execute(sql)
            self.con.commit()
        except pymysql.Error as e:
            self.con.rollback()
            error = 'MySQL execute failed! ERROR (%s): %s' %(e.args[0],e.args[1])
            print("error:", error)
            return error
 
    def insert(self, tablename, params):
        """创建数据库表
            args：
                tablename  ：表名字
                key        ：属性键
                value      ：属性值
        """
        key = []
        value = []
        for tmpkey, tmpvalue in params.items():
            key.append(tmpkey)
            if isinstance(tmpvalue, str):
                value.append("\'" + tmpvalue + "\'")
            else:
                value.append(tmpvalue)
        attrs_sql = '('+','.join(key)+')'
        values_sql = ' values('+','.join(value)+')'
        sql = 'insert into %s'%tablename
        sql = sql + attrs_sql + values_sql
        print('_insert:'+sql)
        self.executeCommit(sql)
        
    def insertrows(self,sqltext):
        self.executeCommit(sqltext)
        
 
    def select(self, tablename, cond_dict='', order='', fields='*'):
        """查询数据
            args：
                tablename  ：表名字
                cond_dict  ：查询条件
                order      ：排序条件
            example：
                print mydb.select(table)
                print mydb.select(table, fields=["name"])
                print mydb.select(table, fields=["name", "age"])
                print mydb.select(table, fields=["age", "name"])
        """
        consql = ' '
        if cond_dict!='':
            for k, v in cond_dict.items():
                consql = consql+'`'+k +'`'+ '=' + '"'+v + '"' + ' and'
        consql = consql + ' 1=1 '
        if fields == "*":
            sql = 'select * from %s where ' % tablename
        else:
            if isinstance(fields, list):
                fields = ",".join(fields)
                sql = 'select %s from %s where ' % (fields, tablename)
            else:
                print("fields input error, please input list fields.")
        sql = sql + consql + order
        print('select:' + sql)
        return self.executeSql(sql)
    
    def selectrows(self,sqltext):
        return self.executeSql(sqltext)
 
    def insertMany(self,table, attrs, values):
        """插入多条数据
            args：
                tablename  ：表名字
                attrs        ：属性键
                values      ：属性值
            example：
                table='test_mysqldb'
                key = ["id" ,"name", "age"]
                value = [[101, "liuqiao", "25"], [102,"liuqiao1", "26"], [103 ,"liuqiao2", "27"], [104 ,"liuqiao3", "28"]]
                mydb.insertMany(table, key, value)
        """
        values_sql = ['%s' for v in attrs]
        attrs_sql = '('+','.join(attrs)+')'
        values_sql = ' values('+','.join(values_sql)+')'
        sql = 'insert into %s'% table
        sql = sql + attrs_sql + values_sql
        print('insertMany:'+sql)
        try:
            print(sql)
            for i in range(0,len(values),20000):
                    self.cur.executemany(sql,values[i:i+20000])
                    self.con.commit()
        except pymysql.Error as e:
            self.con.rollback()
            error = 'insertMany executemany failed! ERROR (%s): %s' %(e.args[0],e.args[1])
            print(error)
 
    def delete(self, tablename, cond_dict):
        """删除数据
            args：
                tablename  ：表名字
                cond_dict  ：删除条件字典
            example：
                params = {"name" : "caixinglong", "age" : "38"}
                mydb.delete(table, params)
        """
        consql = ' '
        if cond_dict!='':
            for k, v in cond_dict.items():
                if isinstance(v, str):
                    v = "\'" + v + "\'"
                consql = consql + tablename + "." + k + '=' + v + ' and '
        consql = consql + ' 1=1 '
        sql = "DELETE FROM %s where%s" % (tablename, consql)
        print(sql)
        return self.executeCommit(sql)
 
    def update(self, tablename, attrs_dict, cond_dict):
        """更新数据
            args：
                tablename  ：表名字
                attrs_dict  ：更新属性键值对字典
                cond_dict  ：更新条件字典
            example：
                params = {"name" : "caixinglong", "age" : "38"}
                cond_dict = {"name" : "liuqiao", "age" : "18"}
                mydb.update(table, params, cond_dict)
        """
        attrs_list = []
        consql = ' '
        for tmpkey, tmpvalue in attrs_dict.items():
            attrs_list.append("`" + tmpkey + "`" + "=" +"\'" + tmpvalue + "\'")
        attrs_sql = ",".join(attrs_list)
        print("attrs_sql:", attrs_sql)
        if cond_dict!='':
            for k, v in cond_dict.items():
                if isinstance(v, str):
                    v = "\'" + v + "\'"
                consql = consql + "`" + tablename +"`." + "`" + k + "`" + '=' + v + ' and '
        consql = consql + ' 1=1 '
        sql = "UPDATE %s SET %s where%s" % (tablename, attrs_sql, consql)
        print(sql)
        return self.executeCommit(sql)
    
 
    def dropTable(self, tablename):
        """删除数据库表
            args：
                tablename  ：表名字
        """
        sql = "DROP TABLE  %s" % tablename
        self.executeCommit(sql)
 
    def deleteTable(self, tablename):
        """清空数据库表
            args：
                tablename  ：表名字
        """
        sql = "DELETE FROM %s" % tablename
        print("sql=",sql)
        self.executeCommit(sql)
 
    def isExistTable(self, tablename):
        """判断数据表是否存在
            args：
                tablename  ：表名字
            Return:
                存在返回True，不存在返回False
        """
        sql = "select * from %s" % tablename
        result = self.executeCommit(sql)
        if result is None:
            return True
        else:
            if re.search("doesn't exist", result):
                return False
            else:
                return True
 
 
#def isrepeat():
 #   use_input_str=input('Please input new hostname: ')
  #  dbn=mydb.selectrows("select * from ppe_detect.equipment_info where hostname='"+use_input_str+"'")
   # if len(dbn)==0:
    #    return use_input_str
    #else:
    #    isrepeat()
 
if __name__ == "__main__":
    startWatch(0,30)
     # 定义数据库访问参数
    config = {
        'host': 'cnwuxm0tes04',
        'port': 3306,
        'user': 'ppe_testuser',
        'passwd': 'ppe_testuser',
        'db': 'ppe_detect',
        'cursorclass': pymysql.cursors.DictCursor
    }
 
    # 初始化打开数据库连接
    mydb = MysqldbHelper(config)
    
    hostname=socket.gethostname()
    macaddr=get_mac_address()
    ipaddr=get_ip_address()
    dbn=mydb.selectrows("select * from ppe_detect.equipment_info where macaddr='"+macaddr+"' limit 1")
    print(dbn)
    shitime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    if len(dbn)==0:
        mydb.insertrows("insert into ppe_detect.equipment_info(site,hostname,macaddr,ipaddr,firstlogin,lastlogin,logintimes) values('undetermined','NewEquip','"+macaddr+"','"+ipaddr+"','"+shitime+"','"+shitime+"','1')")
    else:
        dbn1=mydb.selectrows("select * from ppe_detect.equipment_info where macaddr='"+macaddr+"' and firstlogin is null limit 1")
        if len(dbn1)!=0:
            mydb.insertrows("update ppe_detect.equipment_info set firstlogin='"+shitime+"',lastlogin='"+shitime+"',logintimes=logintimes+1 where macaddr='"+macaddr+"' and firstlogin is null")
        else:
            mydb.insertrows("update ppe_detect.equipment_info set lastlogin='"+shitime+"',logintimes=logintimes+1 where macaddr='"+macaddr+"'")
            while 1:
                cameraphotos()

# -*- coding: utf-8 -*-
import mysql.connector
from .settings import mysql_host,mysql_port,mysql_user_name,mysql_user_password,mysql_database_name
class DoubanPipeline:
    # 连接数据库
    def __init__(self):
        self.conn = mysql.connector.connect(host=mysql_host, port=mysql_port, database=mysql_database_name, user=mysql_user_name, password=mysql_user_password, charset='utf8')
        self.cs=self.conn.cursor()

    # 数据表是否存在
    def tableExists(self):
        stmt = 'SHOW TABLES LIKE "{}"'.format("movies")
        self.cs.execute(stmt)
        return self.cs.fetchone()
    # 数据库操作
    def process_item(self, item, spider):
        try:
            if self.tableExists():
                print("不建数据表")
            else:
                print("创建数据表")
                creat_sql = "CREATE TABLE movies (serial_number VARCHAR(10),movie_name VARCHAR(150),introduce text,star VARCHAR(10),evaluate VARCHAR(100),describle text)"
                self.cs.execute(creat_sql)
                print("创建成功")
            # 插入数据
            sql="insert into movies (serial_number,movie_name,introduce,star,evaluate,describle) values(%s,%s,%s,%s,%s,%s)"
            self.cs.execute(sql,(item['serial_number'],item['movie_name'],item['introduce'],item['star'],item['evaluate'],item['describle']))
            self.conn.commit()
            # self.cs.close()
            # self.conn.close()
        except Exception as error:
            # 出现错误时打印错误日志
            print(error)
        return item

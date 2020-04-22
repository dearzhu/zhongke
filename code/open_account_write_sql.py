#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 20-4-16 下午10:58
# @Author  : zhu
# @Email   : xxx@163.com
# @File    : open_accunt_write_sql.py
# @Desc    :


import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import time,datetime


class Write_Sql:

    def __int__(self, user, pwd, ip, db_name, encoding_):
        self.user = user
        self.pwd = pwd
        self.ip = ip
        self.db_name = db_name
        self.encoding_ = encoding_

    def get_con_sql(self, user, pwd, ip, db_name, encoding_):
        """

        :param user :
        :param pwd:
        :param ip:
        :param db_name:
        :param encoding_: 编码格式
        :return: 数据库的连接
        """

        engine = create_engine(
            "mysql+pymysql://{}:{}@{}/{}?charset={}".format(user, pwd, ip, db_name, encoding_))
        # if_exists='replace/append/fail',
        # df1.to_sql('gas_bank_records', con=engine, if_exists='append', index=False)

        return engine

    def get_data(self, path):
        # 读取数据
        print('开始读取数据......')

        df = pd.read_csv(path, encoding='gb18030')
        print('开始选择目标字段.....')

        # 选择有效数据
        df=df[['\t银行卡号', '\t银行账号', '\t开户名称', '\t开户行','\t开户人证件类型', '\t账号开户日期', '\t开户人证件号码']]

        # 删除每个字段的回车符
        print('数据开始清洗......')
        df.columns=['cxkh','cxzh','jymc','khh','zjhm','khdate','card_num']
        for column in df.columns:
           
            df[column] = df[column].apply(lambda x: str(x).replace("\t", ""))
            df[column] = df[column].apply(lambda x: str(x).replace(" ", ""))
            print('数据清洗完成......')

        return df
        
    def main(self,paths,db_name,table_name):
        """
        :param paths :数据路径
        :param db_name:数据库名
        :param table_name: 目标表名
        :return: 
        """
        #write_sql = self.Write_Sql()
        # 连接数据库引擎
        print('数据库初始化......')
        t1 = datetime.datetime.now()

        engine = self.get_con_sql('root', '521521', '127.0.0.1:3306', db_name, 'utf8')
        for path in paths:
        
            # 读取数据
            df = self.get_data(path)
            # 获取数据库中的已有表
            table_list = [i[0] for i in engine.execute('show tables')]
            print('数据库中已有表:' + str(len(table_list)) + '个')
          
            print('已有表:'+','.join((tab_name) for tab_name in table_list))
            # 数据库引擎连接
            con = engine.connect()
            print('数据开始写入数据库......')
            # 分批输入数据，防止数据过多，引起进程被kill
            for i in range(0,np.int(df.shape[0]/100000)+1):
                print('第---{}----分区采集,总共---{}---区'.format(str(i),str(np.int(df.shape[0]/100000)+1)))
                df1=df[i*100000:(i+1)*100000]
                if table_name in table_list:
                # 如果表存在,则添加,不存在,则创建添加
                    df1.to_sql(table_name, con=con, if_exists='append', index=False)
                else:
                    df1.to_sql(table_name, con=con, if_exists='replace', index=False)

        t2 = datetime.datetime.now()
        print('开始时间:-------')
        print(t1)
        print('结束时间:-------')
        print(t2)
        print('总共耗时:' + str((t2 - t1).seconds))
        con.close()
        print('数据写入完成,关闭连接!!!')
        
 


if __name__ == '__main__':
    # 路径
    
    paths = [r'c:/Users/jxh/Desktop/20200422返回数据/开户信息20200422133650_1.csv']
    write_sql = Write_Sql()

    write_sql.main(paths,'sxzy','anti_money_account')

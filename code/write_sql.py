#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 20-4-16 下午10:58
# @Author  : zhu
# @Email   : xxx@163.com
# @File    : write_sql.py
# @Desc    :


import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import time


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

        df = pd.read_csv(path, encoding='gbk')
        print('开始选择目标字段.....')
        select_col = ['\t交易卡号', '\t交易账号', '\t交易方户名', '\t交易方证件号', '\t交易账户开户银行', '\t交易时间',
                      '\t交易金额', '\t交易余额', '\t交易币种', '\t借贷标志', '\t对手账号', '\t对手户名', '\t对手证件号',
                      '\t对手账户开户银行', '\t对手交易余额', '\t摘要说明', '\t备注', '\t批次', '\tIP地址', '\tMAC地址']
        # 选择有效数据
        df = df[select_col]
        # 重名字
        print('数据狂重新命名字......')
        df.columns = ['cxkh', 'cxzh', 'jymc', 'jyzjhm', 'jyzhkhh', 'jysj', 'jyje', 'jyye', 'jybz', 'jdbz', 'jydfzkh',
                      'jydfmc', 'jydfzjhm',
                      'jydfzhkhh', 'dsjyye', 'zysm', 'beiz', 'pc', 'ip', 'mac']

        # 删除每个字段的回车符
        print('数据开始清洗......')
        for column in df.columns:
            print('字段---------' + column + '-----开始清洗--')
            df[column] = df[column].apply(lambda x: str(x).replace("\t", ""))
        print('数据清洗完成......')

        return df


if __name__ == '__main__':
    # 路径
    path = '/home/zhu/Desktop/资金交易明细20200416183139_1.csv'
    write_sql = Write_Sql()
    # 连接数据库引擎
    print('数据库初始化......')
    engine = write_sql.get_con_sql('root', '521521', '127.0.0.1:3306', 'sxzy', 'utf8')
    # 读取数据
    df = write_sql.get_data(path)
    # 获取数据库中的已有表
    table_list = [i[0] for i in engine.execute('show tables')]
    print('数据库中已有表:' + str(len(table_list)) + '个')
    for tab_name in table_list:
        print('已有表:'+tab_name)
    # 数据库引擎连接
    con = engine.connect()
    print('数据开始写入数据库')
    t1 = time.clock()
    print('开始时间为:' + str(t1))
    if 'gs_df' in table_list:
    # 如果表存在,则添加,不存在,则创建添加
        df.to_sql('gs_df', con=con, if_exists='append', index=False)
    else:
        df.to_sql('gs_df', con=con, if_exists='replace', index=False)
    t2 = time.clock()
    print('结束时间于:' + str(t2), '   总共耗时:' + str(t2 - t1))
    con.close()
    print('关闭连接!!!')
    # /home/zhu/PycharmProjects/zhongke_project

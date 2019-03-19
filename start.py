#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:jieshukai
@file: init.py
@time: 2019/03/10
"""
import argparse
import os
import sys
from optparse import OptionParser

from pwiz_plus.tpl import MysqlMakeModels


class Arguments(object):
    parser = argparse.ArgumentParser()
    parseropt = OptionParser(usage='usage: --option arg')
    ao = parser.add_argument
    ao('-n', '--db_name', type=str, default='zr_test', help='数据库名称')
    ao('-H', '--host', type=str, default='127.0.0.1', help='数据库 host 默认 127.0.0.1')
    ao('-P', '--port', type=int, default=3306, help='数据库 port 默认 52102')
    ao('-u', '--user', type=str, default='root', help='用户')
    ao('-p', '--password', type=str, default='root', help='密码')

    def parse_argv(self, argv):
        options = self.parser.parse_args(argv[1:])
        return options


argument = Arguments()
option = argument.parse_argv(sys.argv)

make_config = dict(
    db_type='mysql',
    # db_name=option.db_name,
    db_name='zr_assets',
    # tables=['novel_my_channel']
    tables=None
)
# tables=None)
db_config = dict(user=option.user, password=option.password, host=option.host, port=option.port)
root_path = os.path.dirname(os.path.realpath(__file__))
# 程序生成
if __name__ == '__main__':
    make_models = MysqlMakeModels(**make_config, **db_config)
    tables = make_models.conn.get_tables()

    content = make_models.get_content()
    models_py_path = make_models.get_file_path(
        os.path.join(root_path, make_config['db_name'], 'models' + '.py'))
    sql_path = make_models.get_file_path(
        os.path.join(root_path, make_config['db_name'], 'sqls' + '.sql'))

    make_models.write_content(models_py_path, content)
    make_models.write_content(sql_path,
                              make_models.get_sql_content(make_models.conn, make_models.tables, partition=False))

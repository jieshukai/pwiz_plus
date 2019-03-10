#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:jieshukai
@file: init.py
@time: 2019/03/10
"""
import os

from pwiz_plus.tpl import MysqlMakeModels, CreateModels

make_config = dict(
    db_type='mysql',
    db_name='zr_novel',
    # tables=['novel_novels', 'zr_novel_sync'])
    tables=None)
db_config = dict(user='root', password='root', host='127.0.0.1', port=3306)
root_path = os.path.dirname(os.path.realpath(__file__))
# 程序生成
if __name__ == '__main__':
    make_models = MysqlMakeModels(**make_config, **db_config)
    content = make_models.get_content()
    create_models = CreateModels()
    models_py_path = create_models.get_file_path(
        os.path.join(root_path, 'apps', 'models', make_config['db_name'] + '.py'))
    sql_path = create_models.get_file_path(
        os.path.join(root_path, 'apps', 'sqls', make_config['db_name'] + '.sql'))

    create_models.write_py_content(models_py_path, content)
    create_models.write_sql_content(make_models.conn, make_models.tables, sql_path)

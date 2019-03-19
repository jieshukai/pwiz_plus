#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:jieshukai
@file: demo.py
@time: 2019/03/11
"""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import re
import time
from collections import namedtuple

import peewee
from sanic import Sanic, response
from sanic.views import HTTPMethodView
from sanic_session import Session
from sanic_jinja2 import SanicJinja2
import os

from pwiz_plus.tpl import MysqlMakeModels

app = Sanic()
Session(app)
jinja = SanicJinja2(app)

db_config = dict(user='root', password='root', host='127.0.0.1', port=3306)

make_config = dict(
    db_type='mysql',
    db_name='zr_novel',
    # tables=['novel_novels', 'zr_novel_sync'])
    tables=None,
    # db_config=db_config,
)
root_path = os.path.dirname(os.path.realpath(__file__))

# Specify the package name, if templates/ dir is inside module
# jinja = SanicJinja2(app, pkg_name='sanicapp')
# or use customized templates path
# jinja = SanicJinja2(app, pkg_name='demo', pkg_path='tool')
app.static('/static', os.path.join(root_path, 'templates', 'static'))


# or setup later
# jinja = SanicJinja2()
# jinja.init_app(app)
class Index(HTTPMethodView):
    @jinja.template('index.html')
    async def post(self, request):
        return {
            'item': type('item', (object,), dict(label='啊哈哈', name='bbb')),
            **locals()
        }

    @jinja.template('tpl/pytpl/model.tpl')  # decorator method is staticmethod
    async def get(self, request):
        column_type = namedtuple('column_type', (
            'columns',
            'primary_keys',
            'foreign_keys',
            'model_names',
            'indexes'))

        make_models = MysqlMakeModels(**make_config, **db_config)
        tables = make_models.conn.get_tables()
        db_class = make_models.introspector.get_database_class().__name__.replace('Pwiz', '')
        db_name = make_models.introspector.get_database_name()
        date = datetime.datetime.fromtimestamp(time.time())

        def make_model_name(table):
            model = re.sub('[^\w]+', '', table)
            model_name = ''.join(sub.title() for sub in model.split('_'))
            if not model_name[0].isalpha():
                model_name = 'T' + model_name
            return model_name

        def maeke_model_columns(table):
            columns = make_models.database.columns[table].items()
            # 排序
            primary_keys = make_models.database.primary_keys[table]
            for name, column in columns:
                skip = all([
                    name in primary_keys,
                    name == 'id',
                    len(primary_keys) == 1,
                    column.field_class in make_models.introspector.pk_classes])
                if skip:
                    continue
                if column.primary_key and len(primary_keys) > 1:
                    column.primary_key = False
                yield column.get_field()

        def make_all_model():
            tables_dict = ['{']
            for k, v in make_models.database.model_names.items():
                tables_dict.append("'{}': {}Model,".format(k, v))
            return '\n    '.join(tables_dict) + '\n}'

        data = dict(
            db_config=repr(make_models.introspector.get_database_kwargs()),
            __version__=peewee.__version__,
            all_model=make_all_model(),
            **locals()
        )
        return data


class CreateProject(HTTPMethodView):
    async def get(self, request, create_id):
        return response.json(create_id)


app.add_route(Index.as_view(), '/')
app.add_route(CreateProject.as_view(), r'/create/<create_id>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)

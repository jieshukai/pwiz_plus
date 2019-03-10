#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:jieshukai
@file: database.py
@time: 2019/03/10
"""
from collections import namedtuple

from peewee import *

ColumnMetadata = namedtuple(
    'ColumnMetadata',
    ('name', 'data_type', 'null', 'primary_key', 'table', 'default', 'help_text'))


class PwizMySQLDatabase(MySQLDatabase):

    def get_columns(self, table, schema=None):
        sql = """
            SELECT column_name, is_nullable, data_type,column_default,column_comment
            FROM information_schema.columns
            WHERE table_name = %s AND table_schema = DATABASE()"""
        cursor = self.execute_sql(sql, (table,))
        pks = set(self.get_primary_keys(table))
        res = [ColumnMetadata(name, dt, null == 'YES', name in pks, table, df, ht)
               for name, null, dt, df, ht in cursor.fetchall()]
        return res


class PwizPostgresqlDatabase(PostgresqlDatabase):
    pass


class PwizSqliteDatabase(SqliteDatabase):
    pass

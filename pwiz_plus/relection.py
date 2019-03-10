#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:jieshukai
@file: relection.py
@time: 2019/03/10
"""
from playhouse.reflection import *
from pwiz_plus.database import *
from pwiz_plus.metada import PwizMySQLMetadata

DATABASE_ALIASES = {
    PwizMySQLDatabase: ['mysql', 'mysqldb'],
    PwizPostgresqlDatabase: ['postgres', 'postgresql'],
    PwizSqliteDatabase: ['sqlite', 'sqlite3'],
}
DATABASE_MAP = dict((value, key)
                    for key in DATABASE_ALIASES
                    for value in DATABASE_ALIASES[key])


class PwizIntrospector(Introspector):
    @classmethod
    def from_database(cls, database, schema=None):
        if isinstance(database, PwizPostgresqlDatabase):
            metadata = PostgresqlMetadata(database)
        elif isinstance(database, PwizMySQLDatabase):
            metadata = PwizMySQLMetadata(database)
        else:
            metadata = SqliteMetadata(database)
        return cls(metadata, schema=schema)

#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:jieshukai
@file: metada.py
@time: 2019/03/10
"""
from playhouse.reflection import *
from pwiz.column import MysqlColumn


class PwizMySQLMetadata(MySQLMetadata):

    def get_columns(self, table, schema=None):
        metadata = OrderedDict(
            (metadata.name, metadata)
            for metadata in self.database.get_columns(table, schema))

        # Look up the actual column type for each column.
        column_types = self.get_column_types(table, schema)

        # Look up the primary keys.
        pk_names = self.get_primary_keys(table, schema)
        if len(pk_names) == 1:
            pk = pk_names[0]
            if column_types[pk] is IntegerField:
                column_types[pk] = PrimaryKeyField

        columns = OrderedDict()
        for name, column_data in metadata.items():
            columns[name] = MysqlColumn(
                name,
                field_class=column_types[name],
                raw_column_type=column_data.data_type,
                nullable=column_data.null,
                primary_key=column_data.primary_key,
                db_column=name,
                help_text=column_data.help_text
            )

        return columns



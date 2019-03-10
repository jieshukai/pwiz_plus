#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:jieshukai
@file: column.py
@time: 2019/03/10
"""
from playhouse.reflection import *


class MysqlColumn(Column):
    """
    Store metadata about a database column.
    """
    def __init__(self, name, field_class, raw_column_type, nullable,
                 primary_key=False, column_name=None, index=False, unique=False, default=None, extra_parameters=None,
                 help_text=''):
        super(MysqlColumn, self).__init__(name, field_class, raw_column_type, nullable,
                                          primary_key=primary_key, column_name=column_name, index=index,
                                          unique=unique, default=default, extra_parameters=extra_parameters)

        self.help_text = help_text

    def __repr__(self):
        attrs = [
            'field_class',
            'raw_column_type',
            'nullable',
            'primary_key',
            'column_name',
            'default',
            'help_text',
        ]
        keyword_args = ', '.join(
            '%s=%s' % (attr, getattr(self, attr))
            for attr in attrs)
        return 'Column(%s, %s)' % (self.name, keyword_args)

    def get_field_parameters(self):
        params = {}
        if self.extra_parameters is not None:
            params.update(self.extra_parameters)

        # Set up default attributes.
        if self.nullable:
            params['null'] = True
        if self.field_class is ForeignKeyField or self.name != self.column_name:
            params['column_name'] = "'%s'" % self.column_name
        if self.primary_key and not issubclass(self.field_class, AutoField):
            params['primary_key'] = True
        if self.default is not None:
            params['constraints'] = '[SQL("DEFAULT %s")]' % self.default

        # Handle ForeignKeyField-specific attributes.
        if self.is_foreign_key():
            params['model'] = self.rel_model
            if self.to_field:
                params['field'] = "'%s'" % self.to_field
            if self.related_name:
                params['backref'] = "'%s'" % self.related_name

        # Handle indexes on column.
        if not self.is_primary_key():
            if self.unique:
                params['unique'] = 'True'
            elif self.index and not self.is_foreign_key():
                params['index'] = 'True'
        if self.help_text:
            params['help_text'] = "'%s'" % self.help_text

        return params


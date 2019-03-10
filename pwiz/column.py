#!usr/bin/env python
#-*- coding:utf-8 _*-
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
    primary_key_types = (IntegerField, PrimaryKeyField)

    def __init__(self, name, field_class, raw_column_type, nullable,
                 primary_key=False, db_column=None, index=False, unique=False, help_text=''):
        super(MysqlColumn, self).__init__(name, field_class, raw_column_type, nullable,
                                          primary_key, db_column, index, unique)
        self.help_text = help_text

    def __repr__(self):
        attrs = [
            'field_class',
            'raw_column_type',
            'nullable',
            'primary_key',
            'db_column',
            'help_text',
        ]
        keyword_args = ', '.join(
            '%s=%s' % (attr, getattr(self, attr))
            for attr in attrs)
        return 'Column(%s, %s)' % (self.name, keyword_args)

    def get_field_parameters(self):
        params = {}

        # Set up default attributes.
        if self.nullable:
            params['null'] = True
        if self.field_class is ForeignKeyField or self.name != self.db_column:
            params['db_column'] = "'%s'" % self.db_column
        if self.primary_key and self.field_class is not PrimaryKeyField:
            params['primary_key'] = True

        # Handle ForeignKeyField-specific attributes.
        if self.is_foreign_key():
            params['rel_model'] = self.rel_model
            if self.to_field:
                params['to_field'] = "'%s'" % self.to_field
            if self.related_name:
                params['related_name'] = "'%s'" % self.related_name

        # Handle indexes on column.
        if not self.is_primary_key():
            if self.unique:
                params['unique'] = 'True'
            elif self.index and not self.is_foreign_key():
                params['index'] = 'True'
        if self.help_text:
            params['help_text'] = "'%s'" % self.help_text
        return params

    def get_field(self):
        # Generate the field definition for this column.
        field_params = self.get_field_parameters()
        param_str = ', '.join('%s=%s' % (k, v)
                              for k, v in sorted(field_params.items()))
        field = '%s = %s(%s)' % (
            self.name,
            self.field_class.__name__,
            param_str)

        if self.field_class is UnknownField:
            field = '%s  # %s' % (field, self.raw_column_type)

        return field






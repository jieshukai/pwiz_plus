# -*- coding:utf-8 _*-
"""
@author:jieshukai
@file: zr_assets_log.py
@time: 2019/03/15
"""
from datetime import datetime, timedelta
from peewee import *
import calendar

database = MySQLDatabase('zr_test', **{'charset': 'utf8', 'use_unicode': True, 'user': 'root', 'password': 'root',
                                       'host': '127.0.0.1', 'port': 3306})


class BaseModel(Model):
    class Meta:
        database = database

    @classmethod
    def get_table_name(cls, tables):
        for i in tables:
            if cls._meta.db_table.startswith(i):
                return i

    @classmethod
    def get_table_by_date(cls, date: datetime):
        TABLE_NAME = cls.get_table_name(zr_assets_table.keys())
        divide_month = date.strftime('_%Y%m')
        cls._meta.db_table = TABLE_NAME + divide_month
        return cls


class UserIncomeCategory(BaseModel):
    # id = PrimaryKeyField()
    name = CharField(constraints=[SQL("DEFAULT ''")], help_text='分类名称')
    level = IntegerField(constraints=[SQL("DEFAULT 0")], help_text='分类级别')
    k_coin = IntegerField(constraints=[SQL("DEFAULT 0")], help_text='金币变化数量')
    bu_text1 = CharField(constraints=[SQL("DEFAULT ''")], help_text='备用字段1 满足条件，满赠时长or广告时长')
    gmt_create = DateTimeField(default=datetime.now(),
                               constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")]
                               )
    gmt_modified = DateTimeField(default=datetime.now(),
                                 constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")]
                                 )

    class Meta:
        db_table = 'user_income_category'


class UserPayoutCategory(BaseModel):
    # id = PrimaryKeyField()
    name = CharField(constraints=[SQL("DEFAULT ''")], help_text='分类名称')
    level = IntegerField(constraints=[SQL("DEFAULT 0")], help_text='分类级别')
    k_coin = IntegerField(constraints=[SQL("DEFAULT 0")], help_text='金币变化数量')
    bu_text1 = CharField(constraints=[SQL("DEFAULT ''")], help_text='备用字段1 满足条件，满赠时长or广告时长')
    gmt_create = DateTimeField(default=datetime.now(),
                               constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")],
                               help_text='创建时间'
                               )
    gmt_modified = DateTimeField(default=datetime.now(),
                                 constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")],
                                 help_text='修改时间'

                                 )

    class Meta:
        db_table = 'user_payout_category'


class UserTradeLog(BaseModel):
    # 交易信息
    # id = PrimaryKeyField()
    title = CharField(constraints=[SQL("DEFAULT ''")], help_text='交易标题or交易分类or交易商品')
    k_coin = IntegerField(constraints=[SQL("DEFAULT 0")], help_text='金币')
    user_id = IntegerField(help_text='用户ID', index=True)
    app_id = CharField(max_length=128, help_text='APP_ID', index=True)
    # 交易分类
    # 获取一级分类id
    is_income = IntegerField(help_text='1 获取 2 花费', constraints=[SQL("DEFAULT 0")])
    # 获取分类id
    category_id = IntegerField(constraints=[SQL("DEFAULT 0")],
                               help_text='1:阅读奖励7:首登奖励2:签到3:宝箱 4:任务 5金币兑钱6提现8提现失败10商品11赠送12分享13合力吃鸡', index=True)

    # 获取金额
    # 1. 阅读 奖励，7首登12分享，11满赠14看广告
    # 2. 签到奖励
    level = IntegerField(constraints=[SQL("DEFAULT 0")], help_text='级别')
    # 3. 微信或qq 二维码等 兑换
    # 10商品
    status = IntegerField(help_text='交易状态 1. 创建订单未支付，2. 已支付订单，3. 待确认收货，4.收货交易成功，5. 超时交易关闭',
                          constraints=[SQL("DEFAULT 0")])
    bu_int1 = IntegerField(help_text='备用_交易_三级分类_标记id', constraints=[SQL("DEFAULT 0")])
    bu_text1 = CharField(max_length=255, constraints=[SQL("DEFAULT ''")], help_text='备用文本字段')
    # 时间
    gmt_create = DateTimeField(help_text='创建时间', default=datetime.now(),
                               constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")]
                               )
    gmt_modified = DateTimeField(help_text='修改时间', default=datetime.now(),
                                 constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")]

                                 )

    class Meta:
        db_table = 'user_trade_log'
        # indexes = (
        #     (('id', 'gmt_create'), True),
        # )


zr_assets_table = {
    'user_trade_log': UserTradeLog,
}
zr_assets_sql = {
    'user_trade_log': """CREATE TABLE if not exists `{table_name}_{month}` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL DEFAULT '' COMMENT '交易标题or交易分类or交易商品',
  `k_coin` int(11) NOT NULL DEFAULT '0' COMMENT '金币',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `app_id` varchar(128) NOT NULL COMMENT 'APP_ID',
  `is_income` int(11) NOT NULL DEFAULT '0' COMMENT '1 获取 2 花费',
  `category_id` int(11) NOT NULL DEFAULT '0' COMMENT '1:阅读奖励7:首登奖励2:签到3:宝箱 4:任务 5金币兑钱6提现8提现失败10商品11赠送12分享13合力吃鸡',
  `level` int(11) NOT NULL DEFAULT '0' COMMENT '级别',
  `status` int(11) NOT NULL DEFAULT '0' COMMENT '交易状态 1. 创建订单未支付，2. 已支付订单，3. 待确认收货，4.收货交易成功，5. 超时交易关闭',
  `bu_int1` int(11) NOT NULL DEFAULT '0' COMMENT '备用_交易_三级分类_标记id',
  `bu_text1` varchar(255) NOT NULL DEFAULT '' COMMENT '备用文本字段1',
  `bu_text2` varchar(255) NOT NULL DEFAULT '' COMMENT '备用文本字段2',
  `gmt_create` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`,`gmt_create`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 
PARTITION BY RANGE (TO_DAYS(gmt_create))
("""
}


def get_partition_days(sql_items):
    partition = "PARTITION p_{day} VALUES LESS THAN ( TO_DAYS('{_day}' ))ENGINE = InnoDB,\n"
    for table_name, sql_tpl in sql_items:
        # 单个表处理
        for i in range(12):
            # 表数量为月数量数量
            dt_time = (datetime.now() + timedelta(days=30 * i))
            pre_sql = sql_tpl.format(table_name=table_name, month=dt_time.strftime('%Y%m'))

            # pre_sql = sql_tpl % table_name, divide_month
            days = calendar.Calendar().itermonthdates(dt_time.year, dt_time.month)
            for day in days:
                if day > datetime.now().date() and day.month == dt_time.month:
                    pre_sql += partition.format(day=str(day).replace('-', ''), _day=day)
            pre_sql = pre_sql[:-2] + ');'
            yield pre_sql
            del pre_sql


def create_partition_table(sql_items):
    res = get_partition_days(sql_items)
    for index, sql in enumerate(res):
        try:
            database.execute_sql(sql)
        except:
            print(index, '---', sql)


if __name__ == '__main__':
    # get_partition_days()
    create_partition_table(zr_assets_sql.items())
    # print(UserTradeLog.create_table())
    # UserIncomeCategory.create_table()
    # UserPayoutCategory.create_table()

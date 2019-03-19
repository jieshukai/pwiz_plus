# pwiz_plus
自动导出model 添加 help_text
目前只支持 MySQL
```python
from pwiz_plus.tpl import MysqlMakeModels

make_config = dict(
    db_type='mysql',
    db_name='db_name', #填写你的数据库名称
    # tables=['table1', 'table2'] #填写你想导出的表   
    tables=None) #不提供默认全部表
# 数据库 参数 
db_config = dict(user='root', password='root', host='127.0.0.1', port=3306)
if __name__ == '__main__':
    # 程序生成
    make_models = MysqlMakeModels(**make_config, **db_config)
    make_models.write_py_content('models.py', make_models.get_content())

```

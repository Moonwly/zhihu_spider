import pymysql

# 数据库相关配置
mysql_config = {
    # 'host': '106.15.204.111',
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'db': 'zhihu',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': True
}
app = {
    'port': 5002,   # 启动端口
    'host': '0.0.0.0',
    'debug': True,
}

db = {
    'host': '192.168.0.106',
    'port': 27017,
    'user': 'admin',
    'pwd': '1',
    # 连接数据库时权限校验的库名，没有账号密码则置为空
    'authSource': 'admin',
}

# 两张脸之间有多少距离才算匹配。该值越小对比越严格，0.6是典型的最佳值
SIMILARITY_TOLERANCE = 0.5

# 日志文件名
LOG_FILENAME = 'serverlog.log'

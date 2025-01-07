import os
from pymongo import MongoClient

def get_mongodb_client(host=None, port=None, username=None, password=None, database=None):
    """创建 MongoDB 客户端连接
    
    所有参数都可以从环境变量获取:
    - MONGO_HOST: MongoDB 主机地址
    - MONGO_PORT: MongoDB 端口
    - MONGO_USER: MongoDB 用户名
    - MONGO_PASSWORD: MongoDB 密码
    - MONGO_DATABASE: MongoDB 数据库名称
    """
    host = host or os.getenv('MONGO_HOST', 'localhost')
    port = port or os.getenv('MONGO_PORT', '27017')
    username = username or os.getenv('MONGO_USER')
    password = password or os.getenv('MONGO_PASSWORD')
    database = database or os.getenv('MONGO_DATABASE', 'genesis')

    if username and password:
        uri = f"mongodb://{username}:{password}@{host}:{port}/{database}"
    else:
        uri = f"mongodb://{host}:{port}/{database}"

    client = MongoClient(uri)
    return client

def get_mongodb_database(client=None, database=None):
    """获取 MongoDB 数据库实例"""
    if client is None:
        client = get_mongodb_client()
    database = database or os.getenv('MONGO_DATABASE', 'genesis')
    return client[database] 
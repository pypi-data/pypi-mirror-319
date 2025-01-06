import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def get_db_engine(host=None, port=None, user=None, password=None, database=None):
    """创建数据库引擎
    
    所有参数都可以从环境变量获取:
    - MYSQL_HOST: 数据库主机地址
    - MYSQL_PORT: 数据库端口
    - MYSQL_USER: 数据库用户名
    - MYSQL_PASSWORD: 数据库密码
    - MYSQL_DATABASE: 数据库名称
    """
    host = host or os.getenv('MYSQL_HOST', 'localhost')
    port = port or os.getenv('MYSQL_PORT', '3306')
    user = user or os.getenv('MYSQL_USER', 'genesis')
    password = password or os.getenv('MYSQL_PASSWORD', 'y5rw)a8H!g')
    database = database or os.getenv('MYSQL_DATABASE', 'genesis')

    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    return create_engine(url, pool_recycle=3600)

def get_db_session(engine):
    """创建数据库会话"""
    Session = sessionmaker(bind=engine)
    return Session() 
import os
from typing import Optional
from pymongo.database import Database
from sqlalchemy.orm import Session
from boto3 import client as boto3_client
from boto3 import resource as boto3_resource

from .connections import (
    get_db_engine, get_db_session,
    get_mongodb_client, get_mongodb_database,
    get_s3_client, get_s3_resource
)

class ProcessorTools:
    """处理器辅助工具类
    
    提供 MySQL 和 S3 等辅助功能
    """
    
    def __init__(self):
        self._db_session = None
        self._s3_client = None
        self._s3_resource = None
    
    def use_mysql(self) -> Session:
        """获取 MySQL 会话
        
        用于数据导出、备份等场景
        """
        if self._db_session is None:
            engine = get_db_engine()
            self._db_session = get_db_session(engine)
        return self._db_session
    
    def use_s3_client(self) -> boto3_client:
        """获取 S3 客户端
        
        用于文件上传、下载等场景
        """
        if self._s3_client is None:
            self._s3_client = get_s3_client()
        return self._s3_client
    
    def use_s3_resource(self) -> boto3_resource:
        """获取 S3 资源对象
        
        用于更高级的 S3 操作
        """
        if self._s3_resource is None:
            self._s3_resource = get_s3_resource()
        return self._s3_resource
    
    def cleanup(self):
        """清理辅助工具的资源连接"""
        if self._db_session:
            self._db_session.close()
            self._db_session = None
        
        # S3 客户端不需要显式关闭

class BaseProcessor:
    """基础处理器类
    
    专注于 MongoDB 数据库操作，通过 tools 属性提供辅助功能
    """
    
    def __init__(self, mongodb_database: Optional[str] = None):
        """初始化处理器
        
        Args:
            mongodb_database: MongoDB 数据库名称，如果为 None 则从环境变量获取
        """
        self._mongodb = get_mongodb_database(database=mongodb_database)
        self._tools = ProcessorTools()
    
    @property
    def mongodb(self) -> Database:
        """获取 MongoDB 数据库实例"""
        return self._mongodb
    
    @property
    def tools(self) -> ProcessorTools:
        """获取辅助工具实例"""
        return self._tools

    def cleanup(self):
        """清理资源连接"""
        if self._mongodb:
            self._mongodb.client.close()
            self._mongodb = None
        
        if self._tools:
            self._tools.cleanup()
            self._tools = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup() 
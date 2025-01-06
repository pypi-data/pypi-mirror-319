from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Document(BaseModel):
    """文档基础模型类
    
    提供通用的文档属性和方法，可用于各种数据存储（MongoDB、Redis、ElasticSearch等）
    """
    
    id: Optional[str] = Field(None, alias="_id")  # 文档ID，MongoDB中为_id
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True  # 允许使用字段名而不是别名
        json_encoders = {
            datetime: lambda v: v.isoformat()  # 日期时间序列化为 ISO 格式
        }
    
    def update_timestamp(self):
        """更新时间戳"""
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """转换为字典，用于存储"""
        return self.dict(by_alias=True)
    
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建实例"""
        return cls.parse_obj(data) 
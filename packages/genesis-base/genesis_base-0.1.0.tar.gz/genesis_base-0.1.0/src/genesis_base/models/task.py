from datetime import datetime
from typing import Optional, Dict, Any, List, ClassVar, Type, TypeVar
from pydantic import Field
from pymongo.database import Database
from pymongo.collection import Collection
from .base import Document

T = TypeVar('T', bound='GenesisTaskModel')

class GenesisTaskModel(Document):
    """基础任务模型"""
    
    # 集合名称，子类必须覆盖
    COLLECTION_NAME: ClassVar[str] = None
    
    # 任务ID作为主键
    task_id: str = Field(..., description="任务ID")
    
    # 基本信息
    name: str = Field(..., description="任务名称")
    description: Optional[str] = Field(None, description="任务描述")
    
    @classmethod
    def get_collection(cls, db: Database) -> Collection:
        """获取对应的 MongoDB collection
        
        每个任务类型对应不同的 collection
        """
        if cls.COLLECTION_NAME is None:
            raise NotImplementedError(f"{cls.__name__} must define COLLECTION_NAME")
        return db[cls.COLLECTION_NAME]
    
    @classmethod
    def load(cls: Type[T], db: Database, task_id: str) -> Optional[T]:
        """从数据库加载任务"""
        collection = cls.get_collection(db)
        data = collection.find_one({"task_id": task_id})
        return cls.from_dict(data) if data else None
    
    def save(self, db: Database) -> str:
        """保存任务到数据库"""
        collection = self.get_collection(db)
        self.update_timestamp()  # 更新时间戳
        data = self.to_dict()
        
        # 使用 task_id 作为查询条件
        collection.update_one(
            {"task_id": self.task_id},
            {"$set": data},
            upsert=True
        )
        return self.task_id

class PretrainTask(GenesisTaskModel):
    """预训练任务模型"""
    
    # 明确指定集合名称
    COLLECTION_NAME: ClassVar[str] = "pretrain_tasks"
    
    # 视频相关路径
    source_video_path: str = Field(..., description="原始素材视频路径")
    reference_video_path: str = Field(..., description="参考素材视频路径")
    video_model_path: str = Field(..., description="视频模型路径")
    
    # 音频相关路径
    reference_audio_path: str = Field(..., description="参考素材音频路径")
    audio_model_path: str = Field(..., description="音频模型路径")

class ProductTask(GenesisTaskModel):
    """成品任务模型"""
    
    # 明确指定集合名称
    COLLECTION_NAME: ClassVar[str] = "product_tasks"
    
    # 音频相关
    audio_model_path: str = Field(..., description="音频模型路径")
    reference_audio_path: str = Field(..., description="参考素材音频路径")
    target_text: str = Field(..., description="目标台词")
    output_audio_path: Optional[str] = Field(None, description="合成成品音频路径")
    
    # 视频相关
    video_model_path: str = Field(..., description="视频模型路径")
    output_video_path: Optional[str] = Field(None, description="合成成品视频路径") 
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置类，统一管理所有配置项"""
    
    # MySQL配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'genesis')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    
    @classmethod
    def get_mysql_url(cls):
        return (f"mysql+pymysql://{cls.MYSQL_USER}:{cls.MYSQL_PASSWORD}"
                f"@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DATABASE}")
    
    # MongoDB配置
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'genesis')
    MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION', 'tasks')
    MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
    MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
    
    @classmethod
    def get_mongodb_uri(cls):
        if cls.MONGODB_USERNAME and cls.MONGODB_PASSWORD:
            if '://' in cls.MONGODB_URI:
                protocol, rest = cls.MONGODB_URI.split('://', 1)
                return f"{protocol}://{cls.MONGODB_USERNAME}:{cls.MONGODB_PASSWORD}@{rest}"
            return f"mongodb://{cls.MONGODB_USERNAME}:{cls.MONGODB_PASSWORD}@{cls.MONGODB_URI}"
        return cls.MONGODB_URI 
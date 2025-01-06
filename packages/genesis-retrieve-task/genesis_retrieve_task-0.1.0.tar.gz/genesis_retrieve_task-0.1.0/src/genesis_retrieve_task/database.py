from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import Config

def get_db_session():
    """获取数据库会话"""
    engine = create_engine(
        Config.get_mysql_url(),
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False
    )
    Session = sessionmaker(bind=engine)
    return Session() 
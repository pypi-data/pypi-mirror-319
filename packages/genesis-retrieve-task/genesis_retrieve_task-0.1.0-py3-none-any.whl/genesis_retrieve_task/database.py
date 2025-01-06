from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from genesis_base.database import get_db_url

def get_db_session():
    """获取数据库会话"""
    db_url = get_db_url()
    
    # 创建引擎
    engine = create_engine(db_url)
    
    # 创建会话工厂
    Session = sessionmaker(bind=engine)
    
    # 返回新的会话
    return Session() 
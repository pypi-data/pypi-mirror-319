import os
import sys
import json
import logging
from typing import Dict
from datetime import datetime, UTC
from sqlalchemy import text
from pymongo import MongoClient
from dotenv import load_dotenv
from .config import Config
from genesis_base.models import TaskModel, MaterialModel

# 加载.env文件（如果存在）
load_dotenv()

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 添加项目根目录到 Python 路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from genesis_retrieve_task.database import get_db_session

class TaskRetriever:
    def __init__(self):
        # 使用配置类初始化MongoDB连接
        mongo_uri = Config.get_mongodb_uri()
        
        # 初始化MongoDB连接
        self.mongo_client = MongoClient(mongo_uri)
        self.mongo_db = self.mongo_client[Config.MONGODB_DATABASE]
        self.mongo_collection = self.mongo_db[Config.MONGODB_COLLECTION]

    def get_mongo_task(self, task_id: int) -> Dict:
        """从MongoDB获取指定task_id的任务信息"""
        task = self.mongo_collection.find_one({"task_id": task_id})
        if not task:
            # 如果在MongoDB中找不到该任务，创建一个新的任务记录
            task = {
                "task_id": task_id,
                "status": "processing",
                "created_at": datetime.now(UTC)
            }
            self.mongo_collection.insert_one(task)
        return task

    def update_mongo_task(self, task_id: int, result: Dict) -> None:
        """更新MongoDB中的任务结果"""
        self.mongo_collection.update_one(
            {"task_id": task_id},
            {
                "$set": {
                    "status": "completed",
                    "result": result,
                    "updated_at": datetime.now(UTC)
                }
            }
        )

    def get_task(self, task_id: int) -> Dict:
        """获取任务信息"""
        session = get_db_session()
        try:
            task = session.query(TaskModel).join(
                MaterialModel,
                TaskModel.material_id == MaterialModel.material_id
            ).filter(
                TaskModel.task_id == task_id,
                TaskModel.deleted == 0
            ).first()
            
            if not task:
                return {
                    "success": False,
                    "error": f"Task {task_id} not found"
                }
            
            task_dict = {
                "task_id": task.task_id,
                "task_name": task.task_name,
                "task_text": task.task_text,
                "material_path": task.material.material_path,
                "task_status": task.task_status
            }
            
            response = {
                "success": True,
                "data": task_dict
            }
            
            return response
        finally:
            session.close()

    def update_task_status(self, task_id: int, status: int) -> Dict:
        """更新任务状态"""
        session = get_db_session()
        try:
            task = session.query(TaskModel).filter_by(
                task_id=task_id, 
                deleted=0
            ).first()
            
            if not task:
                return {
                    "success": False,
                    "error": f"Task {task_id} not found"
                }
            
            task.task_status = status
            task.update_time = datetime.now(UTC)
            
            session.commit()
            return {"success": True}
        except Exception as e:
            session.rollback()
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            session.close()

def main():
    try:
        # 从环境变量获取task_id
        task_id = os.getenv('TASK_ID')
        if not task_id:
            logging.error("TASK_ID environment variable is required")
            sys.exit(1)
        
        task_id = int(task_id)
        retriever = TaskRetriever()
        
        # 获取或创建MongoDB中的任务记录
        mongo_task = retriever.get_mongo_task(task_id)
        status = os.getenv('TASK_STATUS')
        if status:
            status = int(status)
            
        if status is not None:
            # 更新任务状态
            result = retriever.update_task_status(task_id, status)
            if not result["success"]:
                logging.error(json.dumps({"error": result['error']}))
                sys.exit(1)
            # 更新MongoDB中的任务状态
            retriever.update_mongo_task(task_id, result)
            logging.info(json.dumps({"message": f"Task {task_id} status updated to {status}"}))
        else:
            # 获取任务信息
            result = retriever.get_task(task_id)
            if not result["success"]:
                logging.error(json.dumps({"error": result['error']}))
                sys.exit(1)
            # 更新MongoDB中的任务信息
            retriever.update_mongo_task(task_id, result)
            logging.info(json.dumps({"task_info": result['data']}))

    except Exception as e:
        logging.error(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main() 
# genesis-retrieve-task

Task retrieval component for Genesis video processing pipeline.

## Description
Retrieves task information from the database based on task ID.

## Installation
```bash
pip install git+https://github.com/stevenge-godscode/genesis-retrieve-task.git
```

## Usage
```python
from genesis_retrieve_task.processor import TaskRetriever

retriever = TaskRetriever()
result = retriever.get_task(task_id=123)
```

## Database Schema
```sql
-- task_info table
CREATE TABLE task_info (
    task_id INT PRIMARY KEY AUTO_INCREMENT,
    task_name VARCHAR(50),
    task_text VARCHAR(100) NOT NULL,
    user_id INT NOT NULL,
    material_id INT NOT NULL,
    task_status TINYINT NOT NULL DEFAULT 0,
    subscribe_flag TINYINT DEFAULT 0,
    template_id VARCHAR(100),
    deleted TINYINT DEFAULT 0,
    create_user VARCHAR(20),
    create_time DATETIME,
    update_user VARCHAR(20),
    update_time DATETIME
);

-- material_info table (referenced)
CREATE TABLE material_info (
    material_id INT PRIMARY KEY AUTO_INCREMENT,
    material_path VARCHAR(100) NOT NULL
    -- other fields...
);
```

## API
### get_task(task_id: int)
Returns task information including:
- task_id
- task_name
- task_text
- material_path
- task_status

### update_task_status(task_id: int, status: int)
Updates task status. Available statuses:
- 0: PENDING
- 1: PROCESSING
- 2: COMPLETED
- 3: FAILED

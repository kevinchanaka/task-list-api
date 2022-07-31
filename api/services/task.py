import uuid
from datetime import datetime, timezone
from api.database import task_db
from api.exceptions import InvalidUsageError
from api.models import task_output_schema, Task


class TaskService:
    def create_task(self, task: Task):
        task.id = uuid.uuid4()
        task.completed = False
        task.created_at = datetime.now(timezone.utc)
        task.updated_at = task.created_at
        task_db.add(task)
        created_task = task_db.get(user_id=task.user_id, id=task.id)
        return {
            "task": task_output_schema.dump(created_task),
            "message": "Task added",
        }

    def get_task(self, user_id: str, task_id: str):
        task = task_db.get(user_id=user_id, id=task_id)
        if not task:
            raise InvalidUsageError("Task not found")
        return {"task": task_output_schema.dump(task)}

    def list_tasks(self, user_id: str):
        tasks = task_db.list(user_id=user_id)
        return {"tasks": [task_output_schema.dump(x) for x in tasks]}

    def delete_task(self, user_id: str, task_id: str):
        success = task_db.delete(user_id=user_id, id=task_id)
        if not success:
            raise InvalidUsageError("Task not found")
        return {"message": "Task deleted"}

    def update_task(self, task: Task):
        task.updated_at = datetime.now(timezone.utc)
        success = task_db.update(task, user_id=task.user_id, id=task.id)
        if not success:
            raise InvalidUsageError("Task not found")
        updated_task = task_db.get(user_id=task.user_id, id=task.id)
        return {
            "task": task_output_schema.dump(updated_task),
            "message": "Task modified",
        }

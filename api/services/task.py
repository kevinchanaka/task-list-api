from api.models import Task, TaskSchema
from api.database import task_db
from api.exceptions import InvalidUsageError


class TaskService:
    def __init__(self):
        self.task_schema = TaskSchema()
        self.task_schema_no_user = TaskSchema(exclude=("user_id",))

    def create_task(self, task: Task):
        task_db.add(task)
        return {"task": task.serialise_public()}

    def get_task(self, user_id: str, task_id: str):
        task = task_db.get(user_id=user_id, id=task_id)
        if not task:
            raise InvalidUsageError("Task not found")
        return {"task": task.serialise_public()}

    def list_tasks(self, user_id: str):
        tasks = task_db.list(user_id=user_id)
        return {"tasks": [x.serialise_public() for x in tasks]}

    def delete_task(self, user_id: str, task_id: str):
        success = task_db.delete(user_id=user_id, id=task_id)
        if not success:
            raise InvalidUsageError("Task not found")
        return {"message": "Task deleted"}

    def update_task(self, task: Task):
        success = task_db.update(task, user_id=task.user_id, id=task.id)
        if not success:
            raise InvalidUsageError("Task not found")
        return {"task": task.serialise_public()}

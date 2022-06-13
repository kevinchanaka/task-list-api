import uuid
from api.models import task_model
from api.exceptions import InvalidUsageError


class TaskService:
    def __init__(self):
        pass

    @staticmethod
    def __make_task__(data):
        return {
            "id": uuid.uuid4().__str__(),
            "user_id": data["user_id"],
            "name": data["name"],
            "description": data["description"],
        }

    @staticmethod
    def __remove_user_id__(task):
        return {k: task[k] for k in task.keys() if k != "user_id"}

    def create_task(self, user_id: str, data):
        task = self.__make_task__({"user_id": user_id, **data})
        task_model.add(task)
        return {"task": self.__remove_user_id__(task)}

    def update_task(self, user_id: str, task_id: str, data):
        success = task_model.update({"user_id": user_id, "id": task_id}, data)
        if not success:
            raise InvalidUsageError("Task not found")
        return {"task": {"id": task_id, **data}}

    def delete_task(self, user_id: str, task_id: str):
        success = task_model.delete({"user_id": user_id, "id": task_id})
        if not success:
            raise InvalidUsageError("Task not found")
        return {"message": "Task deleted"}

    def list_tasks(self, user_id: str):
        tasks = task_model.list({"user_id": user_id})
        tasks = [self.__remove_user_id__(x) for x in tasks]
        return {"tasks": tasks}

    def get_task(self, user_id: str, task_id: str):
        task = task_model.get({"user_id": user_id, "id": task_id})
        if not task:
            raise InvalidUsageError("Task not found")
        return {"task": self.__remove_user_id__(task)}

import uuid
from datetime import datetime, timezone
from api.database import task_db, label_db, task_label_db
from api.services import label_service
from api.exceptions import InvalidUsageError
from api.schemas import (
    task_schema,
    task_get_schema,
    task_list_schema,
    label_list_schema,
)
from api.models import Task


def create_task(task: Task):
    task.id = uuid.uuid4()
    task.completed = False
    task.created_at = datetime.now(timezone.utc)
    task.updated_at = task.created_at
    task_db.add(task_schema.dump(task))
    created_task = task_db.get(user_id=task.user_id, id=task.id)
    return task_get_schema.dump(created_task)


def get_task(user_id: str, task_id: str):
    task = task_db.get(user_id=user_id, id=task_id)
    if not task:
        raise InvalidUsageError("Task not found")
    labels = label_db.list_relationship("task_labels", task_id)
    return {
        **task_get_schema.dump(task),
        "labels": [label_list_schema.dump(x) for x in labels],
    }


def list_tasks(user_id: str):
    output = []
    for item in task_db.list(user_id=user_id):
        task = task_list_schema.dump(item)
        labels = label_db.list_relationship("task_labels", task["id"])
        task["labels"] = [label_list_schema.dump(x) for x in labels]
        output.append(task)
    return output


def delete_task(user_id: str, task_id: str):
    get_task(user_id, task_id)
    task_db.delete(user_id=user_id, id=task_id)


def update_task(task: Task):
    task.updated_at = datetime.now(timezone.utc)
    success = task_db.update(task_schema.dump(task), user_id=task.user_id, id=task.id)
    if not success:
        raise InvalidUsageError("Task not found")
    updated_task = task_db.get(user_id=task.user_id, id=task.id)
    return task_get_schema.dump(updated_task)


def attach_label_to_task(user_id: str, label_id: str, task_id: str):
    task = get_task(user_id, task_id)
    label = label_service.get_label(user_id, label_id)
    if task_label_db.get(task_id=task["id"], label_id=label["id"]):
        raise InvalidUsageError("Label already attached to task")
    task_label_db.add(
        {
            "task_id": task["id"],
            "label_id": label["id"],
        }
    )


def detach_label_from_task(user_id: str, label_id: str, task_id: str):
    get_task(user_id, task_id)
    label_service.get_label(user_id, label_id)
    if not task_label_db.get(task_id=task_id, label_id=label_id):
        raise InvalidUsageError("Label not attached to task")
    task_label_db.delete(task_id=task_id, label_id=label_id)

import uuid
from datetime import datetime, timezone
from api.services import label_service
from api.exceptions import InvalidUsageError
from api.models import Task, db
from sqlalchemy import select
from typing import List


def create_task(task: Task):
    task.id = uuid.uuid4()
    task.completed = False
    task.created_at = datetime.now(timezone.utc)
    task.updated_at = task.created_at
    db.session.add(task)
    db.session.commit()


def get_task(user_id: str, task_id: str) -> Task:
    query = select(Task).where(Task.user_id == user_id, Task.id == task_id)
    task = db.session.execute(query).scalars().first()
    if not task:
        raise InvalidUsageError("Task not found")
    return task


def list_tasks(user_id: str):
    query = select(Task).where(Task.user_id == user_id)
    tasks = db.session.execute(query).scalars().all()
    return tasks


def delete_task(user_id: str, task_id: str):
    task = get_task(user_id, task_id)
    db.session.delete(task)
    db.session.commit()


def update_task(user_id: str, task_id: str, data: dict):
    task = get_task(user_id, task_id)
    for k, v in data.items():
        setattr(task, k, v)
    task.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    return task


def attach_labels_to_task(user_id: str, labels: List[str], task_id: str):
    task = get_task(user_id, task_id)
    task.updated_at = datetime.now(timezone.utc)
    for label_id in labels:
        label = label_service.get_label(user_id, label_id)
        task.labels.append(label)
    db.session.commit()


def detach_labels_from_task(user_id: str, labels: List[str], task_id: str):
    task = get_task(user_id, task_id)
    task.updated_at = datetime.now(timezone.utc)
    for label_id in labels:
        label = label_service.get_label(user_id, label_id)
        task.labels = [x for x in task.labels if x.id != label.id]
    db.session.commit()

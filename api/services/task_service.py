import uuid
from datetime import datetime, timezone
from api.services import label_service
from api.exceptions import InvalidUsageError
from api.models import Task, db, Label, TaskLabelAssociation, TaskQuery
from sqlalchemy import select, func


def create_task(user_id: str, task: Task):
    task.id = uuid.uuid4()
    task.completed = False
    task.created_at = datetime.now(timezone.utc)
    task.updated_at = task.created_at
    task.user_id = user_id
    db.session.add(task)
    db.session.commit()


def get_task(user_id: str, task_id: str) -> Task:
    query = select(Task).where(Task.user_id == user_id, Task.id == task_id)
    task = db.session.execute(query).scalars().first()
    if not task:
        raise InvalidUsageError("Task not found")
    return task


def list_tasks(user_id: str, task_query: TaskQuery):
    offset = (task_query.page - 1) * task_query.limit
    query = (
        select(Task)
        .where(Task.user_id == user_id)
        .limit(task_query.limit)
        .offset(offset)
        .order_by(Task.updated_at.desc())
    )
    for label_id in task_query.label:
        query = query.where(Task.labels.any(Label.id == label_id))

    tasks = db.session.execute(query).scalars().all()

    query = select(func.count(Task.id)).where(Task.user_id == user_id)
    for label_id in task_query.label:
        query = query.where(Task.labels.any(Label.id == label_id))

    rowcount = db.session.execute(query).first()[0]

    return tasks, rowcount


def delete_task(user_id: str, task_id: str):
    task = get_task(user_id, task_id)
    db.session.delete(task)
    db.session.commit()


def update_task(user_id: str, task_id: str, task_obj: Task):
    task = get_task(user_id, task_id)
    task.name = task_obj.name
    task.description = task_obj.description
    task.completed = task_obj.completed
    task.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    return task


def attach_labels_to_task(user_id: str, data: TaskLabelAssociation):
    task = get_task(user_id, data.task_id)
    task.updated_at = datetime.now(timezone.utc)
    for label_id in data.label_ids:
        label = label_service.get_label(user_id, label_id)
        task.labels.append(label)
    db.session.commit()


def detach_labels_from_task(user_id: str, data: TaskLabelAssociation):
    task = get_task(user_id, data.task_id)
    task.updated_at = datetime.now(timezone.utc)
    for label_id in data.label_ids:
        label = label_service.get_label(user_id, str(label_id))
        task.labels = [x for x in task.labels if x.id != label.id]
    db.session.commit()

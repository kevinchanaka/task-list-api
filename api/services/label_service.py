import uuid
from datetime import datetime, timezone
from api.database import label_db, task_label_db
from api.exceptions import InvalidUsageError
from api.schemas import label_schema, label_get_schema, label_list_schema
from api.models import Label


def create_label(label: Label):
    label.id = uuid.uuid4()
    label.created_at = datetime.now(timezone.utc)
    label.updated_at = label.created_at
    label_db.add(label_schema.dump(label))
    created_label = label_db.get(user_id=label.user_id, id=label.id)
    return label_get_schema.dump(created_label)


def get_label(user_id: str, label_id: str):
    label = label_db.get(user_id=user_id, id=label_id)
    if not label:
        raise InvalidUsageError("Label not found")
    return label_get_schema.dump(label)


def list_labels(user_id: str):
    labels = label_db.list(user_id=user_id)
    return [label_list_schema.dump(x) for x in labels]


def delete_label(user_id: str, label_id: str):
    get_label(user_id, label_id)
    task_label_db.delete(label_id=label_id)
    label_db.delete(user_id=user_id, id=label_id)
    

def update_label(label: Label):
    label.updated_at = datetime.now(timezone.utc)
    success = label_db.update(
        label_schema.dump(label), user_id=label.user_id, id=label.id
    )
    if not success:
        raise InvalidUsageError("Label not found")
    updated_label = label_db.get(user_id=label.user_id, id=label.id)
    return label_get_schema.dump(updated_label)

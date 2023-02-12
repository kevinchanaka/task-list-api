import uuid
from datetime import datetime, timezone
from api.exceptions import InvalidUsageError
from api.models import Label, db
from sqlalchemy import select, func


def create_label(label: Label):
    label.id = uuid.uuid4()
    label.created_at = datetime.now(timezone.utc)
    label.updated_at = label.created_at
    db.session.add(label)
    db.session.commit()


def get_label(user_id: str, label_id: str) -> Label:
    query = select(Label).where(Label.id == label_id).where(Label.user_id == user_id)
    label = db.session.execute(query).scalars().first()
    if not label:
        raise InvalidUsageError("Label not found")
    return label


def list_labels(user_id: str, params: dict):
    offset = (params["page"] - 1) * params["limit"]
    query = (
        select(Label)
        .where(Label.user_id == user_id)
        .limit(params["limit"])
        .offset(offset)
        .order_by(Label.updated_at.desc())
    )
    labels = db.session.execute(query).scalars().all()

    query = select(func.count(Label.id)).where(Label.user_id == user_id)

    rowcount = db.session.execute(query).first()[0]

    return labels, rowcount


def delete_label(user_id: str, label_id: str):
    # TODO: fix minor bug, label deletion does not change task update time
    label = get_label(user_id, label_id)
    db.session.delete(label)
    db.session.commit()


def update_label(user_id: str, label_id: str, data: dict) -> Label:
    label = get_label(user_id, label_id)
    for k, v in data.items():
        setattr(label, k, v)
    label.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    return label

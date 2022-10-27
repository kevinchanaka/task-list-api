from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Table
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

tasks_labels_map = Table(
    "tasks_labels_map",
    db.metadata,
    Column("id", sa.Integer, primary_key=True, autoincrement=True),
    Column("label_id", sa.String, ForeignKey("labels.id")),
    Column("task_id", sa.String, ForeignKey("tasks.id")),
)


class Task(db.Model):
    __tablename__ = "tasks"
    id = Column(sa.Integer, primary_key=True)
    name = Column(sa.String, nullable=False)
    description = Column(sa.String, nullable=False)
    user_id = Column(sa.String, ForeignKey("users.id"))
    completed = Column(sa.Boolean, nullable=False)
    created_at = Column(sa.String, nullable=False)
    updated_at = Column(sa.String, nullable=False)

    labels = relationship("Label", secondary=tasks_labels_map, back_populates="tasks")


class Token(db.Model):
    __tablename__ = "refresh_tokens"
    token = Column(sa.String, primary_key=True)
    expiry = Column(sa.String, nullable=False)


class User(db.Model):
    __tablename__ = "users"
    id = Column(sa.String, primary_key=True)
    name = Column(sa.String, nullable=False)
    email = Column(sa.String, nullable=False)
    password_hash = Column(sa.String, nullable=False)
    password = None

    tasks = relationship("Task")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"


class Label(db.Model):
    __tablename__ = "labels"
    id = Column(sa.String, primary_key=True)
    name = Column(sa.String, nullable=False)
    colour = Column(sa.String, nullable=False)
    user_id = Column(sa.String, ForeignKey("users.id"))
    created_at = Column(sa.String, nullable=False)
    updated_at = Column(sa.String, nullable=False)

    tasks = relationship("Task", secondary=tasks_labels_map, back_populates="labels")

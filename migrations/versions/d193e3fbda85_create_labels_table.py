"""create labels tables

Revision ID: d193e3fbda85
Revises: 576c8d9334a5
Create Date: 2022-08-03 08:53:15.477062

"""
from alembic import op
import sqlalchemy as sa
from api.config import UUID_LENGTH, NAME_LENGTH


# revision identifiers, used by Alembic.
revision = "d193e3fbda85"
down_revision = "576c8d9334a5"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "labels",
        sa.Column("id", sa.String(UUID_LENGTH), primary_key=True),
        sa.Column("name", sa.String(NAME_LENGTH), nullable=False),
        sa.Column("colour", sa.String(7), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("user_id", sa.String(UUID_LENGTH), nullable=False),
    )
    op.create_foreign_key("fk_labels_user_id", "labels", "users", ["user_id"], ["id"])

    op.create_table(
        "tasks_labels_map",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("label_id", sa.String(UUID_LENGTH), nullable=False),
        sa.Column("task_id", sa.String(UUID_LENGTH), nullable=False),
    )
    op.create_foreign_key(
        "fk_tasks_labels_map_label_id",
        "tasks_labels_map",
        "labels",
        ["label_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_tasks_labels_map_task_id", "tasks_labels_map", "tasks", ["task_id"], ["id"]
    )


def downgrade():
    op.drop_constraint(
        "fk_tasks_labels_map_task_id", "tasks_labels_map", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_tasks_labels_map_label_id", "tasks_labels_map", type_="foreignkey"
    )
    op.drop_constraint("fk_labels_user_id", "labels", type_="foreignkey")
    op.drop_table("tasks_labels_map")
    op.drop_table("labels")

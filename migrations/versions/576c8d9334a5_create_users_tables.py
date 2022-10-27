"""create users tables

Revision ID: 576c8d9334a5
Revises: 51b73841aae6
Create Date: 2022-05-25 08:24:28.391844

"""
from alembic import op
import sqlalchemy as sa
from api.config import (
    UUID_LENGTH,
    NAME_LENGTH,
    HASH_LENGTH,
    DEFAULT_LENGTH,
    TIMESTAMP_LENGTH,
)


# revision identifiers, used by Alembic.
revision = "576c8d9334a5"
down_revision = "51b73841aae6"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.String(UUID_LENGTH), primary_key=True),
        sa.Column("name", sa.String(NAME_LENGTH), nullable=False),
        sa.Column("email", sa.String(NAME_LENGTH), nullable=False),
        sa.Column("password_hash", sa.String(HASH_LENGTH), nullable=False),
    )

    op.add_column("tasks", sa.Column("user_id", sa.String(UUID_LENGTH), nullable=False))
    op.create_foreign_key("fk_tasks_user_id", "tasks", "users", ["user_id"], ["id"])

    op.create_table(
        "refresh_tokens",
        sa.Column("token", sa.String(DEFAULT_LENGTH), primary_key=True, nullable=False),
        sa.Column("expiry", sa.String(TIMESTAMP_LENGTH), nullable=False),
    )


def downgrade():
    op.drop_constraint("fk_tasks_user_id", "tasks", type_="foreignkey")
    op.drop_column("tasks", "user_id")
    op.drop_table("refresh_tokens")
    op.drop_table("users")

"""create tasks table

Revision ID: 51b73841aae6
Revises: 
Create Date: 2022-05-19 08:53:42.595075

"""
from alembic import op
import sqlalchemy as sa

from api.config import UUID_LENGTH, NAME_LENGTH, DEFAULT_LENGTH


# revision identifiers, used by Alembic.
revision = "51b73841aae6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "tasks",
        sa.Column("id", sa.String(UUID_LENGTH), primary_key=True),
        sa.Column("name", sa.String(NAME_LENGTH), nullable=False),
        sa.Column("description", sa.String(DEFAULT_LENGTH), nullable=False),
    )


def downgrade():
    op.drop_table("tasks")

"""add last_changed column to user

Revision ID: 6c589bf489b8
Revises: 360776d91d7a
Create Date: 2022-03-23 12:31:06.470070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c589bf489b8'
down_revision = '360776d91d7a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users",sa.Column("last_changed",sa.DateTime))


def downgrade():
    op.drop_column("users", "last_changed")
"""add_active_column_to_pages_keywords

Revision ID: 2f50fa9f7941
Revises: c277c72b5e06
Create Date: 2022-05-03 23:05:10.006716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f50fa9f7941'
down_revision = 'c277c72b5e06'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("pages",sa.Column("active",sa.Boolean))
    op.add_column("keywords",sa.Column("active",sa.Boolean))


def downgrade():
    op.drop_column("pages", "active")
    op.drop_column("keywords", "active")
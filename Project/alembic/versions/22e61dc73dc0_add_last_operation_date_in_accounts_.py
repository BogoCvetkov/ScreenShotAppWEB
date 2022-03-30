"""add last operation date in accounts table

Revision ID: 22e61dc73dc0
Revises: 6c589bf489b8
Create Date: 2022-03-29 12:02:57.385364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22e61dc73dc0'
down_revision = '6c589bf489b8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("accounts", sa.Column("last_scraped", sa.DateTime))
    op.add_column("accounts", sa.Column("last_emailed", sa.DateTime))


def downgrade():
    op.drop_column("accounts", "last_scraped")
    op.drop_column("accounts", "last_emailed")
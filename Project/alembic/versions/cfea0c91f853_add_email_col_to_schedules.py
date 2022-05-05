"""add_email_col_to_schedules

Revision ID: cfea0c91f853
Revises: 2f50fa9f7941
Create Date: 2022-05-05 10:37:39.134341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfea0c91f853'
down_revision = '2f50fa9f7941'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("schedules", sa.Column("email", sa.String))


def downgrade():
    op.drop_column("schedules", "email")
"""add_country_col_to_acc_table

Revision ID: 591d0c1e7ec5
Revises: cfea0c91f853
Create Date: 2022-05-16 08:23:54.052689

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '591d0c1e7ec5'
down_revision = 'cfea0c91f853'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("accounts",sa.Column("country",sa.String))


def downgrade():
    op.drop_column("accounts", "country")
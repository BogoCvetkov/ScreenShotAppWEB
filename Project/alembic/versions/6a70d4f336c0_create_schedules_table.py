"""create schedules table

Revision ID: 6a70d4f336c0
Revises: 22e61dc73dc0
Create Date: 2022-04-05 18:04:13.395704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a70d4f336c0'
down_revision = '22e61dc73dc0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("schedules",
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("day", sa.Integer),
                    sa.Column("hour", sa.Integer),
                    sa.Column("account_id", sa.Integer,
                              sa.ForeignKey("accounts.id", ondelete="CASCADE"),
                              nullable=False)
                    )


def downgrade():
    op.drop_table('schedules')
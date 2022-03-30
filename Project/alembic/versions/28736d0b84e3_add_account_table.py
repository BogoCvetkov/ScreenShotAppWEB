"""add account Table

Revision ID: 28736d0b84e3
Revises: c76339936dc9
Create Date: 2022-03-03 15:42:36.315334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28736d0b84e3'
down_revision = 'c76339936dc9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table( "accounts",
                     sa.Column( "id", sa.Integer, primary_key=True ),
                     sa.Column( "name", sa.String,nullable=False ),
                     sa.Column( "email", sa.String, unique=True, nullable=False ),
                     sa.Column( "email_body", sa.String ),
                     sa.Column( "active", sa.Boolean, default=True )
                     )


def downgrade():
    op.drop_table("accounts")
"""add pages  Table

Revision ID: 93eb863789cf
Revises: 28736d0b84e3
Create Date: 2022-03-03 15:55:18.657266

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '93eb863789cf'
down_revision = '28736d0b84e3'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table( "pages",
	                 sa.Column( "id", sa.Integer, primary_key=True ),
	                 sa.Column( "name", sa.String, nullable=False ),
	                 sa.Column( "page_id", sa.String, nullable=False ),
	                 sa.Column( "account_id", sa.Integer, sa.ForeignKey( "accounts.id", ondelete="CASCADE" ),
	                            nullable=False ),
	                 )


def downgrade():
	op.drop_table('pages')
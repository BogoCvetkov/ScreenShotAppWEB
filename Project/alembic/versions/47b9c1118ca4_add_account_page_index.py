"""add account_page Index

Revision ID: 47b9c1118ca4
Revises: 93eb863789cf
Create Date: 2022-03-03 16:12:21.996797

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '47b9c1118ca4'
down_revision = '93eb863789cf'
branch_labels = None
depends_on = None


def upgrade():
	op.create_index( index_name="account_page_index", table_name="pages", columns=["account_id", "page_id"],
	                 unique=True )


def downgrade():
	op.drop_index( index_name="account_page_index", table_name="pages" )
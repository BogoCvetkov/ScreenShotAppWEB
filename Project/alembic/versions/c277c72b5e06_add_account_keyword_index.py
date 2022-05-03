"""add_account_keyword_index

Revision ID: c277c72b5e06
Revises: 55491a17d36d
Create Date: 2022-05-03 21:59:11.550771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c277c72b5e06'
down_revision = '55491a17d36d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(index_name="account_keyword_index", table_name="keywords", columns=["account_id", "keyword"],
                    unique=True)


def downgrade():
    op.create_index(index_name="account_keyword_index", table_name="keywords", columns=["account_id", "keyword"],
                    unique=True)
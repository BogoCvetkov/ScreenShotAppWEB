"""create_keywords_table

Revision ID: 55491a17d36d
Revises: 6a70d4f336c0
Create Date: 2022-05-03 21:39:28.322711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55491a17d36d'
down_revision = '6a70d4f336c0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("keywords",
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("keyword", sa.String),
                    sa.Column("account_id", sa.Integer,
                              sa.ForeignKey("accounts.id", ondelete="CASCADE"),
                              nullable=False)
                    )


def downgrade():
    op.drop_table('keywords')
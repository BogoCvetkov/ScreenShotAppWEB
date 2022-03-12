"""create a table for pdf screenshots with One-to-One relationship

Revision ID: 77f1d7fab661
Revises: 47b9c1118ca4
Create Date: 2022-03-09 17:48:23.892565

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '77f1d7fab661'
down_revision = '47b9c1118ca4'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table( "screenshots",
	                 sa.Column( "id", sa.Integer, primary_key=True ),
	                 sa.Column( "file_dir", sa.String),
	                 sa.Column( "last_captured", sa.DateTime ),
	                 sa.Column( "account_id", sa.Integer,
	                            sa.ForeignKey( "accounts.id", ondelete="CASCADE" ),
	                            nullable=False, unique=True )
	                 )


def downgrade():
	op.drop_table('screenshots')
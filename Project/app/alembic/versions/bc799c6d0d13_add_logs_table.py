"""add logs table

Revision ID: bc799c6d0d13
Revises: a59d2adf71b1
Create Date: 2022-03-11 10:33:08.390719

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'bc799c6d0d13'
down_revision = 'a59d2adf71b1'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table( "logs",
	                 sa.Column( "id", sa.Integer, primary_key=True ),
	                 sa.Column( "started_by", sa.String, nullable=False ),
	                 sa.Column( "account_name", sa.String, nullable=False ),
	                 sa.Column( "log_msg", sa.String ),
	                 sa.Column( "log_details", sa.String ),
	                 sa.Column( "date", sa.DateTime ),
	                 sa.Column( "fail", sa.Boolean, default=False ),
	                 sa.Column( "account_id", sa.Integer,
	                            sa.ForeignKey( "accounts.id", ondelete="CASCADE" ),
	                            nullable=False ),
	                 sa.Column( "user_id",sa.Integer )
	                 )


def downgrade():
	op.drop_table( "logs" )
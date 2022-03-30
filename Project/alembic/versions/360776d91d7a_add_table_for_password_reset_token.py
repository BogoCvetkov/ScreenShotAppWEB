"""Add table for password reset token

Revision ID: 360776d91d7a
Revises: bc799c6d0d13
Create Date: 2022-03-17 16:13:33.233632

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '360776d91d7a'
down_revision = 'bc799c6d0d13'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table( "reset_pass",
	                 sa.Column( "id", sa.Integer, primary_key=True ),
	                 sa.Column( "token", sa.String, unique=True, nullable=False ),
	                 sa.Column( "expires_at", sa.DateTime, nullable=False ),
	                 sa.Column( "email", sa.String, unique=True, nullable=False )
	                 )


def downgrade():
	op.drop_table( 'reset_pass' )
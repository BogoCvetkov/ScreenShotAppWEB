"""add user Table

Revision ID: c76339936dc9
Revises: 
Create Date: 2022-03-03 15:13:32.689652

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c76339936dc9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
	op.create_table( "users",
	                 sa.Column( "id", sa.Integer, primary_key=True ),
	                 sa.Column( "email", sa.String, unique=True, nullable=False ),
	                 sa.Column( "username", sa.String, unique=True, nullable=False ),
	                 sa.Column( "password", sa.String, nullable=False ),
	                 sa.Column( "admin", sa.Boolean, default=False )
	                 )


def downgrade():
	op.drop_table("users")
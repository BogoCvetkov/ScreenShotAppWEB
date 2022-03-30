"""make account name unique
and add more columns

Revision ID: a59d2adf71b1
Revises: 77f1d7fab661
Create Date: 2022-03-10 16:25:25.198244

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a59d2adf71b1'
down_revision = '77f1d7fab661'
branch_labels = None
depends_on = None


def upgrade():
	# Make account name unique
	op.create_unique_constraint( "uq_acc_name", "accounts", ["name"] )

	# Add status for most recent operations
	op.add_column("accounts",sa.Column("last_scrape_fail",sa.Boolean, default=False))
	op.add_column("accounts",sa.Column("last_email_fail",sa.Boolean, default=False))


def downgrade():
	op.drop_constraint( 'uq_acc_name', 'accounts' )

	op.drop_column("accounts", "last_scrape_fail")
	op.drop_column("accounts", "last_email_fail")
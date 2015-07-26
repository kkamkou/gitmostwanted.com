"""status_updated_at column for repos

Revision ID: 4610d5e2ddb
Revises: 535f62f51e1
Create Date: 2015-07-23 12:06:05.176043

"""

# revision identifiers, used by Alembic.
revision = '4610d5e2ddb'
down_revision = '535f62f51e1'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('repos', sa.Column('status_updated_at', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_index(op.f('ix_repos_created_at'), table_name='repos')
    op.drop_column('repos', 'status_updated_at')

"""created_at column added

Revision ID: 16aa6c2f450
Revises: 420f9b8b9e
Create Date: 2015-07-03 16:43:55.000792

"""

# revision identifiers, used by Alembic.
revision = '16aa6c2f450'
down_revision = '420f9b8b9e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('repos', sa.Column('created_at', sa.DateTime, nullable=False))


def downgrade():
    op.drop_column('repos', 'created_at')

"""mature and status columns for the repos table

Revision ID: 535f62f51e1
Revises: 4e0851c5f08
Create Date: 2015-07-20 10:37:05.997716

"""

# revision identifiers, used by Alembic.
revision = '535f62f51e1'
down_revision = '4e0851c5f08'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy.sql import expression
import sqlalchemy as sa


def upgrade():
    op.create_index(op.f('ix_repos_created_at'), 'repos', ['created_at'], unique=False)
    op.add_column(
        'repos', sa.Column(
            'mature', sa.Boolean(), nullable=False, server_default=expression.false(), index=True
        )
    )
    op.add_column(
        'repos', sa.Column(
            'status', sa.Enum('promising', 'new', 'unknown', 'deleted', 'hopeless'),
            server_default='new', nullable=False, index=True
        )
    )


def downgrade():
    op.drop_index(op.f('ix_repos_created_at'), table_name='repos')
    op.drop_column('repos', 'status')
    op.drop_column('repos', 'mature')

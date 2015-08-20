"""worth column in repos

Revision ID: 590104e559b
Revises: 4610d5e2ddb
Create Date: 2015-08-20 09:26:57.523468

"""

revision = '590104e559b'
down_revision = '4610d5e2ddb'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    op.add_column(
        'repos',
        sa.Column('worth', mysql.TINYINT(display_width=1), server_default='3', nullable=False)
    )
    op.create_index(op.f('ix_repos_worth'), 'repos', ['worth'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_repos_worth'), table_name='repos')
    op.drop_column('repos', 'worth')

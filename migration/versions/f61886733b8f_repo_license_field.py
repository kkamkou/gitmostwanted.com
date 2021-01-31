"""repo license field

Revision ID: f61886733b8f
Revises: 286e2cdc37c9
Create Date: 2020-10-17 21:31:18.551374

"""

revision = 'f61886733b8f'
down_revision = '286e2cdc37c9'
branch_labels = None
depends_on = None

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql


def upgrade():
    op.add_column('repos', sa.Column('license', mysql.VARCHAR(length=20), nullable=True))
    op.create_index(op.f('ix_repos_license'), 'repos', ['license'])


def downgrade():
    op.drop_index(op.f('ix_repos_license'), table_name='repos')
    op.drop_column('repos', 'license')

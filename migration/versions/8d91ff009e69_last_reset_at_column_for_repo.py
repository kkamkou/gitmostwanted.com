"""last_reset_at column for repo

Revision ID: 8d91ff009e69
Revises: dbf1daf55faf
Create Date: 2017-09-01 10:54:46.855976

"""

revision = '8d91ff009e69'
down_revision = 'dbf1daf55faf'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('repos', sa.Column('last_reset_at', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_repos_last_reset_at'), 'repos', ['last_reset_at'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_repos_last_reset_at'), table_name='repos')
    op.drop_column('repos', 'last_reset_at')

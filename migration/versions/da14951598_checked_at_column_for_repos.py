"""checked_at column for repos

Revision ID: da14951598
Revises: 590104e559b
Create Date: 2015-08-24 13:20:43.100819

"""

revision = 'da14951598'
down_revision = '590104e559b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('repos', sa.Column('checked_at', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_repos_checked_at'), 'repos', ['checked_at'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_repos_checked_at'), table_name='repos')
    op.drop_column('repos', 'checked_at')

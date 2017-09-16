"""forks and subscribers count

Revision ID: 057d794890a4
Revises: 8d91ff009e69
Create Date: 2017-09-16 17:02:10.406402

"""

revision = '057d794890a4'
down_revision = '8d91ff009e69'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy.dialects.mysql import INTEGER
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'repos',
        sa.Column('forks_count', INTEGER(unsigned=True), server_default='0', nullable=False)
    )
    op.add_column(
        'repos',
        sa.Column('open_issues_count', INTEGER(unsigned=True), server_default='0', nullable=False)
    )
    op.add_column(
        'repos', sa.Column('size', INTEGER(unsigned=True), server_default='0', nullable=False)
    )
    op.add_column(
        'repos',
        sa.Column('subscribers_count', INTEGER(unsigned=True), server_default='0', nullable=False)
    )
    op.create_index(op.f('ix_repos_forks_count'), 'repos', ['forks_count'], unique=False)
    op.create_index(op.f('ix_repos_stargazers_count'), 'repos', ['stargazers_count'], unique=False)
    op.create_index(
        op.f('ix_repos_subscribers_count'), 'repos', ['subscribers_count'], unique=False
    )


def downgrade():
    op.drop_index(op.f('ix_repos_forks_count'), table_name='repos')
    op.drop_index(op.f('ix_repos_stargazers_count'), table_name='repos')
    op.drop_index(op.f('ix_repos_subscribers_count'), table_name='repos')
    op.drop_column('repos', 'forks_count')
    op.drop_column('repos', 'open_issues_count')
    op.drop_column('repos', 'size')
    op.drop_column('repos', 'subscribers_count')

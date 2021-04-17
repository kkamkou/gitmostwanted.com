"""Added repos_topics table

Revision ID: 5addea704642
Revises: f61886733b8f
Create Date: 2021-04-17 15:05:36.450231

"""

revision = '5addea704642'
down_revision = 'f61886733b8f'
branch_labels = None
depends_on = None

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.create_table(
        'repos_topics',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('repo_id', sa.BigInteger(), nullable=False),
        sa.Column('title', sa.String(length=30), nullable=False),
        sa.ForeignKeyConstraint(
            ['repo_id'], ['repos.id'], name='fk_repos_topics_repo_id', ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('repo_id', 'title', name='uc_repos_topics_repo_id_title')
    )


def downgrade():
    op.drop_table('repos_topics')

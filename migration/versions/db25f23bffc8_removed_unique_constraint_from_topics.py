"""Removed unique constraint from topics

Revision ID: db25f23bffc8
Revises: 5addea704642
Create Date: 2021-08-23 17:16:20.389142

"""
from alembic import op

revision = 'db25f23bffc8'
down_revision = '5addea704642'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(op.f('ix_repos_topics_repo_id_title'), 'repos_topics', ['repo_id', 'title'])
    op.drop_constraint('uc_repos_topics_repo_id_title', 'repos_topics', type_='foreignkey')


def downgrade():
    op.create_unique_constraint(
        'uc_repos_topics_repo_id_title', 'repos_topics', ['repo_id', 'title']
    )
    op.drop_index(op.f('ix_repos_topics_repo_id_title'), table_name='repos_topics')



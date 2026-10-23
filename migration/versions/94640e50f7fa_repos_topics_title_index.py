"""index on repos_topics title

Revision ID: 94640e50f7fa
Revises: e731a57c1d29
Create Date: 2026-10-23 13:30:00.000000

"""
from alembic import op

revision = '94640e50f7fa'
down_revision = 'e731a57c1d29'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(op.f('ix_repos_topics_title'), 'repos_topics', ['title'])


def downgrade():
    op.drop_index(op.f('ix_repos_topics_title'), table_name='repos_topics')

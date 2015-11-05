"""repos_mean table

Revision ID: 4a7b02b0a63
Revises: b75a76936b
Create Date: 2015-11-05 11:25:32.920590

"""

revision = '4a7b02b0a63'
down_revision = 'b75a76936b'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy.sql import func
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'repos_mean',
        sa.Column('repo_id', sa.BigInteger(), nullable=False),
        sa.Column('created_at', sa.Date(), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ['repo_id'], ['repos.id'],
            name='fk_repos_mean_repo_id', ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('repo_id', 'created_at')
    )


def downgrade():
    op.drop_table('repos_mean')

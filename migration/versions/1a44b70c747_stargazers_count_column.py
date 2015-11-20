"""stargazers_count column

Revision ID: 1a44b70c747
Revises: 4a7b02b0a63
Create Date: 2015-11-20 11:52:49.429594

"""

revision = '1a44b70c747'
down_revision = '4a7b02b0a63'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'repos', sa.Column('stargazers_count', sa.Integer(), server_default='0', nullable=False)
    )


def downgrade():
    op.drop_column('repos', 'stargazers_count')

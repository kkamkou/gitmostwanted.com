"""open_issues_count field

Revision ID: 36be8974c95f
Revises: 057d794890a4
Create Date: 2017-09-17 18:53:21.352072

"""

revision = '36be8974c95f'
down_revision = '057d794890a4'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy.dialects.mysql import INTEGER
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'repos',
        sa.Column('open_issues_count', INTEGER(unsigned=True), server_default='0', nullable=False)
    )


def downgrade():
    op.drop_column('repos', 'open_issues_count')

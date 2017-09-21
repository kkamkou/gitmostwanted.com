"""worh_max field

Revision ID: 286e2cdc37c9
Revises: 057d794890a4
Create Date: 2017-09-21 11:17:56.008366

"""

revision = '286e2cdc37c9'
down_revision = '057d794890a4'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy.dialects.mysql import SMALLINT
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'repos',
        sa.Column('worth_max', SMALLINT(display_width=2), server_default='0', nullable=False)
    )


def downgrade():
    op.drop_column('repos', 'worth_max')

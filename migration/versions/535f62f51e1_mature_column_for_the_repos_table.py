"""mature column for the repos table

Revision ID: 535f62f51e1
Revises: 4e0851c5f08
Create Date: 2015-07-20 10:37:05.997716

"""

# revision identifiers, used by Alembic.
revision = '535f62f51e1'
down_revision = '4e0851c5f08'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy.sql import expression
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'repos',
        sa.Column('mature', sa.Boolean(), nullable=False, server_default=expression.false())
    )


def downgrade():
    op.drop_column('repos', 'mature')

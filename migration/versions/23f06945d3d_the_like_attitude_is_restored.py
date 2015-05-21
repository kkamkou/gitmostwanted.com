"""the like attitude is restored

Revision ID: 23f06945d3d
Revises: 2561b22c4a8
Create Date: 2015-05-21 18:23:24.525600

"""

# revision identifiers, used by Alembic.
revision = '23f06945d3d'
down_revision = '2561b22c4a8'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

type_old = sa.Enum('dislike', 'neutral', name='attitude')
type_new = sa.Enum('like', 'dislike', 'neutral', name='attitude')


def upgrade():
    op.alter_column(
        'users_attitude', 'attitude',
        type_=type_new, existing_type=type_old, nullable=False
    )


def downgrade():
    op.alter_column(
        'users_attitude', 'attitude',
        type_=type_old, existing_type=type_new, nullable=False
    )

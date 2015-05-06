"""the like attitude is removed

Revision ID: 2561b22c4a8
Revises: 2bce993585c
Create Date: 2015-05-06 22:35:04.528371

"""

# revision identifiers, used by Alembic.
revision = '2561b22c4a8'
down_revision = '2bce993585c'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

type_old = sa.Enum('like', 'dislike', 'neutral', name='attitude')
type_new = sa.Enum('dislike', 'neutral', name='attitude')


def upgrade():
    ua = sa.sql.table('users_attitude', sa.Column('attitude', type_old))

    op.execute(ua.delete().where(ua.c.attitude == 'like'))
    op.alter_column(
        'users_attitude', 'attitude',
        type_=type_new, existing_type=type_old, nullable=False
    )


def downgrade():
    op.alter_column(
        'users_attitude', 'attitude',
        type_=type_old, existing_type=type_new, nullable=False
    )

"""add a new attitude - neutral

Revision ID: 56f14840f6d
Revises:
Create Date: 2015-04-27 21:10:08.934165

"""

# revision identifiers, used by Alembic.
revision = '56f14840f6d'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


type_old = sa.Enum('like', 'dislike', name='attitude')
type_new = sa.Enum('like', 'dislike', 'neutral', name='attitude')


def upgrade():
    op.alter_column(
        'users_attitude', 'attitude',
        type_=type_new, existing_type=type_old, nullable=False
    )


def downgrade():
    ua = sa.sql.table('users_attitude', sa.Column('attitude', type_new))
    op.execute(ua.delete().where(ua.c.attitude=='neutral'))

    op.alter_column(
        'users_attitude', 'attitude',
        type_=type_old, existing_type=type_new, nullable=False
    )

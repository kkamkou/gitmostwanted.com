"""repository language length

Revision ID: b75a76936b
Revises: da14951598
Create Date: 2015-10-21 09:20:38.142258

"""

revision = 'b75a76936b'
down_revision = 'da14951598'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('repos', 'language', existing_type=sa.String(25), nullable=True)


def downgrade():
    op.alter_column('repos', 'language', existing_type=sa.String(20), nullable=True)

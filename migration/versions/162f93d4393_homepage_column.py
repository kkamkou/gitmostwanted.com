"""homepage column

Revision ID: 162f93d4393
Revises: 23f06945d3d
Create Date: 2015-06-17 18:07:19.417807

"""

# revision identifiers, used by Alembic.
revision = '162f93d4393'
down_revision = '23f06945d3d'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('repos', sa.Column('homepage', sa.String(150)))


def downgrade():
    op.drop_column('repos', 'homepage')

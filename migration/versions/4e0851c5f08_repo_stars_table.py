"""repo_stars table

Revision ID: 4e0851c5f08
Revises: 16aa6c2f450
Create Date: 2015-07-13 09:56:10.710842

"""

# revision identifiers, used by Alembic.
revision = '4e0851c5f08'
down_revision = '16aa6c2f450'
branch_labels = None
depends_on = None

from sqlalchemy.dialects import mysql
from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'repos_stars',
        sa.Column('repo_id', sa.BigInteger(), nullable=False, primary_key=True),
        sa.Column('stars', mysql.SMALLINT(display_width=4, unsigned=True), nullable=False),
        sa.Column(
            'year',
            mysql.SMALLINT(display_width=4, unsigned=True),
            autoincrement=False, nullable=False, primary_key=True
        ),
        sa.Column(
            'day', mysql.SMALLINT(display_width=3, unsigned=True),
            autoincrement=False, nullable=False, primary_key=True
        ),
        sa.ForeignKeyConstraint(
            ['repo_id'], ['repos.id'], name='fk_repos_stars_repo_id', ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('repo_id', 'year', 'day')
    )


def downgrade():
    op.drop_table('repos_stars')

"""attitude constraint corrections

Revision ID: 420f9b8b9e
Revises: 162f93d4393
Create Date: 2015-06-24 16:52:02.606637

"""

# revision identifiers, used by Alembic.
revision = '420f9b8b9e'
down_revision = '162f93d4393'
branch_labels = None
depends_on = None

from alembic import op


def upgrade():
    op.drop_constraint('fk_repos_id', 'users_attitude', type_='foreignkey')
    op.drop_constraint('fk_users_id', 'users_attitude', type_='foreignkey')
    op.create_foreign_key(
        'fk_users_id', 'users_attitude', 'users', ['user_id'], ['id'], ondelete='CASCADE'
    )
    op.create_foreign_key(
        'fk_repos_id', 'users_attitude', 'repos', ['repo_id'], ['id'], ondelete='CASCADE'
    )

def downgrade():
    op.drop_constraint('fk_repos_id', 'users_attitude', type_='foreignkey')
    op.drop_constraint('fk_users_id', 'users_attitude', type_='foreignkey')
    op.create_foreign_key('fk_users_id', 'users_attitude', 'users', ['user_id'], ['id'])
    op.create_foreign_key('fk_repos_id', 'users_attitude', 'repos', ['repo_id'], ['id'])

"""cascade delete for period stars

Revision ID: dbf1daf55faf
Revises: 1a44b70c747
Create Date: 2016-10-08 10:14:03.852963

"""

revision = 'dbf1daf55faf'
down_revision = '1a44b70c747'
branch_labels = None
depends_on = None

from alembic import op


def upgrade():
    op.drop_constraint('report_all_daily_ibfk_1', 'report_all_daily', type_='foreignkey')
    op.create_foreign_key(None, 'report_all_daily', 'repos', ['id'], ['id'])
    op.drop_constraint('report_all_monthly_ibfk_1', 'report_all_monthly', type_='foreignkey')
    op.create_foreign_key(None, 'report_all_monthly', 'repos', ['id'], ['id'])
    op.drop_constraint('report_all_weekly_ibfk_1', 'report_all_weekly', type_='foreignkey')
    op.create_foreign_key(None, 'report_all_weekly', 'repos', ['id'], ['id'])


def downgrade():
    op.drop_constraint(None, 'report_all_weekly', type_='foreignkey')
    op.create_foreign_key(
        'report_all_weekly_ibfk_1', 'report_all_weekly', 'repos', ['id'], ['id'],
        ondelete='CASCADE'
    )
    op.drop_constraint(None, 'report_all_monthly', type_='foreignkey')
    op.create_foreign_key(
        'report_all_monthly_ibfk_1', 'report_all_monthly', 'repos', ['id'], ['id'],
        ondelete='CASCADE'
    )
    op.drop_constraint(None, 'report_all_daily', type_='foreignkey')
    op.create_foreign_key(
        'report_all_daily_ibfk_1', 'report_all_daily', 'repos', ['id'], ['id'],
        ondelete='CASCADE'
    )

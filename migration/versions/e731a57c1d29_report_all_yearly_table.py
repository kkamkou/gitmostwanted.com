"""report_all_yearly and report_all_quarterly tables

Revision ID: e731a57c1d29
Revises: db25f23bffc8
Create Date: 2026-10-21 12:30:00.000000

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

revision = 'e731a57c1d29'
down_revision = 'db25f23bffc8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'report_all_quarterly',
        sa.Column('cnt_watch', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('id', mysql.BIGINT(display_width=20), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['id'], ['repos.id'], name='report_all_quarterly_ibfk_1'),
        sa.PrimaryKeyConstraint('id'),
        mysql_default_charset='utf8',
        mysql_engine='InnoDB'
    )

    op.create_table(
        'report_all_yearly',
        sa.Column('cnt_watch', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('id', mysql.BIGINT(display_width=20), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['id'], ['repos.id'], name='report_all_yearly_ibfk_1'),
        sa.PrimaryKeyConstraint('id'),
        mysql_default_charset='utf8',
        mysql_engine='InnoDB'
    )


def downgrade():
    op.drop_table('report_all_yearly')
    op.drop_table('report_all_quarterly')

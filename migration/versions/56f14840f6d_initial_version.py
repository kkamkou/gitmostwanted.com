"""Initial version

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
from sqlalchemy.dialects import mysql


def upgrade():
    op.create_table(
        'repos',
        sa.Column('id', mysql.BIGINT(display_width=20), nullable=False),
        sa.Column('name', mysql.VARCHAR(length=80), nullable=True),
        sa.Column('language', mysql.VARCHAR(length=20), nullable=True),
        sa.Column('full_name', mysql.VARCHAR(length=120), nullable=True),
        sa.Column('description', mysql.VARCHAR(length=250), nullable=True),
        sa.Column('html_url', mysql.VARCHAR(length=150), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        mysql_default_charset='utf8',
        mysql_engine='InnoDB'
    )

    op.create_table(
        'report_all_monthly',
        sa.Column('cnt_watch', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('id', mysql.BIGINT(display_width=20), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['id'], ['repos.id'], name='report_all_monthly_ibfk_1'),
        sa.PrimaryKeyConstraint('id'),
        mysql_default_charset='utf8',
        mysql_engine='InnoDB'
    )

    op.create_table(
        'report_all_daily',
        sa.Column('cnt_watch', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('id', mysql.BIGINT(display_width=20), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['id'], ['repos.id'], name='report_all_daily_ibfk_1'),
        sa.PrimaryKeyConstraint('id'),
        mysql_default_charset='utf8',
        mysql_engine='InnoDB'
    )

    op.create_table(
        'report_all_weekly',
        sa.Column('cnt_watch', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('id', mysql.BIGINT(display_width=20), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['id'], ['repos.id'], name='report_all_weekly_ibfk_1'),
        sa.PrimaryKeyConstraint('id'),
        mysql_default_charset='utf8',
        mysql_engine='InnoDB'
    )

    op.create_table(
        'users',
        sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
        sa.Column('email', mysql.VARCHAR(length=120), nullable=True),
        sa.Column('username', mysql.VARCHAR(length=80), nullable=True),
        sa.Column('github_id', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint('id'),
        mysql_default_charset='utf8',
        mysql_engine='InnoDB'
    )

    op.create_table(
        'users_attitude',
        sa.Column('user_id', mysql.INTEGER(display_width=11), nullable=False),
        sa.Column('repo_id', mysql.BIGINT(display_width=20), autoincrement=False, nullable=False),
        sa.Column('attitude', mysql.ENUM('like', 'dislike'), nullable=False),
        sa.PrimaryKeyConstraint('user_id', 'repo_id'),
        mysql_default_charset='utf8',
        mysql_engine='InnoDB'
    )


def downgrade():
    op.drop_table('users_attitude')
    op.drop_table('users')
    op.drop_table('repos')
    op.drop_table('report_all_weekly')
    op.drop_table('report_all_daily')
    op.drop_table('report_all_monthly')

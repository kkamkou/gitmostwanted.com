"""Null corrections for repos and users

Revision ID: 2bce993585c
Revises: 547c89c103b
Create Date: 2015-05-04 21:21:35.215593

"""

# revision identifiers, used by Alembic.
revision = '2bce993585c'
down_revision = '547c89c103b'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy.dialects import mysql


def upgrade():
    op.alter_column(
        'report_all_daily', 'cnt_watch',
        existing_type=mysql.INTEGER(display_width=11), nullable=False
    )
    op.alter_column(
        'report_all_monthly', 'cnt_watch',
        existing_type=mysql.INTEGER(display_width=11), nullable=False
    )
    op.alter_column(
        'report_all_weekly', 'cnt_watch',
        existing_type=mysql.INTEGER(display_width=11), nullable=False
    )
    op.alter_column(
        'repos', 'full_name',
        existing_type=mysql.VARCHAR(length=120), nullable=False
    )
    op.alter_column(
        'repos', 'html_url',
        existing_type=mysql.VARCHAR(length=150), nullable=False
    )
    op.alter_column(
        'repos', 'name',
        existing_type=mysql.VARCHAR(length=80), nullable=False
    )
    op.create_unique_constraint('ix_email', 'users', ['email'])
    op.create_unique_constraint('ix_github_id', 'users', ['github_id'])
    op.create_foreign_key('fk_users_id', 'users_attitude', 'users', ['user_id'], ['id'])
    op.create_foreign_key('fk_repos_id', 'users_attitude', 'repos', ['repo_id'], ['id'])
    op.create_index(op.f('ix_users_attitude_repo_id'), 'users_attitude', ['repo_id'], unique=False)


def downgrade():
    op.drop_constraint('fk_repos_id', 'users_attitude', type_='foreignkey')
    op.drop_constraint('fk_users_id', 'users_attitude', type_='foreignkey')
    op.drop_constraint('ix_github_id', 'users', type_='unique')
    op.drop_constraint('ix_email', 'users', type_='unique')
    op.drop_index(op.f('ix_users_attitude_repo_id'), table_name='users_attitude')
    op.alter_column(
        'repos', 'name',
        existing_type=mysql.VARCHAR(length=80), nullable=True
    )
    op.alter_column(
        'repos', 'html_url',
        existing_type=mysql.VARCHAR(length=150), nullable=True
    )
    op.alter_column(
        'repos', 'full_name',
        existing_type=mysql.VARCHAR(length=120), nullable=True
    )
    op.alter_column(
        'report_all_weekly', 'cnt_watch',
        existing_type=mysql.INTEGER(display_width=11), nullable=True
    )
    op.alter_column(
        'report_all_monthly', 'cnt_watch',
        existing_type=mysql.INTEGER(display_width=11), nullable=True
    )
    op.alter_column(
        'report_all_daily', 'cnt_watch',
        existing_type=mysql.INTEGER(display_width=11), nullable=True
    )

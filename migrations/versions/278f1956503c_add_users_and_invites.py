"""add users and invites

Revision ID: 278f1956503c
Revises: None
Create Date: 2016-05-27 16:55:12.309554

"""

# revision identifiers, used by Alembic.
revision = '278f1956503c'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invite', sa.Unicode(length=36), nullable=True),
    sa.Column('email', sa.Unicode(length=30), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('used', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('invite')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.Unicode(length=30), nullable=True),
    sa.Column('password', sa.Unicode(length=60), nullable=True),
    sa.Column('invite', sa.Unicode(length=36), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('admin', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('invite'),
    sa.UniqueConstraint('login'),
    sa.UniqueConstraint('password')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('invites')
    ### end Alembic commands ###
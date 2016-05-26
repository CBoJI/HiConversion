"""add user

Revision ID: c32dce588c6a
Revises: None
Create Date: 2016-05-26 11:32:51.517846

"""

# revision identifiers, used by Alembic.
revision = 'c32dce588c6a'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.Unicode(length=30), nullable=True),
    sa.Column('password', sa.Unicode(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login'),
    sa.UniqueConstraint('password')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    ### end Alembic commands ###
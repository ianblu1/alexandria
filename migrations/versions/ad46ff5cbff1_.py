"""empty message

Revision ID: ad46ff5cbff1
Revises: None
Create Date: 2016-11-10 22:05:30.899717

"""

# revision identifiers, used by Alembic.
revision = 'ad46ff5cbff1'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('first_name', sa.Text(), nullable=True),
    sa.Column('last_name', sa.Text(), nullable=True),
    sa.Column('user_name', sa.Text(), nullable=False),
    sa.Column('password', postgresql.BYTEA(), nullable=False),
    sa.Column('authenticated', sa.Boolean(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_name'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    ### end Alembic commands ###

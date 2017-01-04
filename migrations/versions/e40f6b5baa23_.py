"""empty message

Revision ID: e40f6b5baa23
Revises: 2d4355c91ba2
Create Date: 2017-01-01 22:56:46.494899

"""

# revision identifiers, used by Alembic.
revision = 'e40f6b5baa23'
down_revision = '2d4355c91ba2'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('tag', sa.Text(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('documentlinks',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('url', sa.Text(), nullable=False),
    sa.Column('slug', sa.Text(), nullable=True),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('document_vector', postgresql.TSVECTOR(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('creating_user', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['creating_user'], ['users.user_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('documentlink_tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('documentlink_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['documentlink_id'], ['documentlinks.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('documentlink_id', 'tag_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('documentlink_tags')
    op.drop_table('documentlinks')
    op.drop_table('tags')
    ### end Alembic commands ###

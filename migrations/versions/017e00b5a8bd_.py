"""empty message

Revision ID: 017e00b5a8bd
Revises: e40f6b5baa23
Create Date: 2017-01-01 23:59:20.816541

"""

# revision identifiers, used by Alembic.
revision = '017e00b5a8bd'
down_revision = 'e40f6b5baa23'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('documentlinks', sa.Column('description', sa.Text(), nullable=False))
    op.create_index('ix_documentlinks', 'documentlinks', ['document_vector'], unique=False, postgresql_using='gin')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_documentlinks', table_name='documentlinks')
    op.drop_column('documentlinks', 'description')
    ### end Alembic commands ###

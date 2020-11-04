"""empty message

Revision ID: 41955aeb0952
Revises: b20062b102a2
Create Date: 2020-11-04 09:08:49.032916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41955aeb0952'
down_revision = 'b20062b102a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('img', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'img')
    # ### end Alembic commands ###

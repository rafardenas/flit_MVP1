"""empty message

Revision ID: fc4b2f4a95a6
Revises: 
Create Date: 2021-07-21 13:56:41.703953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc4b2f4a95a6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cargasembarcadores', 'carga')
    # ### end Alembic commands ###

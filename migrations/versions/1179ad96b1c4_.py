"""empty message

Revision ID: 1179ad96b1c4
Revises: 484427a88da3
Create Date: 2021-08-01 08:35:27.420221

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1179ad96b1c4'
down_revision = '484427a88da3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cargasembarcadores', sa.Column('forma_de_pago', sa.String(length=200), nullable=True))
    op.drop_column('cargasembarcadores', 'precio_por_unidad_ofertado')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cargasembarcadores', sa.Column('precio_por_unidad_ofertado', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_column('cargasembarcadores', 'forma_de_pago')
    # ### end Alembic commands ###

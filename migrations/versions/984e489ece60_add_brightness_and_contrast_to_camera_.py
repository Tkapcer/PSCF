"""Add brightness and contrast to camera settings

Revision ID: 984e489ece60
Revises: bd718a99e76e
Create Date: 2025-05-31 15:57:15.906869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '984e489ece60'
down_revision = 'bd718a99e76e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('camera_settings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('brightness', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('contrast', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('camera_settings', schema=None) as batch_op:
        batch_op.drop_column('contrast')
        batch_op.drop_column('brightness')

    # ### end Alembic commands ###

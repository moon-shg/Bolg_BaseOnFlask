"""add User.confirmed

Revision ID: 09aeee631b6c
Revises: 5a5ff2ba50e4
Create Date: 2019-11-21 11:58:19.569484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09aeee631b6c'
down_revision = '5a5ff2ba50e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###
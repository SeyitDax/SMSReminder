"""Initial tables

Revision ID: 50d83bc7a246
Revises: 
Create Date: 2025-07-01 13:16:47.064488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50d83bc7a246'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reminder',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('to', sa.String(length=20), nullable=False),
    sa.Column('message', sa.String(length=160), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reminder')
    # ### end Alembic commands ###

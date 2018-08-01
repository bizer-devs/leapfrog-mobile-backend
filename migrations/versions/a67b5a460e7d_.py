"""empty message

Revision ID: a67b5a460e7d
Revises: 
Create Date: 2018-07-31 23:40:01.020674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a67b5a460e7d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pending_transfers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('old_holder_id', sa.Integer(), nullable=False),
    sa.Column('leapfrog_id', sa.Integer(), nullable=False),
    sa.Column('transfer_code', sa.String(length=30), nullable=True),
    sa.Column('time_created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['leapfrog_id'], ['leapfrogs.id'], ),
    sa.ForeignKeyConstraint(['old_holder_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pending_transfers')
    # ### end Alembic commands ###
"""add user name+surname

Revision ID: fde3cb2aa55a
Revises: 183699afb765
Create Date: 2022-02-10 13:05:49.762656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fde3cb2aa55a'
down_revision = '183699afb765'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('first_name', sa.Text(), nullable=False))
    op.add_column('users', sa.Column('last_name', sa.Text(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    # ### end Alembic commands ###

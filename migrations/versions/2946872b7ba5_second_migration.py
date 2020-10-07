"""Second Migration

Revision ID: 2946872b7ba5
Revises: 6a443e237c05
Create Date: 2020-10-07 10:28:03.483641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2946872b7ba5'
down_revision = '6a443e237c05'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('profile_pic_path', sa.String(), nullable=True))
    op.drop_column('users', 'prof_pic_path')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('prof_pic_path', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('users', 'profile_pic_path')
    # ### end Alembic commands ###

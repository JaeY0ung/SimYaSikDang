"""empty message

Revision ID: 2c1d3b8feb22
Revises: 1dd19e3696fc
Create Date: 2023-09-26 16:02:43.937980

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c1d3b8feb22'
down_revision = '1dd19e3696fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('place', schema=None) as batch_op:
        batch_op.alter_column('review_total',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=64),
               existing_nullable=True)

    with op.batch_alter_table('userlike', schema=None) as batch_op:
        batch_op.alter_column('likedate',
               existing_type=sa.DATETIME(),
               type_=sa.String(length=64),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('userlike', schema=None) as batch_op:
        batch_op.alter_column('likedate',
               existing_type=sa.String(length=64),
               type_=sa.DATETIME(),
               existing_nullable=False)

    with op.batch_alter_table('place', schema=None) as batch_op:
        batch_op.alter_column('review_total',
               existing_type=sa.String(length=64),
               type_=sa.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###

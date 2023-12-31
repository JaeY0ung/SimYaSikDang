"""empty message

Revision ID: a15e1da3f421
Revises: 7c35e066ace8
Create Date: 2023-09-29 14:08:34.167248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a15e1da3f421'
down_revision = '7c35e066ace8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('singoplace', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contact', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('email', sa.String(length=64), nullable=True))
        batch_op.alter_column('userid',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('placeid',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contact', sa.String(length=64), nullable=True))
        batch_op.drop_column('phone')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone', sa.VARCHAR(length=64), nullable=True))
        batch_op.drop_column('contact')

    with op.batch_alter_table('singoplace', schema=None) as batch_op:
        batch_op.alter_column('placeid',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('userid',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_column('email')
        batch_op.drop_column('contact')

    # ### end Alembic commands ###

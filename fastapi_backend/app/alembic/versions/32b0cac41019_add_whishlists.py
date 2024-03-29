"""Add whishlists

Revision ID: 32b0cac41019
Revises: 191c130fdb11
Create Date: 2021-10-23 16:07:56.306078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32b0cac41019'
down_revision = '191c130fdb11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('whishlists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_whishlists_id'), 'whishlists', ['id'], unique=False)
    op.create_table('whishlisted_books',
    sa.Column('whishlist_id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['whishlist_id'], ['whishlists.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('whishlisted_books')
    op.drop_index(op.f('ix_whishlists_id'), table_name='whishlists')
    op.drop_table('whishlists')
    # ### end Alembic commands ###

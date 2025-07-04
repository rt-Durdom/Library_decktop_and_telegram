"""Add genre_users

Revision ID: 5319f611dc8b
Revises: 7074e20b9bc2
Create Date: 2025-06-13 14:04:33.265811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5319f611dc8b'
down_revision = '7074e20b9bc2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('basket',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'book_id', 'id')
    )
    op.add_column('user', sa.Column('like_ganre', sa.Enum('ACTION', 'COMEDY', 'DRAMA', 'FANTASY', 'HORROR', 'ROMANCE', 'THRILLER', name='ganrebook'), nullable=False))
    op.add_column('user', sa.Column('telegram_id', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('total_books', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'total_books')
    op.drop_column('user', 'telegram_id')
    op.drop_column('user', 'like_ganre')
    op.drop_table('basket')
    # ### end Alembic commands ###

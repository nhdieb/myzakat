"""Add Story model

Revision ID: 12f917cf4dcc
Revises: ca00c104b62d
Create Date: 2025-05-06 03:03:31.326092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12f917cf4dcc'
down_revision = 'ca00c104b62d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('story',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('image_filename', sa.String(length=100), nullable=False),
    sa.Column('summary', sa.Text(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('story')
    # ### end Alembic commands ###

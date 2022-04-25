"""Migration

Revision ID: 72a1a49e513a
Revises: 
Create Date: 2022-04-25 14:50:56.249380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72a1a49e513a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('sender_id', sa.Integer(), nullable=True))
    op.add_column('task', sa.Column('recipient_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'task', 'user', ['recipient_id'], ['id'])
    op.create_foreign_key(None, 'task', 'user', ['sender_id'], ['id'])
    op.drop_column('task', 'recipient')
    op.drop_column('task', 'sender')
    op.add_column('user', sa.Column('name', sa.String(length=64), nullable=True))
    op.drop_column('user', 'forename')
    op.drop_column('user', 'surname')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('surname', sa.VARCHAR(length=64), nullable=True))
    op.add_column('user', sa.Column('forename', sa.VARCHAR(length=64), nullable=True))
    op.drop_column('user', 'name')
    op.add_column('task', sa.Column('sender', sa.VARCHAR(length=64), nullable=True))
    op.add_column('task', sa.Column('recipient', sa.VARCHAR(length=64), nullable=True))
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'recipient_id')
    op.drop_column('task', 'sender_id')
    # ### end Alembic commands ###

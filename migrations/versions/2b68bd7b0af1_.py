"""empty message

Revision ID: 2b68bd7b0af1
Revises: 905ccf93e73d
Create Date: 2019-01-28 00:10:31.627104

"""

# revision identifiers, used by Alembic.
revision = '2b68bd7b0af1'
down_revision = '905ccf93e73d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_constraint(None, 'game_server', type_='foreignkey')
    op.drop_column('game_server', 'user_id')
    op.drop_constraint(None, 'match', type_='foreignkey')
    op.drop_column('match', 'user_id')
    op.drop_constraint(None, 'team', type_='foreignkey')
    op.drop_column('team', 'user_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('team', sa.Column('user_id', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'team', 'user', ['user_id'], ['id'])
    op.add_column('match', sa.Column('user_id', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'match', 'user', ['user_id'], ['id'])
    op.add_column('game_server', sa.Column('user_id', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'game_server', 'user', ['user_id'], ['id'])
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('steam_id', sa.VARCHAR(length=40), nullable=True),
    sa.Column('name', sa.VARCHAR(length=40), nullable=True),
    sa.Column('admin', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('steam_id')
    )
    ### end Alembic commands ###

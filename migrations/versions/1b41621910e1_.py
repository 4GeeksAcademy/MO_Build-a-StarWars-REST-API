"""empty message

Revision ID: 1b41621910e1
Revises: 940107001b0c
Create Date: 2024-07-07 17:19:32.704197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b41621910e1'
down_revision = '940107001b0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('starships',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('model', sa.String(length=50), nullable=True),
    sa.Column('manufacturer', sa.String(length=50), nullable=True),
    sa.Column('length', sa.Integer(), nullable=True),
    sa.Column('crew', sa.Integer(), nullable=True),
    sa.Column('passengers', sa.Integer(), nullable=True),
    sa.Column('consumables', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite_starships',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('starship_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['starship_id'], ['starships.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('favorite_people', schema=None) as batch_op:
        batch_op.alter_column('people_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('favorite_planets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planet_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('favorite_planets_planets_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'planets', ['planet_id'], ['id'])
        batch_op.drop_column('planets_id')

    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_name', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('height', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('mass', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('birht_year', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('gender', sa.String(length=50), nullable=False))
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=50),
               existing_nullable=False)

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('population', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('rotation_period', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('orbita_period', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('diameter', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('climate', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('terrain', sa.String(length=50), nullable=False))
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=50),
               existing_nullable=False)
        batch_op.create_unique_constraint(None, ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('name',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=30),
               existing_nullable=False)
        batch_op.drop_column('terrain')
        batch_op.drop_column('climate')
        batch_op.drop_column('diameter')
        batch_op.drop_column('orbita_period')
        batch_op.drop_column('rotation_period')
        batch_op.drop_column('population')

    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=30),
               existing_nullable=False)
        batch_op.drop_column('gender')
        batch_op.drop_column('birht_year')
        batch_op.drop_column('mass')
        batch_op.drop_column('height')
        batch_op.drop_column('last_name')

    with op.batch_alter_table('favorite_planets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planets_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('favorite_planets_planets_id_fkey', 'planets', ['planets_id'], ['id'])
        batch_op.drop_column('planet_id')

    with op.batch_alter_table('favorite_people', schema=None) as batch_op:
        batch_op.alter_column('people_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    op.drop_table('favorite_starships')
    op.drop_table('starships')
    # ### end Alembic commands ###

"""empty message

Revision ID: 955a9c2284a9
Revises: 
Create Date: 2018-03-13 18:29:11.512075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '955a9c2284a9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('containers',
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('sessions',
    sa.Column('sessionId', sa.String(length=60), nullable=False),
    sa.Column('sessionComment', sa.String(length=200), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('isTeacher', sa.Boolean(), nullable=True),
    sa.Column('image', sa.String(length=20), nullable=True),
    sa.Column('experiment', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('sessionId')
    )
    op.create_table('students',
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('realname', sa.String(length=30), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('isTeacher', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('teachers',
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('realname', sa.String(length=30), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('isTeacher', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('courses',
    sa.Column('courseNums', sa.String(length=60), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('teacherName', sa.String(length=60), nullable=True),
    sa.ForeignKeyConstraint(['teacherName'], ['teachers.name'], ),
    sa.PrimaryKeyConstraint('courseNums')
    )
    op.create_table('images',
    sa.Column('imageId', sa.String(length=40), nullable=False),
    sa.Column('hostname', sa.String(length=40), nullable=True),
    sa.Column('sessionId', sa.String(length=60), nullable=True),
    sa.ForeignKeyConstraint(['sessionId'], ['sessions.sessionId'], ),
    sa.PrimaryKeyConstraint('imageId')
    )
    op.create_table('experiments',
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('content', sa.LargeBinary(), nullable=True),
    sa.Column('courseNums', sa.String(length=60), nullable=True),
    sa.Column('containerName', sa.String(length=60), nullable=True),
    sa.Column('teacherName', sa.String(length=60), nullable=False),
    sa.ForeignKeyConstraint(['courseNums'], ['courses.courseNums'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('registrations',
    sa.Column('studentName', sa.String(length=60), nullable=True),
    sa.Column('courseNums', sa.String(length=60), nullable=True),
    sa.ForeignKeyConstraint(['courseNums'], ['courses.courseNums'], ),
    sa.ForeignKeyConstraint(['studentName'], ['students.name'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('registrations')
    op.drop_table('experiments')
    op.drop_table('images')
    op.drop_table('courses')
    op.drop_table('teachers')
    op.drop_table('students')
    op.drop_table('sessions')
    op.drop_table('containers')
    # ### end Alembic commands ###

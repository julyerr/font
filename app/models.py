# coding=utf-8
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.schema import Sequence
import uuid

from app import db, login_manager


class Teacher(UserMixin, db.Model):
    __tablename__ = 'teachers'

    # 列名
    name = db.Column(db.String(60), primary_key=True)
    realname = db.Column(db.String(30), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    isTeacher = db.Column(db.Boolean(), nullable=False, default=True)
    # 方便获取courses对象
    courses = db.relationship('Course', backref='teachers',
                              lazy='dynamic')

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = password

    def verifypassword(self, password):
        """
        Check if hashed password matches actual password
        """
        return self.password_hash == password

    def __repr__(self):
        return '<Teacher: {}>'.format(self.username)

        # 用于标志每个用户

    def get_id(self):
        return unicode(self.name)


#     约束表
registrations = db.Table('registrations',
                         db.Column('studentName', db.String(60), db.ForeignKey('students.name')),
                         db.Column('courseNums', db.String(60), db.ForeignKey('courses.courseNums'))
                         )


class Student(UserMixin, db.Model):
    __tablename__ = 'students'

    name = db.Column(db.String(60), nullable=False, primary_key=True)
    realname = db.Column(db.String(30), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    isTeacher = db.Column(db.Boolean(), default=False)
    # 方便获取到courses对象
    courses = db.relationship('Course', secondary=registrations,
                              backref=db.backref('students', lazy='dynamic'),
                              lazy='dynamic')

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verifypassword(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Student: {}>'.format(self.name)

    def get_id(self):
        return unicode(self.name)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    teacher = Teacher.query.filter_by(name=str(user_id)).first()
    if teacher is None:
        return Student.query.filter_by(name=str(user_id)).first()
    return teacher


class Course(db.Model):
    __tablename__ = 'courses'
    courseNums = db.Column(db.String(60), primary_key=True)
    name = db.Column(db.String(60), primary_key=False, nullable=False)
    description = db.Column(db.String(200))
    # 外键约束
    teacherName = db.Column(db.String(60), db.ForeignKey('teachers.name'))
    # 方便获取experiment对象
    experiments = db.relationship('Experiment', backref='courses',
                                  lazy='dynamic')

    def __repr__(self):
        return self.name.encode('utf-8')


def gen_id():
    return uuid.uuid4().hex


class Experiment(db.Model):
    __tablename__ = 'experiments'
    id = db.Column(db.String(60), default=gen_id, primary_key=True)
    name = db.Column(db.String(60))
    description = db.Column(db.String(200))
    # 实验内容也存储到数据库中
    content = db.Column(db.LargeBinary)
    # 外键约束
    courseNums = db.Column(db.String(60), db.ForeignKey('courses.courseNums'))
    containerName = db.Column(db.String(60))
    teacherName = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return '{}'.format(self.name)


class Container(db.Model):
    __tablename__ = 'containers'
    name = db.Column(db.String(60), primary_key=True)


class Session(db.Model):
    __tablename__ = 'sessions'
    sessionId = db.Column(db.String(60), nullable=False, primary_key=True)
    sessionComment = db.Column(db.String(200))
    name = db.Column(db.String(20), nullable=False)
    isTeacher = db.Column(db.Boolean)
    image = db.Column(db.String(20))
    experiment = db.Column(db.String(40))


class Images(db.Model):
    __tablename__ = 'images'
    imageId = db.Column(db.String(40), primary_key=True)
    hostname = db.Column(db.String(40))
    sessionId = db.Column(db.String(60), db.ForeignKey('sessions.sessionId'))

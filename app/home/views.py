from flask import abort, flash, redirect, render_template, url_for ,request
from flask_login import login_required, current_user
from ..models import Student,Teacher,Experiment,Course
from . import home
from .. import db
# from ..models import Employee


@home.route('/')
def homepage():

    return render_template('home/index.html', title='Welcome to Hangdian')


@home.route('/dashboard')
@login_required
def dashboard():
    return render_template('home/dashboard.html', title='Dashboard')


@home.route('/teacher/dashboard')
@login_required
def teacher_dashboard():
	if current_user.id > 10000:
		abort(403)
    return render_template('home/teacher_dashboard.html', title='Teacher Dashboard')


@home.route('/list_courses', methods=['GET', 'POST'])
@login_required
def list_courses():
	courses = Student.query().filter_by(name=current_user.name).courses()
	experimentSet = []
	for i in courses:
		experiments=Experiment.query().filter_by(courseName=i.name).all()
		experimentSet.append(experiments)
    return render_template('home/list_courses.html', title='Student Classes',courses=courses,experimentSet=experimentSet)

@home.route('/selectCourse', methods=['GET', 'POST'])
@login_required
def selectCourse():
	nums=request.form['nums']
	course = Course.query.filter_by(courseNums).first()
	if course is not None or nums == course.courseNums:
		current_user.courses.append(course)
	else:
		flash("no course set the id ")
	return redirect(url_for('home.list_courses'))

@home.route('/experiment', methods=['GET', 'POST'])
@login_required
def experiment(name):
    return render_template('pwd/index.html', title='terminal')
	
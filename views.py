from flask import (
    flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.utils import redirect
from app import app
from model import Course, Lesson, db


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/courses')
def courses():
    course_list = Course.query.all()
    return render_template('courses.html', course_list=course_list)


@app.route('/course/<int:id>')
def lessons(id):
    course = Course.query.filter_by(id=id).first()
    lesson_list = Lesson.query.filter_by(course_id=id).all()
    return render_template('course.html', lesson_list=lesson_list, course=course)


@app.route('/course/<int:courseid>/lesson/<int:id>')
def lesson(courseid, id):
    course = Course.query.filter_by(id=courseid).first()
    lesson = Lesson.query.filter_by(id=id).first()
    return render_template('lesson.html', lesson=lesson, course=course)


@app.route('/newcourse', methods=('GET', 'POST'))
def newcourse():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        instructor_id = g.user.id
        error = None

        if not title:
            error = 'Campo título é obrigatório.'
        elif not description:
            error = 'Campo description é obrigatório.'

        if error is None:
            try:
                course = Course(title=title, description=description, instructor_id=instructor_id)
                db.session.add(course)
                db.session.commit()
            except db.IntegrityError:
                error = f"Curso {title} já foi registrado."
            else:
                return redirect(url_for("courses"))

        flash(error)

    return render_template('createcourse.html')


@app.route('/<int:id>/newlesson', methods=('GET', 'POST'))
def newlesson(id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        content = request.form['content']
        exercise = request.form['exercise']
        input_exercise = request.form['input_exercise']
        output_exercise = request.form['output_exercise']
        course_id = id
        instructor_id = g.user.id
        error = None

        if not title:
            error = 'Campo título é obrigatório.'
        elif not description:
            error = 'Campo descrição é obrigatório.'
        elif not content:
            error = 'Campo conteúdo é obrigatório.'
        elif not exercise:
            error = 'Campo exercício é obrigatório.'

        if error is None:
            try:
                lesson = Lesson(title=title, description=description, content=content, exercise=exercise,
                                input_exercise=input_exercise, output_exercise=output_exercise,
                                instructor_id=instructor_id, course_id=course_id)
                db.session.add(lesson)
                db.session.commit()
            except db.IntegrityError:
                error = f"Aula {title} já foi registrada."
            else:
                return redirect(url_for("courses"))

        flash(error)

    return render_template('createlesson.html')
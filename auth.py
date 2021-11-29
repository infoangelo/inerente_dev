import functools
from flask import (
    flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from model import User, Course, db


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        error = None

        if not name:
            error = 'Campo nome é obrigatório.'
        elif not email:
            error = 'Campo email é obrigatório.'
        elif not password:
            error = 'Campo senha é obrigatório.'
        elif not role:
            error = 'Campo grupo é obrigatório.'

        if error is None:
            try:
                user = User(name=name, email=email, password=generate_password_hash(password), role=role)
                db.session.add(user)
                db.session.commit()
            except db.IntegrityError:
                error = f"Email {email} já foi registrado."
            else:
                return redirect(url_for("login"))

        flash(error)

    return render_template('auth/register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        user = User.query.filter_by(email=email).first()

        if user is None:
            error = 'Usuário ou senha incorretos.'
        elif not check_password_hash(user.password, password):
            error = 'Usuário ou senha incorretos.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


@app.before_first_request
def setup():
    db.create_all()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view
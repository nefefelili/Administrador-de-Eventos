from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm
from app.models import db, User, Role
from flask_login import login_user, logout_user

#blueprint de autenticaciion
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Logs in an existing user if credentials are valid.
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        #verifica si el usuario y el password esta correcto
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))

        flash('Invalid credentials.')

    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registers a new user as either a Participante or Organizador.
    """
    form = RegisterForm()

    if form.validate_on_submit():
        role = Role.query.filter_by(name=form.role.data).first()

        if not role:
            flash('Selected role not found. Please try again.')
            return render_template('register.html', form=form)

        user = User(
            username=form.username.data,
            email=form.email.data,
            role=role
        )
        user.set_password(form.password.data)

        #salvar a bases de dato
        db.session.add(user)
        db.session.commit()

        flash('User registered successfully.')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth.route('/logout')
def logout():
    """
    Logs out the current user and redirects to login.
    """
    logout_user()
    return redirect(url_for('auth.login'))
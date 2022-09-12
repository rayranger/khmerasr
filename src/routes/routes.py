from crypt import methods
from src import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from src.forms.register_form import RegisterForm
from src.forms.sing_in_form import SigninForm
from src.controllers import user_controller, role_controller
from src.models.user import User
from src.models.role import Role
from src import db
from flask_login import login_user, logout_user, login_required

userController = user_controller.UserController()

@app.route('/sign-in', methods=['GET', 'POST'])
def signin_page():
    sign_in_form = SigninForm()
    if sign_in_form.validate_on_submit:
        attempted_user = userController.is_existed(sign_in_form.username.data)
        if attempted_user and attempted_user.check_password_correction(attempted_password = sign_in_form.password.data):
            login_user(attempted_user)
            flash(f'Seccess! You are logged in as: {attempted_user.username}')
            return redirect(url_for('home_page'))
        else:
            flash(f'Username or password are not match')
    return render_template('sign-in.html', sign_in_form = sign_in_form)

@app.route('/sign-out')
def signout_page():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('signin_page'))

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    register_form = RegisterForm()
    roleController = role_controller.RoleController()
    roles = roleController.get_all_roles()
    if register_form.validate_on_submit():
        new_user = User(username=register_form.username.data, email=register_form.email.data, password=register_form.password.data)
        db.session.add(new_user)
        db.session.commit()
        new_user.roles.append(roles[1])
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home_page'))
    if register_form.errors != {}:
        for err_msg in register_form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}')
    return render_template('register.html', register_form=register_form)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/record')
@login_required
def record_page():
    return render_template('record.html')
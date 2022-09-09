from crypt import methods
from src import app
from flask import render_template
from src.forms.sing_in_form import SigninForm
from src.controllers import user_controller

userController = user_controller.UserController()

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/sign-in', methods=['GET', 'POST'])
def signin_page():
    sign_in_form = SigninForm()
    return render_template('sign-in.html', sign_in_form = sign_in_form)

# @app.route('/create-user')
# def create_page():
#     user = userController.create_user(username='punsolita', email='punsolita@gmail.com', password='1234')
#     if user:
#         return 'Done'
#     else:
#         return 'Undone'
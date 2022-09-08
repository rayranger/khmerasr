from crypt import methods
from src import app
from flask import render_template
from src.forms.sing_in_form import SigninForm

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/sign-in', methods=['GET', 'POST'])
def signin_page():
    sign_in_form = SigninForm()
    return render_template('sign-in.html', sign_in_form = sign_in_form)
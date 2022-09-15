from genericpath import exists
from pickle import TRUE
from src.controllers import user_controller, role_controller, speaker_controller, random_password
from src import GOGOLE_CLIENT_ID
from flask_login import login_user, logout_user
from flask import flash, session, request, get_flashed_messages, redirect, url_for
from  google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import os
import pathlib
import requests
import cachecontrol
import google

userController = user_controller.UserController()
roleController = role_controller.RoleController()
speakerController = speaker_controller.SpeakerController()

client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secrets_file.json")
flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
        redirect_uri="http://127.0.0.1:5000/callback",
    )

class AuthController():

    def sign_in(self, sign_in_form):
        if sign_in_form.validate_on_submit:
            attempted_user = userController.is_existed(sign_in_form.username.data)
            if attempted_user and attempted_user.check_password_correction(attempted_password = sign_in_form.password.data):
                login_user(attempted_user)
                flash(f'Seccess! You are logged in as: {attempted_user.username}')
                return True
            else:
                flash(f'Username or password are not match')
                return False
    
    def register(self, register_form):
        roles = roleController.get_all_roles()
        if register_form.validate_on_submit():
            new_user = userController.create_user(
            username=register_form.username.data, 
            email=register_form.email.data, 
            password=register_form.password.data,
            role=roles[1]
            )
            speakerController.create_speaker(
                first_name=register_form.first_name.data,
                last_name=register_form.last_name.data,
                gender=register_form.gender.data,
                age=register_form.age.data,
                occupation=register_form.occupation.data,
                phone_number=register_form.phone_number.data,
                user_id=userController.is_existed(data=register_form.username.data).id
            )
            login_user(new_user)
            return True
        if register_form.errors != {}:
            for err_msg in register_form.errors.values():
                flash(f'There was an error with creating a user: {err_msg}')
            return False
    
    def sign_out(self):
        logout_user()
        flash('You have been logged out!')
        return True

    def google_sign_in(self):
        authorization_url, state = flow.authorization_url()
        session["state"] = state
        return authorization_url
    
    def google_callback(self):
        flow.fetch_token(authorization_response=request.url)
        if not session["state"] == request.args["state"]:
            return False
        else:
            credentials = flow.credentials
            request_session = requests.session()
            cached_session = cachecontrol.CacheControl(request_session)
            token_request = google.auth.transport.requests.Request(session=cached_session)
            id_info = id_token.verify_oauth2_token(
                id_token=credentials._id_token,
                request=token_request,
                audience=GOGOLE_CLIENT_ID
            )
            roles = roleController.get_all_roles()
            username = id_info.get("given_name").lower()
            password = random_password.RANDOM_NUMBER
            email = id_info.get("email")
            new_user = userController.create_user(
                username=username,
                password=password,
                email=email,
                role=roles[1]
            )
            if new_user:
                login_user(new_user)
                return redirect(url_for('speaker_register_page'))
            else:
                exist_user = userController.is_existed(data=username)
                login_user(exist_user)
            return True
    
from src.models import audio, user, speaker, record_config, task, default_values
from src import db
from flask_login import UserMixin
from datetime import datetime

class UserController(UserMixin):

    # Check by username
    def is_existed(self, data):
        req = user.User.query.filter_by(username=data).first()
        if req:
            return req
        return None
    
    # Check by id
    def findUserById(self, data):
        req = user.User.query.filter_by(id=data).first()
        if req:
            return req
        return None

    def create_user(self, username, email, password, role):
        if self.is_existed(username):
            return None
        else:
            new_user = user.User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            new_user.roles.append(role)
            db.session.commit()
            return new_user
    
    def update_user(self, new_user_obj, id):
        user_obj = self.findUserById(data=id)
        if user_obj:
            user_obj.username = new_user_obj.username
            user_obj.email = new_user_obj.email
            user_obj.is_active = new_user_obj.is_active
            user_obj.updated_at = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
            db.session.commit()
            return new_user_obj
        else:
            return None
    
    def delete_user(self, id):
        user_obj = self.findUserById(data=id)
        print(user_obj.roles)
        if user_obj:
            db.session.delete(user_obj)
            db.session.commit()
            return user_obj
        else:
            return None
    
    def get_all_user(self):
        users = user.User.query.all()
        userList = []
        for user_obj in users:
            userList.append(user_obj)
        return userList


from multiprocessing.util import is_exiting
from src.models import user, speaker, record_config, task, record
from src import db

class UserController():

    def is_existed(self, data):
        req_1 = user.User.query.filter_by(username=data).first()
        req_2 = user.User.query.filter_by(id=data).first()
        if req_1 or req_2:
            return req_1
        else:
            return None

    def create_user(self, username, email, password):
        new_user = user.User(username=username, email=email, password=password)

        if self.is_existed(username):
            return None
        else:
            db.session.add(new_user)
            db.session.commit()
            new_user.roles.append()
            db.session.commit()
            return new_user
    
    def update_user(self, id, new_user_obj):
        user_obj = self.is_existed(id)
        if user_obj:
            user_obj.username = new_user_obj.username
            user_obj.password = new_user_obj.password
            user_obj.email = new_user_obj.email
            db.session.commit()
            return new_user_obj
        else:
            return None


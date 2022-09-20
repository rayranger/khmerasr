from src.models import user, speaker, record_config, task, record, default_values
from src import db
from flask_login import UserMixin

class UserController(UserMixin):

    def is_existed(self, data):
        req_1 = user.User.query.filter_by(username=data).first()
        req_2 = user.User.query.filter_by(id=data).first()
        if req_1:
            return req_1
        elif req_2:
            return req_2
        else:
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
    
    def update_user(self, new_user_obj):
        user_obj = self.is_existed(data=new_user_obj.id)
        if user_obj:
            user_obj.username = new_user_obj.username
            user_obj.password = new_user_obj.password
            user_obj.email = new_user_obj.email
            user_obj.updated_at = default_values.TODAY_DATE_TIME
            db.session.commit()
            return new_user_obj
        else:
            return None
    
    def delete_user(self, id):
        user_obj = self.is_existed(data=id)
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


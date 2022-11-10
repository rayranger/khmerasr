from src import db
from src.models import role

class RoleController():

    # Check by id
    def is_existed(self, id):
        req = role.Role.query.filter_by(id=id).first()
        if req:
            return req
        else:
            return None
    
    def get_all_roles(self):
        roles = role.Role.query.all()
        roleList = []
        for role_item in roles:
            roleList.append(role_item)
        return roleList


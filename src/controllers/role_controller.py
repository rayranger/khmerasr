from src import db
from src.models import role

class RoleController():
    
    def get_all_roles(self):
        roles = role.Role.query.all()
        roleList = []
        for role_item in roles:
            roleList.append(role_item)
        return roleList

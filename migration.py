from src import db
# from src.models import models
from src.models import record, record_category, role, speaker, user, record_config, task
db.create_all()
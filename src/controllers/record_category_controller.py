from src import db
from src.models import record_category, record, default_values

class RecordCategoryController():
    
    def is_existed(self, data):
        req_1 = record_category.RecordCategory.query.filter_by(id=data).first()
        req_2 = record_category.RecordCategory.query.filter_by(name=data).first()
        if req_1 or req_2:
            return req_1
        else:
            return None
    
    def create_record_category(self, name, description):
        if self.is_existed(name):
            return None
        else:
            new_record_category = record_category.RecordCategory(
                name=name,
                description=description
            )
            db.session.add(new_record_category)
            db.session.commit()
            return new_record_category
    
    def update_record_category(self, new_record_category):
        record_category_obj = self.is_existed(data=new_record_category.id)
        if record_category_obj:
            record_category_obj.name = new_record_category.name
            record_category_obj.description = new_record_category.description
            record_category_obj.updated_at = default_values.TODAY_DATE_TIME
            db.session.commit()
            return record_category_obj
        else:
            return None
    
    def delete_record_category(self, id):
        record_category_obj = self.is_existed(data=id)
        if record_category_obj:
            db.session.delete(record_category_obj)
            db.session.commit()
        return record_category_obj
    
    def get_all_record_category(self):
        record_categories = record_category.RecordCategory.query.all()
        record_categoryList = []
        for record_category_obj in record_categories:
            record_categoryList.append(record_category_obj)
        return record_categoryList
    

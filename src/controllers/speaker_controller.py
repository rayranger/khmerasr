from src import db
from src.models import speaker, user, default_values
from datetime import datetime

class SpeakerController():

    # Check by id
    def is_existed(self, data):
        req = speaker.Speaker.query.filter_by(id=data).first()
        if req:
            return req
        else:
            return None
    
    def create_speaker(self, first_name, last_name, gender, age, occupation, phone_number, user_id):
        new_speaker = speaker.Speaker(
            first_name = first_name,
            last_name = last_name,
            gender = gender,
            age = age,
            occupation = occupation,
            phone_number = phone_number,
            user_id = user_id
        )
        db.session.add(new_speaker)
        db.session.commit()
        return new_speaker
    
    def update_speaker(self, new_speaker_obj, id):
        speaker_obj = self.is_existed(data=id)
        if speaker_obj:
            speaker_obj.first_name = new_speaker_obj.first_name
            speaker_obj.last_name = new_speaker_obj.last_name
            speaker_obj.gender = new_speaker_obj.gender
            speaker_obj.age = new_speaker_obj.age
            speaker_obj.occupation = new_speaker_obj.occupation
            speaker_obj.phone_number = new_speaker_obj.phone_number
            speaker_obj.updated_at = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
            db.session.commit()
            return speaker_obj
        else:
            return None
    
    def delete_speaker(self, id):
        speaker_obj = self.is_existed(data=id)
        if speaker_obj:
            db.session.delete(speaker_obj)
            db.session.commit()
        return speaker_obj

    def get_all_speaker(self):
        speakers = speaker.Speaker.query.all()
        speakerList = []
        for speaker_obj in speakers:
            speakerList.append(speaker_obj)
        return speakerList
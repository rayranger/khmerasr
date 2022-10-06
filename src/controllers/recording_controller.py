from src.models import recording
from src import db
from src.controllers import audio_controller

audioController = audio_controller.AudioController()

class RecordingController():
    
    def is_existed(self, data):
        req = recording.Recording.query.filter_by(id=data).first()
        req_1 = recording.Recording.query.filter_by(sample_filename=data).first()
        if req:
            return req
        elif req_1:
            return req_1
        else:
            return None
    
    def create_task_record(self, transcript, instruction, sample_filename, task_id):
        if self.is_existed(data=sample_filename):
            return None
        else:
            new_task_record = recording.Recording(
                transcript=transcript,
                instruction=instruction,
                sample_filename=sample_filename,
                task_id=task_id
            )
            db.session.add(new_task_record)
            db.session.commit()
            return new_task_record
    
    def update_task_record(self, new_task_record):
        task_record = self.is_existed(data=new_task_record.id)
        if task_record:
            task_record.transcript = new_task_record.transcript
            task_record.instruction = new_task_record.instruction
            task_record.sample_filename = new_task_record.sample_filename
            task_record.task_id = new_task_record.task_id 
            db.session.commit()
        else:
            return None
    
    def delete_task_record(self, id):
        task_record = self.is_existed(data=id)
        if task_record:
            db.session.delete(task_record)
            db.session.commit()
            return task_record
        else:
            return None
    
    def get_all_task_record(self):
        recordings = recording.Recording.query.all()
        recordingList = []
        for recording in recordings:
            recordingList.append(recording)
        return recordingList
    
    def getRemainingRecording(self, speaker_id, selected_task):
        total_recordings = selected_task.recordings
        completed_recordings = audioController.getAllAudioByUser(speakerId=speaker_id)
        remaining_recordings = []

        total_recordings_id = []
        completed_recordings_id=[]
        remaining_recordings_id=[]

        for total_recording in total_recordings:
            total_recordings_id.append(total_recording.id)
        
        for completed_recording in completed_recordings:
            completed_recordings_id.append(completed_recording.id)

        for total_recording_id in total_recordings_id:
            if total_recording_id not in completed_recordings_id:
                remaining_recordings_id.append(total_recording_id)

        for id in remaining_recordings_id:
            recording = self.is_existed(data=id)
            remaining_recordings.append(recording)
        return remaining_recordings
from this import d
from src.models import audio
from datetime import datetime
import soundfile
from src import db
import os.path
import os
import pyaudio

class AudioController():

    FRAMES_PER_BUFFER = 0
    FORMAT = pyaudio.paInt16
    CHANNEL = 0
    RATE = 0
    FILETYPE = ''
    DURATION = 0
    AUDIO_DIR = "src/static/storage/audios/recordings"

    def getRecordConfig(self, frame_per_buffer, channel, rate, filetype, duration):
        self.FRAMES_PER_BUFFER = frame_per_buffer
        self.CHANNEL = channel
        self.RATE = rate
        self.FILETYPE = filetype
        self.DURATION = duration

    def set_audio_filename(self, username):
        return f'{username}_{str(datetime.now().strftime("%d%m%Y_%H%M%S"))}.ogg'

    def is_existed(self, data):
        req = audio.Audio.query.filter_by(id=data).first()
        if req:
            return req
        else:
            return None

    def create_audio(self, filename, recording_id, speaker_id):
        file_path = os.path.join(self.AUDIO_DIR, filename)
        print(file_path)
        if self.is_existed(data=filename):
            return None
        else:
            # data, sample_rate = soundfile.read(file_path)
            new_audio = audio.Audio(
                filename=filename,
                # sample_rate = sample_rate,
                speaker_id = speaker_id,
                recording_id=recording_id
            )
            # print(new_audio)
            db.session.add(new_audio)
            db.session.commit()
            return new_audio
            return None
    
    def delete_audio(self, id):
        audioFile = self.is_existed(data=id)
        if audioFile:
            db.session.delete(audioFile)
            db.session.commit()
            os.remove(f"src/static/storage/audios/recordings/{audioFile.filename}")
            return audioFile
        else:
            return None
    
    def get_all_audio(self):
        records = audio.Audio.query.all()
        recordList = []
        for recordItem in records:
            recordList.append(recordItem)
        return recordList
    
    def getAllAudioByUser(self, speakerId):
        audios = audio.Audio.query.filter_by(speaker_id=speakerId)
        audioList = []
        for audioItem in audios:
            audioList.append(audioItem)
        return audioList
        
        
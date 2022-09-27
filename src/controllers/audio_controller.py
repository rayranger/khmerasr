from src.models import audio
from datetime import datetime
from src import db
import os.path
import wave
import pyaudio

class AudioController():

    FRAMES_PER_BUFFER = 0
    FORMAT = 0
    CHANNEL = 0
    RATE = 0
    FILETYPE = ''
    DURATION = 0
    AUDIO_DIR = "storage/audios"

    def getRecordConfig(self, frame_per_buffer, format, channel, rate, filetype, duration):
        self.FRAMES_PER_BUFFER = frame_per_buffer
        self.FORMAT = format
        self.CHANNEL = channel
        self.RATE = rate
        self.FILETYPE = filetype
        self.DURATION = duration


    def is_existed(self, data):
        req = audio.Record.query.filter_by(id=data).first()
        if req:
            return req
        else:
            return None

    def create_record(self, username):
        FILE_NAME = f'{username}_{str(datetime.now().strftime("%d%m%Y_%H%M%S"))}.{self.FILETYPE}'
        FILE_PATH = os.path.join(self.AUDIO_DIR, FILE_NAME)
        print(FILE_PATH)
        p = pyaudio.PyAudio()
        print("Start stream")
        stream = p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.FRAMES_PER_BUFFER,
            
        )
        # seconds = 3
        frames = []
        for i in range(0, int(self.RATE/self.FRAMES_PER_BUFFER*self.DURATION)):
            data = stream.read(self.FRAMES_PER_BUFFER)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        obj = wave.open(FILE_PATH, "wb")
        obj.setnchannels(self.CHANNELS)
        obj.setsampwidth(p.get_sample_size(self.FORMAT))
        obj.setframerate(self.RATE)
        obj.writeframes(b"".join(frames))
        obj.close()
        return FILE_NAME

    def create_audio(self, filename, category_id, speaker_id):
        file_path = os.path.join(self.AUDIO_DIR, filename)
        if self.is_existed(data=filename):
            return None
        else:
            obj = wave.open(file_path, "rb")
            filetype="wav"
            filesize = obj.getnframes()
            channel = obj.getnchannels()
            sample_framerate = obj.getframerate()
            sample_frame = filesize
            total_frame = obj.readframes(-1)
            duration = sample_framerate / sample_frame
            new_record = audio.Record(
                filename=filename,
                filetype=filetype,
                filesize=filesize,
                channel=channel,
                sample_framerate=sample_framerate,
                sample_frame=sample_frame,
                total_frame=total_frame,
                duration=duration,
                speaker_id = speaker_id,
                category_id=category_id
            )
            db.session.add(new_record)
            db.session.commit()
            return new_record
    
    def delete_record(self, id):
        recordFile = self.is_existed(data=id)
        if recordFile:
            db.session.delete(recordFile)
            db.session.commit()
            return recordFile
        else:
            return None
    
    def get_all_record(self):
        records = audio.Audio.query.all()
        recordList = []
        for recordItem in records:
            recordList.append(recordItem)
        return recordList

    
        
        
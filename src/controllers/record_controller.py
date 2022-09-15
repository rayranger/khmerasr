from src.models import record, default_values
from src import db
import os.path
import wave
import pyaudio

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 160000

class RecordController():

    def is_existed(self, data):
        req = record.Record.query.filter_by(id=data).first()
        if req:
            return req
        else:
            return None

    def record(self, username):
        AUDIO_DIR = "storage/audio"
        FILE_NAME = f'{username}_{str(default_values.TODAY_DATE_TIME)}'
        FILE_PATH = os.path.join(AUDIO_DIR, FILE_NAME)
        p = pyaudio.PyAudio()
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER
        )
        seconds = 3
        frames = []
        for i in range(0, int(RATE/FRAMES_PER_BUFFER*seconds)):
            data = stream.read(FRAMES_PER_BUFFER)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        obj = wave.open(FILE_PATH, "wb")
        obj.setnchannels(CHANNELS)
        obj.setsampwidth(p.get_sample_size(FORMAT))
        obj.setframerate(RATE)
        obj.writeframes(b"".join(frames))
        obj.close()
        return FILE_NAME

    def create_record(self, filename, category_id, speaker_id):
        if self.is_exiting(data=filename):
            return None
        else:
            obj = wave.open(filename, "rb")
            filetype="wav"
            filesize = obj.getnframes()
            channel = obj.getnchannels()
            sample_framerate = obj.getframerate()
            sample_frame = filesize
            total_frame = obj.readframes(-1)
            duration = sample_framerate / sample_frame
            new_record = record.Record(
                filename=filename,
                filetype=filetype,
                filesize=filesize,
                channel=channel,
                sample_framerate=sample_framerate,
                sample_frame=sample_frame,
                total_frame=total_frame,
                duration=duration
            )
            db.session.add(new_record)
            db.session.commit()
            return new_record

    
        
        
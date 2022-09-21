from distutils.command.config import config
from ssl import CHANNEL_BINDING_TYPES
from src.models import audio
from src.controllers import record_config_controller
from datetime import datetime
from src import db
import os.path
import wave
import pyaudio

# recordConfigController = record_config_controller.RecordConfigController()
# recordConfig = recordConfigController.get_all_record_config()

# FRAMES_PER_BUFFER = recordConfig[0].frame_per_buffer
# FORMAT = pyaudio.paInt16
# CHANNELS = recordConfig[0].channel
# RATE = recordConfig[0].sample_rate

AUDIO_DIR = "storage/audios"

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

class RecordController():

    def is_existed(self, data):
        req = audio.Record.query.filter_by(id=data).first()
        if req:
            return req
        else:
            return None

    def record(self, username):
        FILE_NAME = f'{username}_{str(datetime.now().strftime("%d%m%Y_%H%M%S"))}.wav'
        FILE_PATH = os.path.join(AUDIO_DIR, FILE_NAME)
        print(FILE_PATH)
        p = pyaudio.PyAudio()
        print("Start stream")
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER,
            
        )
        seconds = 3
        # seconds = recordConfig[0].duration
        print('recording for 3 seconds')
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
        file_path = os.path.join(AUDIO_DIR, filename)
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
        records = audio.Record.query.all()
        recordList = []
        for recordItem in records:
            recordList.append(recordItem)
        return recordList

    
        
        
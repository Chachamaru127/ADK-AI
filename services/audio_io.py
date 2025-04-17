import asyncio
import sounddevice as sd
import simpleaudio as sa
from event_bus import EventBus

class AudioIOService:
    def __init__(self, sample_rate=48000, channels=1, chunk_size=1024):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size

    def record_generator(self):
        with sd.InputStream(samplerate=self.sample_rate, channels=self.channels, dtype="int16") as stream:
            while True:
                data = stream.read(self.chunk_size)[0]
                yield data

    def play(self, audio_bytes):
        play_obj = sa.play_buffer(audio_bytes, num_channels=self.channels, bytes_per_sample=2, sample_rate=self.sample_rate)
        while play_obj.is_playing():
            asyncio.sleep(0.1)
            # 再生中の500ms以上の入力を検知したら割り込みとする実装を追加
        EventBus.publish("USER_INTERRUPT")

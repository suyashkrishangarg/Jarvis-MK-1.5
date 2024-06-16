import pvporcupine
import pyaudio
import struct

keywords = ['ok google', 'jarvis', 'hey google', 'alexa']

def hotword_detection():
    porcupine = pvporcupine.create(keywords=keywords)
    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
    try:
        # print("Listening for hotwords...")
        while True:
            audio_data = audio_stream.read(porcupine.frame_length)
            audio_data = struct.unpack_from("h" * porcupine.frame_length, audio_data)
            keyword_index = porcupine.process(audio_data)
            if keyword_index >= 0:
                # detected_keyword = keywords[keyword_index]
                # print(f"Hotword detected: {detected_keyword}")
                return True
    except:
        pass
    finally:
        audio_stream.close()
        audio_interface.terminate()
        porcupine.delete()

if __name__ == "__main__":
    wotd=hotword_detection()
    if wotd==True:
        print("aahaa")
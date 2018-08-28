# Record Screen Methods
import kivy
kivy.require('1.10.1')

import threading
import pyaudio
import wave

import config
from kivy.uix.button import Button

stopRecording = True
stopEvent = threading.Event()

def recordAudio():
    
    print('Record was called')
    global stopRecording
    global stopEvent

    stopRecording = not stopRecording

    #Change next line based on recording mode selection
    duplicateLines = [i for i, line in enumerate(config.fullLineList) if line == config.lineList[config.lineNum]]
    fileName = 'line' + str(duplicateLines[0]) + 'audio.wav'
    print(fileName)
    #Recording Script
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    p = pyaudio.PyAudio()

    def startRecording():
        stream = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK)

        print("* recording")

        frames = []
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
            if stopEvent.is_set():
            # Stop running this thread so the main Python process can exit.
                finishRecording(stream, frames)
                return

    def finishRecording(stream, frames):
        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(fileName, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        #Save recording to file
        for line in duplicateLines:
            config.audioFiles[line] = fileName 

    if not stopRecording:
        threading.Thread(target=startRecording).start()
    else:
        stopEvent.set()


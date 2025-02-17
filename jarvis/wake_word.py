import pvporcupine
import pyaudio
import struct

def listen_for_wake_word():
    porcupine = pvporcupine.create(keywords=["jarvis"])
    pa = pyaudio.PyAudio()
    
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=porcupine.sample_rate,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )
    print("Listening for 'Hi Jarvis'...")

    try:
        while True:
            pcm = stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            if porcupine.process(pcm) >= 0:
                print("Wake word detected! Jarvis is ready!")
                # Call the activation logic
                activate_jarvis()
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        stream.close()
        pa.terminate()
        porcupine.delete()

def activate_jarvis():
    print("Hello Khushank, how can I assist you today?")
    # Add further assistant activation logic here

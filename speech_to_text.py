import whisper
import pyaudio
import wave
import torch

# Initialize the whisper model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base").to(device)  # You can choose other models like 'small', 'medium', 'large'

# Record audio using the microphone
def record_audio(filename="audio.wav", duration=5):
    p = pyaudio.PyAudio()

    # Set up the audio stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=1024)

    print("Recording... (speak to record, silence to stop)")
    frames = []
    
    # Record until silence is detected
    silence_threshold = 500  # Adjust this value based on testing
    silence_count = 0
    max_silence_count = 30  # About 1 second of silence before stopping
    
    while True:
        data = stream.read(1024)
        frames.append(data)
        
        # Convert bytes to integers
        audio_data = [int.from_bytes(data[i:i+2], byteorder='little', signed=True) 
                     for i in range(0, len(data), 2)]
        
        # Check amplitude
        amplitude = max(abs(x) for x in audio_data)
        
        if amplitude < silence_threshold:
            silence_count += 1
        else:
            silence_count = 0
            
        if silence_count >= max_silence_count and len(frames) > 16:  # Ensure we have at least 1s of audio
            break

    print("Recording complete.")
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save audio to a file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))

# Convert the recorded audio to text using Whisper
def transcribe_audio(filename="audio.wav"):
    print("Transcribing audio...")
    result = model.transcribe(filename)
    print(f"Transcription: {result['text']}")
    return result['text']

# Record and transcribe
if __name__ == "__main__":
    record_audio(duration=5)  # You can adjust the duration to record longer or shorter
    transcribe_audio()

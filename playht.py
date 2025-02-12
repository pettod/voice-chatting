from pyht import Client
from dotenv import load_dotenv
from pyht.client import TTSOptions
from pydub import AudioSegment
from pydub.playback import play

load_dotenv()

with open('user_id.txt', 'r') as f:
    PLAY_HT_USER_ID = f.read().strip()
with open('api_key.txt', 'r') as f:
    PLAY_HT_API_KEY = f.read().strip()

client = Client(
    user_id=PLAY_HT_USER_ID,
    api_key=PLAY_HT_API_KEY,
)
options = TTSOptions(voice="s3://voice-cloning-zero-shot/0798c0dc-192e-4e1e-9cca-798c442654a7/original/manifest.json")
# Open a file to save the audio
output_file = "output_peter.wav"
with open(output_file, "wb") as audio_file:
    for chunk in client.tts("Hi, I'm Peter's cloned voice using Play. How are you doing today?", options, voice_engine = 'PlayDialog-http'):
        # Write the audio chunk to the file
        audio_file.write(chunk)

# Play the audio
audio = AudioSegment.from_file(output_file)
play(audio)

print(f"Audio saved as {output_file}")

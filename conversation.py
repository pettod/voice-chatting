import requests
from pydub import AudioSegment
from pydub.playback import play
from pyht import Client
from pyht.client import TTSOptions
from groq import generate_response, read_api_key
from speech_to_text import record_audio, transcribe_audio

PERSON = "peter"
# Set API keys
# ElevenLabs
with open('api_keys/elevenlabs_api_key.txt', 'r') as f:
    ELEVENLABS_API_KEY = f.read().strip()
with open('api_keys/elevenlabs_voice_id_peter.txt', 'r') as f:
    VOICE_ID = f.read().strip()  # ElevenLabs voice ID
# Play.ai
with open(f'api_keys/playht_user_id_{PERSON}.txt', 'r') as f:
    PLAY_HT_USER_ID = f.read().strip()
with open(f'api_keys/playht_api_key_{PERSON}.txt', 'r') as f:
    PLAY_HT_API_KEY = f.read().strip()
with open(f'api_keys/playht_voice_id_{PERSON}.txt', 'r') as f:
    PLAY_HT_VOICE_ID = f.read().strip()
# Groq
GROQ_API_KEY = read_api_key()

client = Client(
    user_id=PLAY_HT_USER_ID,
    api_key=PLAY_HT_API_KEY,
)

def play_ht_tts(text, output_file="ai_response.wav"):
    options = TTSOptions(voice=PLAY_HT_VOICE_ID)
    with open(output_file, "wb") as audio_file:
        for chunk in client.tts(text, options, voice_engine = 'PlayDialog-http'):
            audio_file.write(chunk)
    return output_file

# Convert AI response to speech using ElevenLabs
def text_to_speech(text, output_file="ai_response.mp3"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.7}
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        return output_file
    else:
        print("Error generating speech:", response.text)
        return None

# Main conversational loop
def main():
    while True:
        record_audio()
        text = transcribe_audio()

        ai_response = generate_response(text, GROQ_API_KEY)
        print("AI:", ai_response)

        audio_file = text_to_speech(ai_response)
        if audio_file:
            audio = AudioSegment.from_file(audio_file)
            play(audio)

if __name__ == "__main__":
    main()



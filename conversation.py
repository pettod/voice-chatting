import requests
from pydub import AudioSegment
from pydub.playback import play

from groq import generate_response, read_api_key
from speech_to_text import record_audio, transcribe_audio

# Set API keys
with open('elevenlabs_api_key.txt', 'r') as f:
    ELEVENLABS_API_KEY = f.read().strip()
with open('elevenlabs_voice_id_peter.txt', 'r') as f:
    VOICE_ID = f.read().strip()  # ElevenLabs voice ID

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
    groq_api_key = read_api_key()
    while True:
        record_audio()
        text = transcribe_audio()

        ai_response = generate_response(text, groq_api_key)
        print("AI:", ai_response)

        audio_file = text_to_speech(ai_response)
        if audio_file:
            audio = AudioSegment.from_file(audio_file)
            play(audio)

if __name__ == "__main__":
    main()



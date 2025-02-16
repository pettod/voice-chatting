from bottle import route, run, request, response, static_file   
import time
import argparse
from twilio.twiml.voice_response import VoiceResponse

from groq import generate_response
from speech_to_text import transcribe_audio
from conversation import text_to_speech, GROQ_API_KEY, play_ht_tts
from aws_polly import aws_text_to_speech

MODEL = "aws" # Options: "elevenlabs", "playht", "aws"

@route('/')
def index():
    return static_file('index.html', root='.')

@route('/process-audio', method='POST')
def process_audio():
    # Get the uploaded audio file
    audio_file = request.files.get('audio')
    audio_data = audio_file.file.read()
    if ECHO:
        time.sleep(2)
    else:
        # Save the uploaded audio file
        audio_filename = 'audio.wav'
        with open(audio_filename, 'wb') as f:
            f.write(audio_data)
        text = transcribe_audio(audio_filename)
        ai_response = generate_response(text, GROQ_API_KEY)
        
        if MODEL == "playht":
            audio_filename = play_ht_tts(ai_response)
            with open(audio_filename, 'rb') as f:
                audio_data = f.read()
        elif MODEL == "aws":
            audio_data = aws_text_to_speech(ai_response)
        else: # elevenlabs
            audio_filename = text_to_speech(ai_response)
            with open(audio_filename, 'rb') as f:
                audio_data = f.read()

    if audio_file:
        # Set response headers for audio file
        response.headers['Content-Type'] = 'audio/wav'
        
        # Return the same audio data
        return audio_data
    
    return {'error': 'No audio file received'}

@route('/voice', method='POST')
def voice():
    user_speech = request.forms.get("SpeechResult", "Hello")  # Capture user's speech
    ai_response = generate_response(user_speech, GROQ_API_KEY)
    audio_data = aws_text_to_speech(ai_response)
    audio_filename = 'audio.mp3'
    with open(audio_filename, 'wb') as f:
        f.write(audio_data)

    response = VoiceResponse()
    response.play(f"https://rauha.co.uk/{audio_filename}")
    
    return str(response)

@route('/<filename>', method='GET')
def get_audio(filename):
    try:
        # Set response headers for audio file
        response.headers['Content-Type'] = 'audio/mpeg'
        
        # Read and return the audio file
        with open(filename, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        response.status = 404
        return {'error': 'Audio file not found'}

# Run the server
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--global', action='store_true', help='Run server globally on 0.0.0.0')
    parser.add_argument('--port', type=int, default=8080, help='Port to run server on')
    parser.add_argument('--echo', action='store_true', help='Echo back the uploaded audio file')
    args = parser.parse_args()
    ECHO = args.echo

    # ipconfig getifaddr en0
    host = '0.0.0.0' if getattr(args, 'global') else 'localhost'
    run(host=host, port=args.port)

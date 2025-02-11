from bottle import route, run, request, response, static_file
import time
import argparse

from groq import generate_response
from speech_to_text import transcribe_audio
from conversation import text_to_speech, GROQ_API_KEY, VOICE_ID, ELEVENLABS_API_KEY

ECHO = False

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
        audio_filename = text_to_speech(ai_response)
        with open(audio_filename, 'rb') as f:
            audio_data = f.read()

    if audio_file:
        # Set response headers for audio file
        response.headers['Content-Type'] = 'audio/wav'
        
        # Return the same audio data
        return audio_data
    
    return {'error': 'No audio file received'}

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

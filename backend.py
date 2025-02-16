from bottle import route, run, request, response, static_file   
import time
import argparse
from twilio.twiml.voice_response import VoiceResponse, Gather

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
    start_time = time.time()
    
    # Create a TwiML response
    response = VoiceResponse()
    
    # Check if we have speech results
    user_speech = request.forms.get("SpeechResult", "Hello")
    stt_time = time.time() - start_time
    
    if user_speech:
        # Generate AI response and play it
        print(f"User: {user_speech}")
        
        gen_start = time.time()
        ai_response = generate_response(user_speech, GROQ_API_KEY)
        gen_time = time.time() - gen_start
        print(f"AI: {ai_response}")
        
        tts_start = time.time()
        audio_data = aws_text_to_speech(ai_response)
        tts_time = time.time() - tts_start
        
        audio_filename = 'audio.mp3'
        with open(audio_filename, 'wb') as f:
            f.write(audio_data)
        
        response.play(f"https://rauha.co.uk/{audio_filename}")
    
    # Add speech recognition gathering
    gather = Gather(input='speech', action='/voice', method='POST', speechTimeout=0.7)
    response.append(gather)
    
    total_time = time.time() - start_time

    print(f"{stt_time:.2f}s Speech-to-text")
    print(f"{gen_time:.2f}s Llama response")
    print(f"{tts_time:.2f}s Text-to-speech")
    print(f"{total_time:.2f}s Total voice processing")
    
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

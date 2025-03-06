from bottle import route, run, request, response, static_file, redirect, template   
import time
import argparse
from twilio.twiml.voice_response import VoiceResponse, Gather
import json
import os
from datetime import datetime

from groq import generate_response
from speech_to_text import transcribe_audio
from conversation import text_to_speech, GROQ_API_KEY, play_ht_tts
from aws_polly import aws_text_to_speech
from telegram_bot import send_telegram_notification
from create_email_list import create_email_list

MODEL = "aws" # Options: "elevenlabs", "playht", "aws"

# Password for accessing the email list
EMAIL_LIST_PASSWORD = "hackerhouse"  # You should change this to a secure password

@route('/')
def index():
    return static_file('landing_page.html', root='.')

@route('/demo')
def demo():
    return static_file('demo.html', root='.')

@route('/email-list', method=['GET', 'POST'])
def email_list():
    if request.method == 'POST':
        password = request.forms.get('password')
        if password == EMAIL_LIST_PASSWORD:
            return create_email_list()
        else:
            return template('email_password.html', error=True)
    else:
        return template('email_password.html', error=False)

@route('/process-audio', method='POST')
def process_audio():
    start_time = time.time()
    
    # Get the uploaded audio file
    audio_file = request.files.get('audio')
    system_prompt = request.forms.get('personality')
    model = request.forms.get('model') or MODEL
    voice = request.forms.get('voice') or None
    language = request.forms.get('language') or "english"
    if language != "english":
        system_prompt += f" Speak only {language}."
    
    audio_data = audio_file.file.read()
    if ECHO:
        time.sleep(2)
    else:
        # Save the uploaded audio file
        audio_filename = 'audio.wav'
        with open(audio_filename, 'wb') as f:
            f.write(audio_data)
            
        stt_start = time.time()
        text = transcribe_audio(audio_filename)
        stt_time = time.time() - stt_start
        
        gen_start = time.time()
        ai_response = generate_response(text, GROQ_API_KEY, system_prompt, 3000)
        gen_time = time.time() - gen_start
        
        tts_start = time.time()
        if model == "playht":
            audio_filename = play_ht_tts(ai_response)
            with open(audio_filename, 'rb') as f:
                audio_data = f.read()
        elif model == "aws":
            print(language)
            if language:
                language_voice_map = {
                    "finnish": "Suvi",
                    "english": "Danielle",
                    "swedish": "Astrid",
                    "german": "Vicki",
                    "french": "Léa",
                    "spanish": "Lucia",
                    "italian": "Bianca",
                    "portuguese": "Camila",
                    "polish": "Ewa",
                    "danish": "Naja",
                    "norwegian": "Liv",
                    "dutch": "Laura"
                }
                
                # Override voice with language-specific voice if available
                if language.lower() in language_voice_map:
                    voice = language_voice_map[language.lower()]
            audio_data = aws_text_to_speech(ai_response, voice_id=voice)
        else: # elevenlabs
            audio_filename = text_to_speech(ai_response, voice=voice, language=language)
            with open(audio_filename, 'rb') as f:
                audio_data = f.read()
        tts_time = time.time() - tts_start

    if audio_file:
        # Set response headers for audio file
        response.headers['Content-Type'] = 'audio/wav'
        
        total_time = time.time() - start_time
        
        if not ECHO:
            print(f"{stt_time:.2f}s Speech-to-text")
            print(f"{gen_time:.2f}s AI response")
            print(f"{tts_time:.2f}s Text-to-speech") 
            print(f"{total_time:.2f}s Total processing")
            
        # Return the same audio data
        return audio_data
    
    return {'error': 'No audio file received'}

@route('/voice', method='POST')
def voice():
    start_time = time.time()
    
    # Create a TwiML response
    response = VoiceResponse()
    
    # Check if we have speech results
    user_speech = request.forms.get("SpeechResult")
    stt_time = time.time() - start_time
        
    gen_start = time.time()
    if user_speech:
        print(f"User: {user_speech}")
        ai_response = generate_response(user_speech, GROQ_API_KEY)
    else:
        ai_response = "Hello. This is your AI friend helping you to keep your cognitive skills up to date. How are you doing today?"

    # Generate AI response and play it
    gen_time = time.time() - gen_start
    print(f"AI: {ai_response}")    
    tts_start = time.time()
    audio_data = aws_text_to_speech(ai_response)
    tts_time = time.time() - tts_start
    audio_filename = 'audio.mp3'
    with open(audio_filename, 'wb') as f:
        f.write(audio_data)    
    
    # Add speech recognition gathering
    gather = Gather(input="speech dtmf", speechTimeout=1.0, bargeIn=True, action='/voice', method='POST')
    gather.play(f"https://rauha.co.uk/{audio_filename}")
    response.append(gather)
    print(response)
    
    total_time = time.time() - start_time

    print(f"{stt_time:.2f}s Speech-to-text")
    if user_speech:
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

@route('/send-email', method='POST')
def send_email():
    try:
        # Get the email from the request body
        body = request.body.read().decode('utf-8')
        data = json.loads(body)
        email = data.get('email')
        
        if not email:
            response.status = 400
            return {'success': False, 'error': 'Email is required'}
        
        # Create emails directory if it doesn't exist
        os.makedirs('emails', exist_ok=True)
        
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Append the email and timestamp to the emails.txt file
        with open('emails/emails.txt', 'a') as f:
            f.write(f"{timestamp} - {email}\n")

        send_telegram_notification(email)

        return {'success': True}
    except Exception as e:
        response.status = 500
        return {'success': False, 'error': str(e)}

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

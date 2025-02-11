from bottle import route, run, request, response, static_file
import time
import argparse

@route('/')
def index():
    return static_file('index.html', root='.')

@route('/process-audio', method='POST')
def process_audio():
    # Get the uploaded audio file
    audio_file = request.files.get('audio')
    time.sleep(2)
    
    if audio_file:
        # Set response headers for audio file
        response.headers['Content-Type'] = 'audio/wav'
        
        # Return the same audio data
        return audio_file.file.read()
    
    return {'error': 'No audio file received'}

# Run the server
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--global', action='store_true', help='Run server globally on 0.0.0.0')
    parser.add_argument('--port', type=int, default=8080, help='Port to run server on')
    args = parser.parse_args()

    # ipconfig getifaddr en0
    host = '0.0.0.0' if getattr(args, 'global') else 'localhost'
    run(host=host, port=args.port)

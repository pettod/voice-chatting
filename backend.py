from bottle import route, run, request, response, static_file
import time

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
    run(host='localhost', port=8080)

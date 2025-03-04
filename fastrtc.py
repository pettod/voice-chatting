from fastrtc import (ReplyOnPause, Stream, get_stt_model, get_tts_model)

from groq import generate_response, read_api_key

GROQ_API_KEY = read_api_key()
stt_model = get_stt_model()
tts_model = get_tts_model()

def echo(audio):
    prompt = stt_model.stt(audio)
    print("User:", prompt)
    ai_response = generate_response(prompt, GROQ_API_KEY)
    for audio_chunk in tts_model.stream_tts_sync(ai_response):
        yield audio_chunk

stream = Stream(ReplyOnPause(echo), modality="audio", mode="send-receive")
stream.ui.launch()

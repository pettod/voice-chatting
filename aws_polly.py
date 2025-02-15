from boto3 import client
from contextlib import closing

def read_key_from_file(filename):
    with open(f"api_keys/{filename}", "r") as f:
        return f.read().strip()

AWS_ACCESS_KEY_ID = read_key_from_file("aws_access_key_id.txt")
AWS_SECRET_ACCESS_KEY = read_key_from_file("aws_secret_access_key.txt")

POLLY = client(
    "polly",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name="eu-west-2",  # Change to your region
)

def aws_text_to_speech(text, voice_id="Danielle", output_format="mp3"):
    """
    Convert text to speech using AWS Polly and return the audio data
    """
    response = POLLY.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id,
        Engine="neural",
    )
    
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            return stream.read()
    return None

if __name__ == "__main__":
    test_text = "Good Morning. My Name is Joanna. I am Testing Polly AWS Service For Voice Application."
    audio_data = aws_text_to_speech(test_text)
    
    if audio_data:
        with open("pollytest.mp3", "wb") as f:
            f.write(audio_data)
        print("Successfully created pollytest.mp3")
    else:
        print("Failed to generate speech")

import requests
import time

def generate_heygen_video(api_key: str, audio_url: str, avatar_id: str = "Angela-inTshirt-20220820"):
    """
    Generate a video using HeyGen API with a specified avatar and audio URL.
    
    Args:
        api_key (str): Your HeyGen API key
        audio_url (str): URL of the audio file to use
        avatar_id (str, optional): Avatar ID to use. Defaults to "Angela-inTshirt-20220820"
    
    Returns:
        str: URL of the generated video if successful
    """
    # Base URL for HeyGen API
    base_url = "https://api.heygen.com"
    
    # Headers for API requests
    headers = {
        'X-Api-Key': api_key,
        'Accept': 'application/json'
    }
    
    # Step 1: Generate video
    generate_url = f"{base_url}/v2/video/generate"
    
    # Create the request payload
    payload = {
        "video_inputs": [{
            "character": {
                "type": "avatar",
                "avatar_id": avatar_id,
                "avatar_style": "normal"
            },
            "voice": {
                "type": "audio",
                "audio_url": audio_url
            }
        }],
        "dimension": {
            "width": 1280,
            "height": 720
        }
    }
    
    # Make the generate video request
    response = requests.post(generate_url, headers=headers, json=payload)
    response.raise_for_status()
    
    # Get video ID from response
    video_id = response.json()['data']['video_id']
    
    # Step 2: Poll for video status
    status_url = f"{base_url}/v1/video_status.get"
    
    while True:
        # Check video status
        status_response = requests.get(
            status_url,
            headers=headers,
            params={'video_id': video_id}
        )
        status_response.raise_for_status()
        
        status_data = status_response.json()['data']
        current_status = status_data['status']
        
        if current_status == 'completed':
            return status_data['video_url']
        elif current_status == 'failed':
            error_details = status_data.get('error', {}).get('detail', 'Unknown error')
            raise Exception(f"Video generation failed: {error_details}")
        elif current_status in ['processing', 'pending', 'waiting']:
            print(f"Video status: {current_status}. Waiting...")
            time.sleep(10)  # Wait 10 seconds before checking again
        else:
            raise Exception(f"Unknown status: {current_status}")

# Example usage
if __name__ == "__main__":
    with open('api_keys/heygen_api_key.txt', 'r') as f:
        API_KEY = f.read().strip()
    AUDIO_URL = "https://rauha.co.uk/audio.mp3"  # Must be a publicly accessible URL
    
    # Using default avatar
    video_url = generate_heygen_video(API_KEY, AUDIO_URL)
    
    print(f"Video generated successfully! URL: {video_url}")
    
    # Download the video
    response = requests.get(video_url)
    if response.status_code == 200:
        with open("output_video.mp4", "wb") as f:
            f.write(response.content)
        print("Video downloaded as 'output_video.mp4'")
import requests


def read_api_key():
    try:
        with open('api_keys/groq_api_key.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Error: groq_api_key.txt file not found")
        return None


def generate_response(prompt, api_key, system_prompt="You are a conversational person. Respond in a natural way.", max_characters=None):
    if system_prompt == "":
        system_prompt = "You are a conversational person. Respond in a natural way."

    # Set the API endpoint URL
    url = "https://api.groq.com/openai/v1/chat/completions"

    # Set the headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Define the payload with the prompt
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.8,  # Slightly higher temperature for more creative responses
        "max_tokens": 1000
    }

    try:
        # Send the POST request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raises an error for HTTP errors

        # Parse the JSON response
        data = response.json()
        response_text = data["choices"][0]["message"]["content"]
        
        # Limit response length if max_characters is specified
        if max_characters:
            response_text = response_text[:max_characters]
            
        return response_text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Example usage
if __name__ == "__main__":
    prompt = "How are you"
    api_key = read_api_key()
    response = generate_response(prompt, api_key)
    if response:
        print("Generated Response:")
        print(response)
    else:
        print("Failed to generate a response.")
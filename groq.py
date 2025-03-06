import requests


# TODO: Reset conversation history when a new conversation starts
# Make individual conversations, so different users won't mix their conversations
conversation_history = []


def read_api_key():
    try:
        with open('api_keys/groq_api_key.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Error: groq_api_key.txt file not found")
        return None


def add_to_conversation_history(role, content, history_length=30):
    conversation_history.append({"role": role, "content": content})
    if len(conversation_history) > history_length:
        conversation_history.pop(0)


def generate_response(prompt, api_key, system_prompt="", max_characters=None):
    system_prompt = f"You are a conversational person. Respond in a natural way. {system_prompt}"

    # Set the API endpoint URL
    url = "https://api.groq.com/openai/v1/chat/completions"

    # Set the headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    add_to_conversation_history("user", prompt)

    # Define the payload with the prompt
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": system_prompt,
            },
            *conversation_history,
        ],
        "temperature": 0.7,  # Slightly higher temperature for more creative responses
        "max_tokens": 500,
        "presence_penalty": 0.6,  # Penalize new tokens based on whether they appear in the text so far
        "frequency_penalty": 0.7,  # Penalize new tokens based on their frequency in the text so far
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
        add_to_conversation_history("assistant", response_text)

        print("AI response:", response_text)
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
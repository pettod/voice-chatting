import requests

# Read Telegram credentials from api_keys directory
with open('api_keys/telegram_bot_token.txt', 'r') as f:
    TELEGRAM_BOT_TOKEN = f.read().strip()
with open('api_keys/telegram_chat_id.txt', 'r') as f:
    TELEGRAM_CHAT_ID = f.read().strip()

def send_telegram_notification(new_user_email):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": new_user_email}

    response = requests.post(url, data=data)
    print(response.json())  # Print response for debugging

# Example usage
if __name__ == "__main__":
    send_telegram_notification("newuser@example.com")

import requests

url = "https://api.play.ht/api/v2/cloned-voices"
# Read API key and user ID from files
with open('api_keys/playht_api_key_peter.txt') as f:
    api_key = f.read().strip()

with open('api_keys/playht_user_id_peter.txt') as f:
    user_id = f.read().strip()

headers = {
    "accept": "application/json",
    "AUTHORIZATION": api_key,
    "X-USER-ID": user_id,
}

response = requests.get(url, headers=headers)

for voice in response.json():
    print("id:", voice["id"])
    print("name:", voice["name"])
    print("type:", voice["type"])
    print("gender:", voice["gender"])
    print("voice_engine:", voice["voice_engine"])
    print()

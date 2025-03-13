# Voice Cloning

![Video](https://github.com/user-attachments/assets/224a097d-20dc-459e-b1e6-bc34fcc10c4f)

![Image](https://github.com/user-attachments/assets/1c6724c5-33b6-4585-86b1-6ec6873332e5)

## Installation

```bash
sudo apt-get install portaudio19-dev
pip install -r requirements.txt
```

## Run

### Turn on the server

Localhost

```bash
python backend.py --port 8080
```

Global host

```bash
python backend.py --port 8080 --global
```

Open the client in a browser: [http://localhost:8080](http://localhost:8080)

### Run the client

#### Make a phone call

```bash
python phone_call.py --phone <phone_number>
```

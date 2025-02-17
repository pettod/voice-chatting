# Voice Cloning

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

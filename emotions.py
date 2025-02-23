from speechbrain.inference.interfaces import foreign_class

EMOTION_MODEL = foreign_class(source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP", pymodule_file="custom_interface.py", classname="CustomEncoderWav2vec2Classifier")
EMOTION_MAP = {
    "ang": "Anger",
    "hap": "Happiness",
    "sad": "Sadness",
    "fea": "Fear",
    "dis": "Disgust",
    "sur": "Surprise",
    "neu": "Neutral",
}

def get_emotions(audio_filename):
    out_prob, score, index, text_lab = EMOTION_MODEL.classify_file(audio_filename)
    emotions = [EMOTION_MAP[emotion] for emotion in text_lab]
    print("Emotions:", emotions)
    sentence = f"The user is feeling {', '.join(emotions)}."
    return sentence

from flask import Flask, render_template, request
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

# Ensure static/audio folder exists
os.makedirs(os.path.join("static", "audio"), exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def translate():
    translated = None
    audio_file = None

    if request.method == 'POST':
        text = request.form['text']
        target_lang = request.form['lang'].lower().strip()

        try:
            # Translate text using GoogleTranslator
            translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
            
            # Generate unique audio file name
            audio_file = f"{uuid.uuid4()}.mp3"
            audio_path = os.path.join("static", "audio", audio_file)
            
            # Generate audio with gTTS
            tts = gTTS(text=translated, lang=target_lang)
            tts.save(audio_path)
        except Exception as e:
            translated = "Error: Language code not supported or TTS failed!"
            audio_file = None

    return render_template('index.html', translated=translated, audio_file=audio_file)

if __name__ == "__main__":
    app.run(debug=True)

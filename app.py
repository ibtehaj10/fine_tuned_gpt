from flask import Flask, request, jsonify,render_template,send_from_directory
from gtts import gTTS
import openai
from flask_cors import CORS
from config import apikey
import requests
import speech_recognition as sr 
import random

app = Flask(__name__)
CORS(app)



openai.api_key = apikey

# openai.api_key = apikey

def openais(message):
    res = openai.Completion.create(
                model="davinci:ft-proxima-2023-02-01-13-33-15",
                prompt=message,
                max_tokens=150,
                temperature=0.6,
            )
    r = res.choices[0].text 
    return r



@app.route('/')
def main():
    return render_template('chatbox.html')



######################## VOICE GPT #############################################################################
@app.route('/transcript', methods=['POST'])
def transcribe():
    transcript = request.json['transcript']
    print(transcript)
    res = openais(transcript)
    tts = gTTS(res)
    audio_file = 'audio.mp3'
    tts.save(audio_file)
    return jsonify({'audio_file': audio_file,'text':res})

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory('.', filename)


######################## VOICE GPT #############################################################################
@app.route("/get", methods=("GET", "POST"))
def index():
    usertext = request.args.get('msg')
    print("User text in chat",usertext)
    # if request.method == "GET":
      
    result = openais(usertext)
    print("results in rasa for chat : ",result)
    return  result


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)

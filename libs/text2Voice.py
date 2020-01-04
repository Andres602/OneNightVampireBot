# -*- coding: utf-8 -*-
import requests
import json
import base64

class text2Voice:

    def __init__(self, token,path):
        self.url = "https://texttospeech.googleapis.com/v1/text:synthesize?key=" + token
        self.path=path


    def buildUrl(self, payload):
        r = requests.post(self.url,data=json.dumps(payload))
        return json.loads(r.text)

        

    def toVoice(self, text):
        message = { 
            "input": { "text": text }, 
            "voice": { "languageCode": "es-ES" },
            "audioConfig": {
            "audioEncoding": "MP3",
            "volumeGainDb": 6 }
        }
        post = self.buildUrl(message)
        return post

    def save_audio(self,audio):
        audio_64_decode=base64.b64decode(audio)
        audio_result = open(self.path, 'wb')
        audio_result.write(audio_64_decode)


text="""Bienvenidos sean todos."""

def main():
    myVoice = text2Voice('GOOGLE API KEY')
    audio=myVoice.toVoice(text)
    myVoice.save_audio(audio["audioContent"])

if __name__ == "__main__":
    main()


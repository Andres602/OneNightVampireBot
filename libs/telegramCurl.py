# -*- coding: utf-8 -*-
import pycurl
import certifi
import json
from StringIO import StringIO
from urllib import urlencode


class telegramBot:

    def __init__(self, token):
        self.url = "https://api.telegram.org/bot" + token + "/"
        self.c = pycurl.Curl()

    def close(self):
        self.c.close()

    def buildUrl(self, method, options=None):
        storage = StringIO()
        self.c.setopt(pycurl.CAINFO, certifi.where())
        self.c.setopt(self.c.URL,  self.url + method)
        if(options != None):
            postfields = urlencode(options)
            self.c.setopt(self.c.POSTFIELDS, postfields)
        self.c.setopt(self.c.WRITEFUNCTION, storage.write)
        self.c.perform()
        content = storage.getvalue()
        return json.loads(content)

    def uploadFile(self, method,options):
        storage = StringIO()
        self.c.setopt(self.c.URL,  self.url + method)
        self.c.setopt(self.c.HTTPPOST, options)
        self.c.perform()
        return self.c.getinfo(pycurl.RESPONSE_CODE)
        
    def getMe(self):
        return self.buildUrl("getMe") 

    def getUpdates(self, offset=False):
        return self.buildUrl("getUpdates", {'offset': offset}) if offset else self.buildUrl("getUpdates")

    def sendMessage(self, id, text, replymarkup=False):
        message = {"chat_id": id, "text": text, "parse_mode": "Markdown"}
        if(replymarkup):
            message['reply_markup'] = replymarkup
        post = self.buildUrl("sendMessage", message)
        return post

    def replyTo(self, m, text):
        message = {
            "chat_id": m['chat']['id'],
            "text": text,
            "parse_mode": "Markdown",
            "reply_to_message_id": m['message_id']
        }
        post = self.buildUrl('sendMessage', message)
        return post

    def editMessage(self, id, msg_id, text, replymarkup=False):
        message = {
            "chat_id": id,
            "message_id": msg_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        if(replymarkup):
            message['reply_markup'] = replymarkup
        post = self.buildUrl('editMessageText', message)
        return post

    def ansCBQuery(self, id, text, alert=False):
        message = {
            "callback_query_id ": id,
            "text": text,
            "parse_mode": "Markdown"
        }
        if(alert):
            message['show_alert'] = alert
        post = self.buildUrl('answerCallbackQuery', message)
        return post

    def sendFile(self,id,sendType,fileIn,caption=False):
        field='voice' if sendType == 'sendVoice' else 'audio' if sendType == 'sendAudio' else 'document'
        objetData = [("chat_id", str(id)), (field, (pycurl.FORM_FILE, fileIn))]
        if caption:
            objectData.append(("caption", caption))
        post = self.uploadFile(sendType, objetData)
        return post

    def makeKeyboard(self, keys,size,inline=False):
        i=0
        j=0
        keyboard=[]
        row=[]
        keys_len=len(keys)/2 if inline else len(keys)
        for k in range(keys_len):
            if j==size[i]:
                keyboard.append(row)
                row=[]
                i+=1
                j=0                
            key={'text': keys[k*2], 'callback_data': keys[k*2+1]} if inline else {'text':keys[k]}
            row.append(key)
            j+=1
        if len(row):
            keyboard.append(row)
        return json.dumps({'inline_keyboard': keyboard}) if inline else json.dumps({'keyboard': keyboard, 'one_time_keyboard':True, 'resize_keyboard':True})


def main():
    bot = telegramBot('TELEGRAM TOKEN')
    print bot.getMe()
    bot.getUpdates()
    keys=bot.makeKeyboard([0,1,2,3,4,5],[1,5])
    print bot.sendFile(5951788, 'sendAudio','./files/4.Wav',"hola Mundo")
    bot.close()

if __name__ == "__main__":
    main()


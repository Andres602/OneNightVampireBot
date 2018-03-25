#!/usr/bin/python
# -*- coding: utf-8 -*-
from telegramCurl import telegramBot
import json
import ast
from ConfigParser import SafeConfigParser
import requests.packages.urllib3
import time
import imp

from modules.config.config import configGame

config = SafeConfigParser()
config.read('./config.ini')

class app:
    def __init__(self, token):
        self.bot = telegramBot(token)
        self.info=self.bot.getMe()
        self.updateId=False
        self.configGame=configGame(self.bot)

    def run(self):
        print("Bot {} iniciado".format(self.info['result']['username']))
        while (1):
            updates=self.bot.getUpdates(self.updateId)
            if(len(updates['result'])):
                self.updates = updates['result']
                self.updates.sort(key=lambda x: x["update_id"], reverse=False)
                self.updateId = self.updates[-1]['update_id'] + 1
                self.updateManager()
                time.sleep(1)

    def updateManager(self):
        for update in self.updates:
            id=None
            data=None
            if('message' in update):
                id = update['message']['chat']['id']
                data=update['message']
            if('callback_query' in update):
                id = update['callback_query']['message']['chat']['id']
                msg_id = update['callback_query']['message']['message_id']
                data = {'callback':update['callback_query']['data'], 'callbackId':update['callback_query']['id'], 'msg_id':msg_id}
            self.proccess(id,data)
    
    def proccess(self,id,data):
        if data.get('entities') and data['entities'][0]['type'] =='bot_command':
            if data['text']=='/start':
                self.configGame.playerNum(id,data,None,True)
        elif data.get('callback'):
            print data['callback']
        elif data.get('text'):
            print data['text']
        else:
            print data
    

if __name__ == "__main__":
    myApp=app(config.get('bot', 'token'))
    myApp.run()
    #main()

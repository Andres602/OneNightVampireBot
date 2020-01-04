#!/usr/bin/python
# -*- coding: utf-8 -*-

from ConfigParser import SafeConfigParser
import requests.packages.urllib3
import time

from modules.configGame import configGame
from libs import telegramBot
from libs import dbBot
from libs.tools import buildTemp

#read config file
config = SafeConfigParser()
config.read('./config.ini')

#read games file
games = SafeConfigParser()
games.read('./games.ini')

class app:
    def __init__(self):
        self.bot = telegramBot(config.get('bot', 'token'))
        self.db = dbBot(config.get('database','host'),config.get('database','port'),config.get('database','id'))
        self.info=self.bot.getMe()
        self.updateId=False
        self.configGame=configGame(self.bot, config.get('google','key'),self.db, "Vampire",games.get('Vampire','card'),config.get('game','pageSize'))

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
            #Check for user
            user=self.db.getUser(id)
            if(not user): 
                self.db.newUser(id)
                user=self.db.getUser(id)
            self.proccess(id,data,user)

    
    def proccess(self,id,data,user):
        if data.get('entities') and data['entities'][0]['type'] =='bot_command':
            if data['text']=='/start':
                self.db.setStep(id,"config.players")
                self.configGame.players(id,data,{},True)
        elif 'step' in user:
            go="self.configGame.%s"%(user['step'].split(".")[1])
            eval(go)(id,data,buildTemp(user),False)
        else:
            print "nothing 2 do"
        # elif data.get('callback'):
        #     print data['callback']
        # elif data.get('text'):
        #     print data['text']
        # else:
        #     print data
    


if __name__ == "__main__":
    myApp=app()
    myApp.run()
    #main()

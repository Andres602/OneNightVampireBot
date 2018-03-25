# -*- coding: utf-8 -*-
from dataFilter import dataFilter
from spanish import spanish


class configGame:
    def __init__(self, bot):
        self.bot=bot
        #self.db=db
        self.filter=dataFilter()
        self.language=spanish()

       

    def playerNum(self, id, data, temp, jumpTo=False):
        if jumpTo:
            keyboard=self.bot.makeKeyboard(self.language.get('keyboard','playerNum'),[3,3,2],inline=True)
            result=self.bot.sendMessage(id,self.language.get('text','playerNum'),keyboard)
            if result.get('ok'):
                print self.language.get('text','playerNum')
        else:
            result=self.filter.getPlayersNum(data)
            if 'error' in result:
                self.bot.sendMessage('id',self.language.get('error',result['error']))

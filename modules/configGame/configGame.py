# -*- coding: utf-8 -*-
from dataFilter import dataFilter
from spanish import spanish
from libs.buildFile import buildFile

class configGame:
    def __init__(self, bot,db, nameGame,cards,pageSize):
        self.bot=bot
        self.db=db
        self.cards=eval(cards)
        self.filter=dataFilter()
        self.language=spanish()
        self.nameGame=nameGame
        self.pageSize=int(pageSize)

    def players(self, id, data, temp, jumpTo=False):
        """Set number of players"""
        if jumpTo:
            keyboard=self.bot.makeKeyboard(self.language.get('keyboard','players'),[3,3,2])
            result=self.bot.sendMessage(id,self.language.get('text','players'),keyboard)
            if result.get('ok'):
                print self.language.get('text','players')
        else:
            result=self.filter.players(data)
            if 'error' in result:
                self.bot.sendMessage('id',self.language.get('error',result['error']))
                self.players(id,data,temp,True)
            else:
                gameId=self.db.newGame(id,self.nameGame,result)
                temp['gameId']=gameId
                temp['players']=result
                self.duration(id,data,temp,jumpTo=True)
    
    def duration(self, id, data, temp, jumpTo=False):
        """Set discution time of play"""
        if jumpTo:
            keyboard=self.bot.makeKeyboard(range(int(temp['players'])+1,int(temp['players'])+6),[1,1,1,1,1])
            result=self.bot.sendMessage(id,self.language.get('text','duration'),keyboard)
            if result.get('ok'):
                self.db.setStep(id,"config.duration")
                self.db.updateTemp(id,temp)
                print self.language.get('text','duration')
            else:
                print result
        else:
            result=self.filter.duration(data)
            if 'error' in result:
                self.bot.sendMessage('id',self.language.get('error',result['error']))
                self.duration(id,data,temp,True)
            else:
                self.db.setDuration(temp['gameId'],self.nameGame,result)
                self.characters(id,data,temp,jumpTo=True)
    
    def characters(self, id, data, temp, jumpTo=False):
        """Choose characters on game"""
        if jumpTo:
            keyboard=self.bot.makeKeyboard(self.charactersKeyboard(0,self.pageSize),[self.pageSize,4],inline=True)
            result=self.bot.sendMessage(id,self.charactersInfo(0,self.pageSize,[],int(temp['players'])),keyboard)
            if result.get('ok'):
                temp['messageId']=result.get('result').get('message_id')
                temp['page']=0
                self.db.setStep(id,"config.characters")
                self.db.updateTemp(id,temp)
                print self.language.get('text','characters')
            else:
                print result
        else:
            result=self.filter.characters(data)
            if 'error' in result:
                self.bot.sendMessage('id',self.language.get('error',result['error']))
            elif 'confirm' in result:
                messageId=temp['messageId']
                selected=self.db.getCharacters(temp['gameId'],self.nameGame) 
                charsInfo, charsOrder =self.charactersSelected(selected)
                result=self.bot.editMessage(id,messageId,charsInfo)
                if 'ok' in result:
                    print charsOrder
                    self.db.setCharacters(temp['gameId'],self.nameGame,charsOrder)
                    self.buildingGame(id,None,temp,jumpTo=True)
            else:
                messageId=temp['messageId']
                page=result['page'] if 'page' in result else temp['page']
                selected=self.db.updateCharacters(temp['gameId'],self.nameGame, self.cards[int(result['item'])]['name'])  if 'item' in result else self.db.getCharacters(temp['gameId'],self.nameGame) 
                keyboard=self.bot.makeKeyboard(self.charactersKeyboard(int(page),self.pageSize,int(temp['players'])+3==len(selected)),[self.pageSize,4],inline=True)
                result=self.bot.editMessage(id,messageId,self.charactersInfo(int(page),self.pageSize,selected,int(temp['players'])),keyboard)
                if result.get('ok'):
                    temp['page']=page
                    self.db.updateTemp(id,temp)

    def buildingGame(self, id, data, temp, jumpTo=False):
        """Set number of players"""
        if jumpTo:
            result=self.bot.sendMessage(id,self.language.get('text','buildingGame'))
            if result.get('ok'):
                print self.language.get('text','buildingGame')
                game=self.db.getGame(temp['gameId'],self.nameGame)
                fileOut=buildFile(game['characters'].split(","),"".join([temp['gameId'],self.nameGame]),game['duration'])
                result=self.bot.sendFile(id,'sendAudio',fileOut)
                if result==200:
                    self.bot.sendMessage(id,self.language.get('text','gamReady'))
                    print self.language.get('text','gamReady')
        

    #Tools of configurationGame
    def charactersKeyboard(self,page,pageSize,confirm=False):
        """Build character keyboard"""
        endPage=(len(self.cards)-1)/pageSize
        navigation=['⏮','page_0','⏪','page_%s'%(max(0,page-1)),'⏩','page_%s'%((page+1)%(endPage+1)),'⏭','page_%s'%(endPage)]
        items=[]
        start=page*pageSize
        for i in range(start,start+pageSize):
            if i < len(self.cards):
                items.extend([str(i+1),'item_%s'%(i)])
            else:
                items.extend([' ','blank_0'])
        items.extend(navigation)
        confirm and items.extend(self.language.get('keyboard','ok'))
        return items

    def charactersInfo(self, page, pageSize, selected, players):
        """Build character Info"""
        info=self.language.get('text','characters')%(players+3)
        selectList="".join([self.language.get('text','charactersInfo')%(len(selected),players+3),",".join(selected)])
        start=page*pageSize
        for i in range(start,min(start+pageSize,len(self.cards))):
            card=self.cards[i]
            if card['name'] in selected :
                info="".join([info,'*%s. %s*(_%s_)   🔵\n%s\n\n'%(i+1,card['name'],card['team'],card['description'])])
            else:
                info="".join([info,'*%s. %s*(_%s_)\n%s\n'%(i+1,card['name'],card['team'],card['description'])])
        info="".join([info,selectList])
        return info

    def charactersSelected(self,selected):
        """Build list of characters selected"""
        info=self.language.get('text','charactersOnGame')
        order=0
        newOrder=[]
        for i in range(len(self.cards)):
            card=self.cards[i]
            if card['name'] in selected:
                info="".join([info,'*%s. %s*(_%s_)   🔵\n%s\n\n'%(order+1,card['name'],card['team'],card['description'])])
                newOrder.append(card['name'])
                order=order+1
                if order==len(selected): break
        return info, newOrder
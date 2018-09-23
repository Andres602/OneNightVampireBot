# -*- coding: utf-8 -*-
import redis
from time import time  as time
from datetime import datetime as datetime

class dbBot:
    def __init__(self, host, port, database):
        self.r= redis.Redis(host=host, port=port, db=database)

    #users
    def getUser(self, id):
        return self.r.hgetall("user:%s"%(id))

    def newUser(self, id):
        """user:id"""
        user={"step": "config.players"}
        return self.r.hmset("user:%s"%(id), user)
    
    def setStep(self, id, step):
        """set bot step"""
        data={"step": step}
        return self.r.hmset("user:%s"%(id), data)

    def updateTemp(self, id, temp):
        data={}
        for key in temp:
            data['temp.%s'%(key)]=temp[key]
        return self.r.hmset("user:%s"%(id), data)

    #gameConfig
    def newGame(self, id, game, players):
        """game:gameCondig:id"""
        gameId=time()
        date=datetime.fromtimestamp(gameId).strftime('%d/%m/%y %H:%M')
        data={"user":id,"onCreated":date, "players": players }
        created=self.r.hmset("%s:gameConfig:%s"%(game,gameId),data)
        if created:
            data={"user":id,"onCreated":date, "Currentstep": "config" }
            flow=self.r.hmset("%s:gameFlow:%s"%(game,gameId),data)
            return gameId
    
    def getGame(self, id, game):
         return self.r.hgetall("%s:gameConfig:%s"%(game,id))
    
    def setDuration(self,id,game,duration):
        return self.r.hset("%s:gameConfig:%s"%(game,id),"duration",duration)

    def getDuration(self,id,game):
        return self.r.hget("%s:gameConfig:%s"%(game,id),"duration")

    def setCharacters(self,id,game,characters):
         return self.r.hset("%s:gameConfig:%s"%(game,id), 'characters',",".join(characters))

    def getCharacters(self,id,game):
        characters=[]
        try:
            characters=self.r.hget("%s:gameConfig:%s"%(game,id), 'characters').split(',')
        except:
            pass
        return characters
    
    def updateCharacters(self, id, game, character):
        """game:gameConfig:id"""
        characters=self.getCharacters(id,game)
        if character in characters:
            characters.remove(character)
        else:
            characters.append(character)
        if characters[0] == "":
            del characters[0]
        self.setCharacters(id,game,characters)
        return characters

    

    #gameFlow

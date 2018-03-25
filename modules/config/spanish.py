# -*- coding: utf-8 -*-
myText={
    'playerNum':'Ingrese el número de jugadores'
}

myError={
    'playerNum':'Por favor elija el número del teclado',
    'noCallback':'Por favor use el teclado',
}

mykeyboard={
    'playerNum':['3','numPlayer_3','4','numPlayer_4','5','numPlayer_5',
                '6','numPlayer_6','7','numPlayer_7','8','numPlayer_8',
                '9','numPlayer_9','10','numPlayer_10']
}

class spanish:
    def __init__(self):
        global myText, myError, mykeyboard
        self.myText=myText
        self.myError=myError
        self.mykeyboard=mykeyboard
    def get(self,kind,id):
        return self.myText[id] if kind =='text' else self.myError[id] if kind=='error' else self.mykeyboard[id]
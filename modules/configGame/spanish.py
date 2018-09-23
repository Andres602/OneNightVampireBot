# -*- coding: utf-8 -*-

myText={
    'players':'Elije número de jugadores:',
    'duration':"Elije el tiempo máximo (_minutos_) de la discución:",
    'characters': 'Elije %s personajes:\n',
    'charactersInfo':"\n*Seleccionados*(_%s de %s_):\n",
    'charactersOnGame': 'Los roles que jugarán son:\n',
    'buildingGame':"Espera unos minutos mienstras se genera el archivo con la narración del juego.",
    'gamReady':"Disfruta tu partida y recueda tener un cronometro a la mano para la parte de la discución.\nEnvia /start para configurar un nuevo juego."
}

myError={
    'players':'Por favor elija el número  de jugadores en teclado.',
    'duration':'Por favor elija el timepo en el teclado.',
    'characters': 'Por favor elija los personajes del teclado.',
    'charactersOnGame': 'charactersOnGame',
    'noCallback':'Por favor use el teclado.',
}

mykeyboard={
    'players':['3','4','5','6','7','8','9','10'],
    'characters':['Random','characters_random'],
    'ok':['Aceptar','confirm_1']
}

class spanish:
    def __init__(self):
        global myText, myError, mykeyboard
        self.myText=myText
        self.myError=myError
        self.mykeyboard=mykeyboard
    def get(self,kind,id):
        return self.myText[id] if kind =='text' else self.myError[id] if kind=='error' else self.mykeyboard[id]
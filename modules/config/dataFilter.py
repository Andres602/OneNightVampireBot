class dataFilter:
    def getPlayersNum(self, data):
        if 'callback' in data:
            result=data['callback'].split('_')
            return result[1]  if result[0]=='numPlayer' else {'error':'playerNum'}
        else:
            return {'error': 'noCallback'}
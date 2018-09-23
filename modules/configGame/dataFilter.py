class dataFilter:
    def players(self, data):
        if 'text' in data:
            return data['text'] if data['text'].isdigit() else {'error':'players'}
        else:
            return {'error': 'noCallback'}

    def duration(self, data):
        if 'text' in data:
            return data['text'] if data['text'].isdigit() else {'error':'duration'}
        else:
            return {'error': 'noCallback'}

    def characters(self, data):
        if 'callback' in data:
            result=data['callback'].split('_')
            return {result[0]:result[1]} if result[0] in ['page','item','confirm'] else {'error':'characters'}
        else:
            return {'error': 'noCallback'}
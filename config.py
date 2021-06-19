import json

class CONFIG():
    @staticmethod
    def get():
        with open('config.json') as fp:
            data = json.load(fp)
            return data
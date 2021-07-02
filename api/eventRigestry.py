import requests
from api.tools import *

class EventRegistry():
    def __init__(self, username, password):
        '''
            initial 就登入
            根據 self.status 判斷成功與否
        '''
        self.username = username    # 學號
        self.session = requests.Session()
        self.status = self.login(username, password)
    
    def login(self, username, password):
        '''
            登入活動報名系統
            return bool
        '''
        # get login token
        response = self.session.get('https://ccweb.ncnu.edu.tw/SLLL/login.asp')
        loginToken = find(response, 'input', param={'name': 'token'}).get('value')

        # request login page
        response = self.session.post(
            "https://ccweb.ncnu.edu.tw/SLLL/login.asp",
            data={
                'token': loginToken,
                'username': username,
                'password': password,
                'type': ''
            }
        )
        
        # 成功的話 return http 302, redirect
        if len(response.history)!=0:
            return True
        else:
            return False
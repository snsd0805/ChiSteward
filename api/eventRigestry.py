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
    
    def getEventsList(self):
        '''
            取得活動列表中的第一頁
            包含所有狀態的活動
        '''
        url = "https://ccweb.ncnu.edu.tw/SLLL/z6D3B52D553CA5831540D8CC7659967E58A62list.asp"
        response = self.session.get(url)

        with open('test.html') as fp:
            response = fp.read()
        
        root = BeautifulSoup(response, 'html.parser')
        events = root.find('table').findAll('tr')
        
        return [{
            'id':           getUrlParam(data[0].find('a').get('href').replace('&amp;', '&'), 'RowID'),
            # 活動詳細： 
            # https://ccweb.ncnu.edu.tw/SLLL/z6D3B52D553CA5831540D8CC7659967E58A62view.asp?showdetail=&RowID={}

            'semester':     data[1].text.replace('\n', ''),
            'status':       data[2].text.replace('\n', ''),     # 活動報名狀態
            'name':         data[3].text.replace('\n', ''),
            'time':         data[4].text.replace('\n', ''),     # 活動開始時間
            'method':       data[5].text.replace('\n', ''),     # 報名方式
            'hour':         data[6].text.replace('\n', ''),     # 時數
            'speaker':      data[7].text.replace('\n', ''),     # 講師
            'teacherEvent': data[8].text.replace('\n', ''),     # 申請為教師知能活動
        } for data in (event.findAll('td') for event in events[1:])]


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
        
        events = find(response, 'table').findAll('tr')
        
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

    def signUpPrepare(self, eventID):
        '''
            報名活動前的資料確認
            return 報名系統預設給的資料，供使用者確認
        '''
        url = "https://ccweb.ncnu.edu.tw/SLLL/z7DDA4E0A5831540Dadd.asp?showmaster=z958B653E5831540D4E4B6D3B52D5660E7D30&fk_RowID={}"
        response = self.session.get(url.format(eventID))
        inputs = find(response, 'form').findAll('input')

        values  = [inputData.get('value') for inputData in inputs]
        names   = [inputData.get('name')  for inputData in inputs]

        # 僅下列資料可更改
        #   - x_iphone  校內分機
        #   - x_phone   聯絡電話
        #   - x_zemail  EMAIL
        #   - x_remark  備註

        ans = {}
        for index in range(len(values)):
            ans[names[index]] = values[index]
        
        return ans

        # 前端接收後，僅可更改上述四項 value
        # 更改後送到 signUp(requestBody) function 中送出請求
    
    def signUp(self, requestBody):
        '''
            目前禁止使用！！！
        '''
        url = "https://ccweb.ncnu.edu.tw/SLLL/z7DDA4E0A5831540Dadd.asp"
        response = self.session.post(url, data=requestBody)

        if response.status_code == 200:
            return True
        else:
            return False

import time
import requests
from bs4 import BeautifulSoup
from api.tools import getUrlParam, findAll, find
import json

class Moodle():
    def __init__(self, username, password):
        '''
            Create a Moodle object to handle Session
            self.session handle cookies
        '''
        self.session = requests.Session()
        self.status = self.login(username, password)
        

    def login(self, username, password):
        '''
            For login to get Moodle Cookies
            self.session handle cookies automatically

            return True if Login Success
        '''
        # get login token
        response = self.session.get('https://moodle.ncnu.edu.tw/')
        loginToken = find(response, 'input', param={'name': 'logintoken'}).get('value')

        # login request
        response = self.session.post(
            'https://moodle.ncnu.edu.tw/login/index.php?authldap_skipntlmsso=1',
            data={
                'logintoken': loginToken,
                'username': username,
                'password': password
            }
        )
        # check whether login success
        # if it does, it return two 303 status code and redirected to Moodle main page
        if len(response.history) == 2:
            self.sessionKey = getUrlParam(
                find(response, 'a', param={'data-title': 'logout,moodle'}).get('href'), 'sesskey'
            )
            return True
        else:
            return False
    
    def getCourses(self, semester):
        '''
            取得該學年的所有課程列表
            Return {
                'id',
                'name'
            }
        '''
        response = self.session.get('https://moodle.ncnu.edu.tw/')
        courses = findAll(response, 'ul', param={'class': 'dropdown-menu'})[1]
        ans = []
        for course in courses:
            if course.text.split('-')[0]==semester:
                ans.append({
                    'id': getUrlParam(course.find('a').get('href'), 'id'),
                    'name': course.text,
                })
        return ans
    
    def getUpcomingEvents(self):
        '''
            取得 Event 列表
            僅包含 ID、大標題、時間
        '''
        response = self.session.get('https://moodle.ncnu.edu.tw/')
        events = findAll(response, 'div', param={'class': 'event'})
        ans = []
        for event in events:
            datas = event.findAll('a')
            ans.append({
                'id': datas[0].get('data-event-id'),
                'name': datas[0].text,
                'time': datas[1].text
            })
        return ans

    def getEvent(self, eventId):
        '''
            取得單一 Event 的細節
            額外取得 Description、課程資訊
        '''
        url = "https://moodle.ncnu.edu.tw/lib/ajax/service.php?sesskey={}&info=core_calendar_get_calendar_event_by_id"
        data = [
            {
                "index": 0,
                "methodname": "core_calendar_get_calendar_event_by_id",
                "args": { "eventid": eventId}
            }
        ]
        response = self.session.get(url.format(self.sessionKey), data=json.dumps(data))
        response = json.loads(response.text)[0]['data']['event']
        return {
            'id': response['id'],
            'name': response['name'],
            'description': response['description'],
            'course': {
                'id': response['course']['id'],
                'name': response['course']['fullname']
            }
        }

    def getWeekWorkInCourse(self, courseID):
        '''
            使用 CourseID 取得當週所公告的物件
            回傳 型別、名稱、連結
        '''
        
        url = "https://moodle.ncnu.edu.tw/course/view.php?id={}"
        response = self.session.get(url.format(courseID))
        # dateBlock = findAll(response, 'li', param={'class': 'section main clearfix'})[-2]
        block = find(response, 'li', param={'class': 'section main clearfix current'})

        if block:
            links = block.findAll('li')

            return [{
                'name': " ".join( link.text.split(' ')[:-1] ),
                'type': link.text.split(' ')[-1],
                'link': link.find('a').get('href')
            } for link in links]
        else:
            return None

    def getAnnoInCourse(self, courseID):
        '''
            使用 CourseID 取得最新公告
            block_news_items block
        '''
        url = "https://moodle.ncnu.edu.tw/course/view.php?id={}"
        response = self.session.get(url.format(courseID))
        block = find(response, 'div', param={'class': 'block_news_items block'})
        
        return [{
            'id': getUrlParam(
                anno.find('a').get('href'), 'd' ),
            'title': anno.text
        } for anno in block.findAll('div', 'info') ]
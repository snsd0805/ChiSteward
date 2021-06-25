import requests
from bs4 import BeautifulSoup
from api.tools import getUrlParam, findAll, find

class Moodle():
    def __init__(self):
        '''
            Create a Moodle object to handle Session
            self.session handle cookies
        '''
        self.session = requests.Session()
        # get login token, token is used for self.login()
        response = self.session.get('https://moodle.ncnu.edu.tw/')
        self.loginToken = find(response, 'input', {'name': 'logintoken'}).get('value')

    def login(self, username, password):
        '''
            For login to get Moodle Cookies
            self.session handle cookies automatically

            return True if Login Success
        '''
        response = self.session.post(
            'https://moodle.ncnu.edu.tw/login/index.php?authldap_skipntlmsso=1',
            data={
                'logintoken': self.loginToken,
                'username': username,
                'password': password
            }
        )
        # check whether login success
        # if it does, it return two 303 status code and redirected to Moodle main page
        if len(response.history) == 2:
            self.sessionKey = getUrlParam(
                find(response, 'a', {'data-title': 'logout,moodle'}).get('href'), 'sesskey'
            )
            print(self.sessionKey)
            return True
        else:
            return False
    
    def getCourses(self, semester):
        '''
            Get Courses link in this semester.
            Return a list including {
                'id',
                'name'
            }
        '''
        response = self.session.get('https://moodle.ncnu.edu.tw/')
        courses = findAll(response, 'ul', {'class': 'dropdown-menu'})[1]
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
            Get Upcomming Events
        '''
        response = self.session.get('https://moodle.ncnu.edu.tw/')
        events = findAll(response, 'div', {'class': 'event'})
        ans = []
        for event in events:
            datas = event.findAll('a')
            ans.append({
                'id': datas[0].get('data-event-id'),
                'name': datas[0].text,
                'time': datas[1].text
            })
        return ans

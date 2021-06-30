import requests
from api.tools import *

class NCNU():
    def __init__(self, username, password):
        self.session = requests.Session()
        self.status = self.login(username, password)
    
    def login(self, username, password):
        # get login token
        response = self.session.get('https://ccweb.ncnu.edu.tw/student/login.php')
        loginToken = find(response, 'input', param={'name': 'token'}).get('value')

        response = self.session.post(
            "https://ccweb.ncnu.edu.tw/student/login.php",
            data={
                'token': loginToken,
                'modal': '0',
                'username': username,
                'password': password,
                'type': 'a'
            }
        )
        if len(response.history)!=0:
            return True
        else:
            return False

    def getCourseTable(self, semester):
        url = "https://ccweb.ncnu.edu.tw/student/print_semester_course_list.php"

        # get token
        response = self.session.get(url)
        token = find(response, 'input', param={'name': 'token'}).get('value')
        response = self.session.post(
            url, 
            data={
                'year': semester,
                'font': 'microsoftjhenghei',
                'token': token,
            }
        )
        if response.status_code == 200:
            with open('{}課表.pdf'.format(semester), 'wb') as fp:
                fp.write(response.content)
            return True
        else:
            return False


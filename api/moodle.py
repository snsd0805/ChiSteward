import requests
from bs4 import BeautifulSoup
from config import CONFIG

class Moodle():
    def __init__(self):
        self.session = requests.Session()

        # get login token
        response = self.session.get('https://moodle.ncnu.edu.tw/')
        root = BeautifulSoup(response.text, 'html.parser')
        self.loginToken = root.find('input', {'name': 'logintoken'}).get('value')

    def login(self, username, password):
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
            return True
        else:
            return False
    
    def getCourses(self, semester):
        response = self.session.get('https://moodle.ncnu.edu.tw/')
        root = BeautifulSoup(response.text, 'html.parser')
        courses = root.findAll('ul', {'class': 'dropdown-menu'})[1] \
                      .findAll('li')
        ans = []
        for course in courses:
            if course.text.split('-')[0]==semester:
                ans.append({
                    'name': course.text,
                    'link': course.find('a').get('href')
                })
        return ans
            


moodle = Moodle()
if moodle.login('學號', '密碼'):
    print("登入成功")
    courses = moodle.getCourses("1092")
    for c in courses:
        print(c)
else:
    print("登入失敗")


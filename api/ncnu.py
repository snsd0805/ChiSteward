import requests
from api.tools import *

class NCNU():
    def __init__(self, username, password):
        '''
            initial 就登入
            根據 self.status 判斷成功與否
        '''
        self.session = requests.Session()
        self.status = self.login(username, password)
    
    def login(self, username, password):
        '''
            登入教務系統
            return bool
        '''
        # get login token
        response = self.session.get('https://ccweb.ncnu.edu.tw/student/login.php')
        loginToken = find(response, 'input', param={'name': 'token'}).get('value')

        # request login page
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
        
        # 成功的話 return http 302, redirect
        if len(response.history)!=0:
            return True
        else:
            return False

    def getCourseTable(self, semester):
        '''
            下載學期課表
            儲存在 ./<semester>課表.pdf
        '''
        url = "https://ccweb.ncnu.edu.tw/student/print_semester_course_list.php"

        # get token
        response = self.session.get(url)
        token = find(response, 'input', param={'name': 'token'}).get('value')

        # get pdf binary response 
        response = self.session.post(
            url, 
            data={
                'year': semester,
                'font': 'microsoftjhenghei',
                'token': token,
            }
        )

        # save pdf file
        if response.status_code == 200:
            with open('{}課表.pdf'.format(semester), 'wb') as fp:
                fp.write(response.content)
            return True
        else:
            return False

    def getScoreSummary(self):
        '''
            取得各學期的學分數、平均、排名
            return data 包含 semesters(list) & sum(dict) 兩部份

            各個學期的細項（各項課程分數）需要在另外的 function 做請求
        '''
        url = "https://ccweb.ncnu.edu.tw/student/aspmaker_student_selected_semester_stat_viewlist.php"
        response = self.session.get(url)

        if response.status_code == 200:
            histories = find(response, 'tbody').findAll('tr')

            # 各學年度的資料(含總和)
            semesterDatas = [{
                'semester':     data[0].text.replace('\n',''),      # 學期
                'select_num':   data[1].text.replace('\n',''),      # 選課數
                'pass_Num':     data[2].text.replace('\n',''),      # 及格課程數
                'pass_credit':  data[3].text.replace('\n',''),      # 及格學分數
                'average':      data[4].text.replace('\n',''),      # 平均  
                'rank':         data[5].text.replace('\n','')       # 班排名
            } for data in (his.findAll('td')[2:] for his in histories)]

            return {
                'semesters': semesterDatas[:-1],
                'sum': semesterDatas[-1]
            }
        else:
            return None
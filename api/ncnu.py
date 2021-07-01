import requests
from api.tools import *

class NCNU():
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
            } for data in (his.findAll('td')[2:]
                for his in histories)]

            return {
                'semesters': semesterDatas[:-1],
                'sum': semesterDatas[-1]
            }
        else:
            return None
    
    def getScore(self, semester):
        '''
            取得指定學期的各項成績
        '''
        url = "https://ccweb.ncnu.edu.tw/student/aspmaker_student_selected_semester_stat_viewview.php"
        url += "?showdetail=aspmaker_student_selected_view&studentid={}&year={}"
        response = self.session.get(url.format(self.username, semester))

        if response.status_code == 200:
            scores = find(response, 'div', param={'class': 'card ew-card ew-grid aspmaker_student_selected_view'}) \
                    .findAll('tr')
            return [{
                'number':       data[1].text.replace('\n',''),          # 
                'class':        data[2].text.replace('\n',''),
                'name':         data[3].text.replace('\n',''),
                'teacher':      data[4].text.replace('\n',''),
                'time':         data[5].text.replace('\n',''),
                'place':        data[6].text.replace('\n',''),
                'credit':       data[7].text.replace('\n',''),
                'score':        data[8].text.replace('\n',''),
                'mandatory':    data[9].text.replace('\n','')
            } for data in (score.findAll('td') for score in scores[1:])]
        else:
            return None
    
    def getAbsenceLogs(self):
        response = self.session.get("https://ccweb.ncnu.edu.tw/student/absencelist.php")
        table = find(response, 'tbody')

        if table:
            logs = table.findAll('tr')
            return [{
                'id':           data[0].text.replace('\n', ''),
                'semester':     data[1].text.replace('\n', ''),
                'classname':    data[2].text.replace('\n', ''),
                'date':         data[3].text.replace('\n', ''),
                'time':         data[4].text.replace('\n', '')
            } for data in (log.findAll('td') for log in logs)]
        else:
            return None
    
    def getAwardLogs(self):
        response = self.session.get('https://ccweb.ncnu.edu.tw/student/aspmaker_student_merit_viewlist.php?export=csv')
        datas = response.text.split('\r\n')[1:-1]
        
        if len(datas) == 2:
            return None
        else:  
            return [{
                'id':       data[0],
                'semester': data[1],
                'award':    data[2],
                'count':    data[3],
                'content':  data[4],
            } for data in (data.replace('"', '').split(',') for data in datas)]
    
    def getAddCourseLogs(self):
        response = self.session.get('https://ccweb.ncnu.edu.tw/student/applyaddcourselist.php?export=csv')
        datas = response.text.split('\r\n')[1:-1]
        
        if len(datas) == 2:
            return None
        else:
            return [{
                'id':           data[0],
                'semester':     data[1],
                'classname':    data[2]+data[3],
                'class':        data[4],
                'check':        data[5],
            } for data in (data.replace('"', '').split(',') for data in datas)]
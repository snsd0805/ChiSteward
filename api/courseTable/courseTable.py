'''
{
    'link': 'https://ccweb.ncnu.edu.tw/student/aspmaker_course_opened_detail_viewview.php?showmaster=aspmaker_course_opened_semester_stat_view&fk_year=1092&fk_deptid=00&year=1092&courseid=000008&_class=0', 
    'year': '1092', 
    'number': '000008', 
    'class': '0', 
    'name': '自我覺察與專業成長', 
    'department': '00, 諮人系', 
    'graduated': '學士班', 
    'grade': '1', 
    'teacher': '蔡毅樺', 
    'place': 'A104+B104專業教室', 
    'time': '4efg'
}

'''
import requests
import json



def getTime(time):
    number = 0
    ans = []
    for c in time:
        if c <= '9' and c >= '0':
            number = c
        else:
            ans.append(str(number)+c)
    return ans

class CourseTable():
    def __init__(self):
        '''
            初始化課表
            取得課堂資料
        '''
        self.table = {}
        for i in range(1, 6):
            for j in "abcdzefghijklm":
                self.table[str(i)+j] = None
                
        self.courseData = json.loads(
            requests.get('https://raw.githubusercontent.com/snsd0805/NCNU_Course/master/%E6%AD%B7%E5%B9%B4%E8%AA%B2%E7%A8%8B%E8%B3%87%E6%96%99/1092_output.json').text
        )
        
    
    def showTableStatus(self):
        '''
            For debug
        '''
        for j in "abcdzefghijklm":
            for i in range(1, 6):
                if self.table[str(i)+j] != None:
                    print("{} ".format(1), end='')
                else:
                    print("{} ".format(0), end='')
            print()
    
    def add(self, courseID):
        '''
            使用 course ID 新增課程到課表
            若課程時間不符或者該時間已經有了則新增失敗
        '''
        for course in self.courseData:
            if course['number'] == courseID:
                targetCourse = course
        
        timeList = getTime(targetCourse['time'])
        
        if self.conflict(targetCourse):
            for time in timeList:
                self.table[time] = targetCourse
            return True
        else:
            return False
    
    def remove(self, courseID):
        '''
            移除課程
        '''
        for key, value in self.table.items():
            if value['number'] == courseID:
                self.table[key] = None
    
    def getDepartmentList(self):
        ans = set()
        for course in self.courseData:
            ans.add(
                course['department']
            )
        ans = [i for i in ans]
        ans.sort()
        
        return ans
    
    def conflict(self, course):
        if course['time'] != None:
            timeList = getTime(course['time'])
        else:
            return False
        status = True
        for time in timeList:
            if time in self.table:
                if self.table[time] != None:
                    status = False
                    break
            else:
                status = False
        
        return status
    
    def courseFilter(self, department):
        ans = []
        for course in self.courseData:
            if course['department'] == department:
                if self.conflict(course):
                    ans.append(course)
        return ans

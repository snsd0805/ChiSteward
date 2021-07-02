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


class Course():
    def __init__(self, data):
        self.data = data
    
    def getTime(self):
        number = 0
        ans = []
        for c in self.data['time']:
            if c <= '9' and c >= '0':
                number = c
            else:
                ans.append(number+c)
        return ans

class CourseTable():
    def __init__(self):
        self.table = {}
        for i in range(1, 6):
            for j in "abcdzefghijklm":
                self.table[str(i)+j] = None
                
        self.courseData = json.loads(
            requests.get('https://raw.githubusercontent.com/snsd0805/NCNU_Course/master/%E6%AD%B7%E5%B9%B4%E8%AA%B2%E7%A8%8B%E8%B3%87%E6%96%99/1092_output.json').text
        )
    
    def showTableStatus(self):
        for j in "abcdzefghijklm":
            for i in range(1, 6):
                if self.table[str(i)+j] != None:
                    print("{} ".format(1), end='')
                else:
                    print("{} ".format(0), end='')
            print()
    
    def add(self, courseID):
        for course in self.courseData:
            if course['number'] == courseID:
                targetCourse = Course(course)
        
        timeList = targetCourse.getTime()
        print(timeList)
        status = True
        for time in timeList:
            if time in self.table:
                if self.table[time] != None:
                    status = False
                    break
            else:
                status = False
        
        if status:
            for time in timeList:
                self.table[time] = targetCourse
            return True
        else:
            return False
    
    def remove(self, courseID):
        for key, value in self.table.items():
            if value.data['number'] == courseID:
                self.table[key] = None
        

table = CourseTable()
table.showTableStatus()
print( table.add('240034') )
table.showTableStatus()
print( table.add('240057') )
table.showTableStatus()
print( table.add('240034') )
table.showTableStatus()
print( table.add('902048') )
table.showTableStatus()
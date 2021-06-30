from config import CONFIG
from api.moodle import Moodle

moodle = Moodle(CONFIG['moodle']['username'], CONFIG['moodle']['password'])
if moodle.status:
    for c in moodle.getCourses("1092"):
        print(c)
    for e in moodle.getUpcomingEvents():
        print(e)    
    for work in moodle.getWeekWorkInCourse('47562'):
        print(work)
    for anno in moodle.getAnnoInCourse('47555'):
        print(anno)
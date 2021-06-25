from config import CONFIG
from api.moodle import Moodle

moodle = Moodle()

if moodle.login(CONFIG['moodle']['username'], CONFIG['moodle']['password']):
    print("登入成功")
    courses = moodle.getCourses("1092")
    for c in courses:
        print(c)
    events = moodle.getUpcomingEvents()
    for e in events:
        print(e)
else:
    print("登入失敗")



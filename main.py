from config import CONFIG
from api.moodle import Moodle
from api.ncnuMain import NcnuMain

def space():
    print("\n" + "="*20 + "\n")

moodle = Moodle(CONFIG['moodle']['username'], CONFIG['moodle']['password'])
if moodle.status:
    for c in moodle.getCourses("1092"):
        print(c)
    space()
    for e in moodle.getUpcomingEvents():
        print(e)
    space()
    for work in moodle.getWeekWorkInCourse('47562'):
        print(work)
    space()
    for anno in moodle.getAnnoInCourse('47555'):
        print(anno)
    space()

main = NcnuMain()
for anno in main.getAnno():
    print(anno)
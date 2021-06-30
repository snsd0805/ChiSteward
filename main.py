from config import CONFIG
from api.moodle import Moodle
from api.ncnuMain import NcnuMain
from api.ncnu import NCNU

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
else:
    print("Moodle 登入失敗")

main = NcnuMain()
for anno in main.getAnno():
    print(anno)
space()

ncnu = NCNU(CONFIG['NCNU']['username'], CONFIG['NCNU']['password'])
if ncnu.status:
    if ncnu.getCourseTable('1092'):
        print("1092 課表已經儲存到 ./1092課表.pdf")
    else:
        print("無法存取 1092 課表")
    
    scores = ncnu.getScoreSummary()
    for c in scores['semesters']:
        print(c)
    print(scores['sum'])
else:
    print("NCNU 教務系統登入失敗")

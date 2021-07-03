from config import CONFIG
from api.moodle import MoodleAPI
from api.ncnuMain import NcnuMainAPI
from api.ncnu import NcnuAPI
from api.eventRigestry import EventRegistry

def space():
    print("\n" + "="*20 + "\n")

# =================== TEST Moodle API ==========================

# ===== Test 登入 =====
moodle = MoodleAPI(CONFIG['moodle']['username'], CONFIG['moodle']['password'])
if moodle.status:

    # ===== Test 取得該學期課程資料 =====
    for c in moodle.getCourses("1092"):
        print(c)
    space()

    # ===== Test 取得未來重要事件 =====
    for e in moodle.getUpcomingEvents():
        print(e)
    space()

    # ===== Test 取得課程在當週發布的物件 （ 文件、功課、BBB連結... 等）
    for work in moodle.getWeekWorkInCourse('47552'):
        print(work)
    space()

    # ===== TEST 取得該課程的最新公告
    for anno in moodle.getAnnoInCourse('47552'):
        print(anno)
    space()
else:
    print("Moodle 登入失敗")



# =================== Test 暨大官網 API ==========================

# ===== Test 取得暨大官網最新消息 =====
main = NcnuMainAPI()
for anno in main.getAnno():
    print(anno)
space()



# =================== Test 暨大教務系統 API ==========================

# ===== Test 登入 =====
ncnu = NcnuAPI(CONFIG['NCNU']['username'], CONFIG['NCNU']['password'])
if ncnu.status:

    # ===== Test 下載課表 =====
    if ncnu.getCourseTable('1092'):
        print("1092 課表已經儲存到 ./1092課表.pdf")
    else:
        print("無法存取 1092 課表")
    space()

    # ===== Test 取得各學期成績總覽 =====
    scores = ncnu.getScoreSummary()
    for c in scores['semesters']:
        print(c)
    print(scores['sum'])
    space()

    # ===== Test 取得指定學期的成績列表 =====
    scores = ncnu.getScore('1092')
    for i in scores:
        print(i)
    space()

    # ===== Test 取得所有缺曠課記錄 =====
    absenceLogs = ncnu.getAbsenceLogs()
    if absenceLogs:
        for log in absenceLogs:
            print(log)
    else:
        print("沒有任何缺曠課記錄")
    space()

    # ===== Test 獎懲紀錄 =====
    awardLogs = ncnu.getAwardLogs()
    if awardLogs:
        for log in awardLogs:
            print(log)
    else:
        print("沒有任何獎懲紀錄")
    space()

    # ===== Test 取得加選課程狀態 =====
    logs = ncnu.getAddCourseLogs()
    if logs:
        for log in logs:
            print(log)
    space()
else:
    print("NCNU 教務系統登入失敗")




# =================== Test 暨大活動報名系統 API ==========================

# ===== Test 登入 =====
eventReg = EventRegistry(CONFIG['NCNU']['username'], CONFIG['NCNU']['password'])
if eventReg.status:
    print("登入成功")
    space()

    # ===== Test 取得所有活動第一頁的列表 =====
    for event in eventReg.getEventsList():
        print(event)
    space()

    # ===== Test 報名前準備 request body =====
    requestBody = eventReg.signUpPrepare('3010')
    for key, value in requestBody.items():
        print("{}: {}".format(key, value))
    space()
else:
    print("登入失敗")

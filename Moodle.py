from tkinter import *
from api.moodle import MoodleAPI
from config import CONFIG
from tkhtmlview import HTMLLabel

def getIdAndName(course):
    coursesId=[]
    courseName=[]
    for i in course:
        coursesId.append(i.get("id"))
        tmp=i.get("name").split(" ")
        courseName.append(tmp[1])
    return coursesId ,courseName   
    

def createMoodleWin():
    moodle = MoodleAPI(CONFIG['moodle']['username'], CONFIG['moodle']['password'])
    
    if moodle.status:
         # ===== 取得課程ID與名稱 =====
        c = moodle.getCourses("1092")
        coursesId,coursesName=getIdAndName(c)
       
         #for e in moodle.getUpcomingEvents()  
        
        win=Tk()

        rightFrame=Frame(win,bg="red")
        leftFrame=Frame(win)
        #===== 右框 初始化 用html去印出所有資料=====
        htmlLb=HTMLLabel(rightFrame,html="")
        htmlScrollbar=Scrollbar(rightFrame)
        htmlLb.configure(yscrollcommand=htmlScrollbar.set)
                   
        htmlScrollbar.pack(fill=Y,side=RIGHT)
        htmlLb.pack()
    
        leftFrame.pack(fill=BOTH,side=LEFT)
        rightFrame.pack(fill=BOTH)
        #=====Leftframe 1.button ->show UpComingEvent 2.choose courses=======
        
        def showUpComingEvent(): #叫出未來事件
            tmphtml=''''''
            for e in moodle.getUpcomingEvents():
                tmphtml+='''<br> {} <br>時間:{} <p>'''.format(e.get("name"),e.get("time") )
            #tmphtml+='''</ul>'''
            htmlLb.set_html(tmphtml)

        upComingEventBtn=Button(leftFrame,text="未來事件",font="Helvetica 10",command= lambda:showUpComingEvent() )
        coursesListBox=Listbox(leftFrame)
        mylb=Label(leftFrame,text="我的課程",font="Helvetica 15")
        coursesListBox.insert(END,*coursesName)
        
        mylb.pack(fill=X)
        coursesListBox.pack(fill=BOTH)
        upComingEventBtn.pack(fill=BOTH,pady=10)
        
        #=======rightframe ->show everything which I click======
        def itemSelected(event):
            obj = event.widget
            Index = obj.curselection()
            tmpId=coursesId[coursesName.index(str(obj.get(Index)))]
            Html='''<h3>本周作業</h3><ol>'''
            for work in moodle.getWeekWorkInCourse(str(tmpId)):
                Html+='''<li> <a href={}> {}</a> </li>'''.format(work.get("link"),work.get("name") )
            Html+='''</ol><h3>最新公告</h3><ol>'''
            for anno in moodle.getAnnoInCourse(str(tmpId)):
                Html+='''<li>{}</li>'''.format(anno.get("title"))
            Html+='''</ol>'''    
            htmlLb.set_html(Html)
            
        coursesListBox.bind("<<ListboxSelect>>", itemSelected)

        win.mainloop()

    else:
        print("Moodle 登入失敗")

createMoodleWin()

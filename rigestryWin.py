from api.eventRigestry import EventRegistry
from config import CONFIG
from tkinter import *
from tkhtmlview import HTMLLabel


def createRigestryWin():
    
    root=Tk()
    frame1=Frame(root)
    frame2=Frame(root)
    frame1.pack(side=LEFT)
    frame2.pack()
    winScrollBar=Scrollbar(frame1)
    htmlLb=HTMLLabel(frame1,html="")
    
    
    winScrollBar.pack(side=RIGHT,fill="y")
    htmlLb.pack(fill=BOTH)
    htmlLb.configure(yscrollcommand=winScrollBar.set)

    ht='''<span style="background-color:#ffcccc"><h5>讀取中</h5></span>'''  
    htmlLb.set_html(ht)
    root.update()
    html=''''''
        
    root.update()
    
    
    rigestry=EventRegistry(CONFIG['moodle']['username'], CONFIG['moodle']['password'])
    tmpid=[]
    tmpname=[]
    if rigestry.status:
        for i in rigestry.getEventsList(): 
            html+='''<tr> <td>活動ID:{}</td> <td>學期{}</td> <br> <td>活動報名狀態:{}</td> <br> <td>活動名稱:{}</td> <br> <td>活動開始時間: {}</td> <br> <td>報名方式:{}</td> <br> <td>時數: {}</td> <br><td>講師: {}</td> <br> <td>申請為教師之能活動: {}</td> </tr><p> '''.format(
            i.get("id"),i.get("semester"),i.get("status"),i.get("name"),i.get("time"),i.get("method"),i.get("hour"),i.get("speaker"),i.get("teacherEvevt") )
            tmpid.append(i.get("id"))
            tmpname.append(i.get("name"))    
        htmlLb.set_html(html)
    else:
        print("NO")

    def signUp(id):
        win=Tk()
        rigestry.signUpPrepare(id)

        win.mainloop()
        

    for i in range(len(tmpname)):
        Button(frame2,text="我要報名  {}".format(tmpname[i]),command=lambda:signUp(tmpid[i]) ).pack(anchor="w")
        
    root.update()        

    root.mainloop()

createRigestryWin()


from api.eventRigestry import EventRegistry
from config import CONFIG
from tkinter import *
from tkhtmlview import HTMLLabel

def createRigestryWin():
    
    root=Tk()
    winScrollBar=Scrollbar(root)
    htmlLb=HTMLLabel(root,html="")
    winScrollBar.pack(side=RIGHT,fill="y")
    htmlLb.pack(fill=BOTH)

    
    htmlLb.configure(yscrollcommand=winScrollBar.set)

    ht='''<span style="background-color:#ffcccc"><h5>讀取中</h5></span>'''  
    htmlLb.set_html(ht)
    root.update()
    html=''''''
    
    rigestry=EventRegistry(CONFIG['moodle']['username'], CONFIG['moodle']['password'])

    if rigestry.status:
        for i in rigestry.getEventsList(): 
            html+='''<tr> <td>活動ID:{}</td> <td>學期{}</td> <br> <td>活動報名狀態:{}</td> <br> <td>活動名稱:{}</td> <br> <td>活動開始時間: {}</td> <br> <td>報名方式:{}</td> <br> <td>時數: {}</td> <br><td>講師: {}</td> <br> <td>申請為教師之能活動: {}</td> </tr><p> '''.format(
            i.get("id"),i.get("semester"),i.get("status"),i.get("name"),i.get("time"),i.get("method"),i.get("hour"),i.get("speaker"),i.get("teacherEvevt") )
            
        htmlLb.set_html(html)

    else:
        print("NO")        

    root.mainloop()
